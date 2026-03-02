from django.views.generic import CreateView, UpdateView, ListView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404, render
from django.db import transaction
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.template.loader import render_to_string
from apy.decorators import PermisoRequeridoMixin

# Librería para el PDF
from xhtml2pdf import pisa

# Modelos y Formularios
from apy.models import (
    DetalleServicio,
    Repuesto,
    TipoMantenimiento,
    Insumos,
    Vehiculo,
    Profile,
)
from apy.forms import (
    DetalleServicioForm,
    DetalleRepuestoFormSet,
    DetalleTipoMantenimientoFormSet,
    DetalleInsumosFormSet,
)


# ─────────────────────────────────────────────────────────────
# LISTAR SERVICIOS ACTIVOS
# ─────────────────────────────────────────────────────────────
class ListServicioView(PermisoRequeridoMixin, ListView):

    module_name = 'Factura'
    permission_required = 'view'

    model = DetalleServicio
    template_name = 'detalle_servicio/lista_servicios.html'
    context_object_name = 'servicios'
    ordering = ['-fecha_creacion']

    def get_queryset(self):
        return DetalleServicio.objects.filter(estado=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_servicios']   = DetalleServicio.objects.count()
        context['servicios_activos'] = DetalleServicio.objects.filter(estado=True).count()
        return context


# ─────────────────────────────────────────────────────────────
# LISTAR SERVICIOS INACTIVOS
# ─────────────────────────────────────────────────────────────
class ServicioInactivosListView(PermisoRequeridoMixin, ListView):

    module_name = 'Factura'
    permission_required = 'view'

    model = DetalleServicio
    template_name = 'detalle_servicio/modal_inactivos.html'
    context_object_name = 'servicios_inactivos'

    def get_queryset(self):
        return DetalleServicio.objects.filter(estado=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_servicios']   = DetalleServicio.objects.count()
        context['servicios_activos'] = DetalleServicio.objects.filter(estado=True).count()
        return context


# ─────────────────────────────────────────────────────────────
# CREAR SERVICIO
# ─────────────────────────────────────────────────────────────
class CreateServicioView(PermisoRequeridoMixin, CreateView):

    module_name = 'Factura'
    permission_required = 'add'

    model = DetalleServicio
    form_class = DetalleServicioForm
    template_name = 'detalle_servicio/crear_servicio.html'
    success_url = reverse_lazy('apy:lista_servicios')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['repuesto_formset']      = DetalleRepuestoFormSet(self.request.POST, prefix='repuestos')
            context['mantenimiento_formset'] = DetalleTipoMantenimientoFormSet(self.request.POST, prefix='mantenimientos')
            context['insumo_formset']        = DetalleInsumosFormSet(self.request.POST, prefix='insumos')
        else:
            context['repuesto_formset']      = DetalleRepuestoFormSet(prefix='repuestos')
            context['mantenimiento_formset'] = DetalleTipoMantenimientoFormSet(prefix='mantenimientos')
            context['insumo_formset']        = DetalleInsumosFormSet(prefix='insumos')

        context['repuestos']           = Repuesto.objects.filter(estado=True)
        context['tipos_mantenimiento'] = TipoMantenimiento.objects.filter(estado=True)
        context['insumos']             = Insumos.objects.filter(estado=True)
        context['perfiles']            = Profile.objects.select_related('user').filter(user__is_active=True)
        return context

    @transaction.atomic
    def form_valid(self, form):
        repuesto_formset      = DetalleRepuestoFormSet(self.request.POST, prefix='repuestos')
        mantenimiento_formset = DetalleTipoMantenimientoFormSet(self.request.POST, prefix='mantenimientos')
        insumo_formset        = DetalleInsumosFormSet(self.request.POST, prefix='insumos')

        if repuesto_formset.is_valid() and mantenimiento_formset.is_valid() and insumo_formset.is_valid():

            # Validar stock suficiente ANTES de guardar nada
            errores_stock = self._validar_stock_suficiente(repuesto_formset, insumo_formset)
            if errores_stock:
                for error in errores_stock:
                    messages.error(self.request, error)
                return self.render_to_response(self.get_context_data(form=form))

            # Guardar el servicio principal
            self.object = form.save()

            # Asignar instancia y guardar cada formset
            repuesto_formset.instance      = self.object
            mantenimiento_formset.instance = self.object
            insumo_formset.instance        = self.object

            repuesto_formset.save()
            mantenimiento_formset.save()
            insumo_formset.save()

            # Notificar stock bajo DESPUÉS de guardar (señales ya descontaron)
            self._notificar_stock_bajo_servicio(self.request, repuesto_formset, insumo_formset)

            # ── Mensaje seguro: recargamos desde BD antes de acceder a la FK ──
            try:
                self.object.refresh_from_db()
                placa = self.object.id_vehiculo.placa
            except Exception:
                placa = f"ID {self.object.id}"

            messages.success(
                self.request,
                f'Servicio #{self.object.id} — Vehículo {placa} registrado correctamente.'
            )
            return redirect(self.success_url)

        else:
            # Mostrar errores detallados de cada formset
            for fs_nombre, fs in [
                ('Repuestos',      repuesto_formset),
                ('Mantenimientos', mantenimiento_formset),
                ('Insumos',        insumo_formset),
            ]:
                for fs_form in fs:
                    for field, errors in fs_form.errors.items():
                        for e in errors:
                            messages.error(self.request, f'{fs_nombre} — {field}: {e}')

            messages.error(self.request, 'Corrige los errores en el formulario.')
            return self.render_to_response(self.get_context_data(form=form))

    def _validar_stock_suficiente(self, repuesto_formset, insumo_formset):
        """
        Verifica stock antes de guardar.
        Retorna lista de mensajes de error, vacía si todo OK.
        """
        errores = []

        for form in repuesto_formset:
            if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                repuesto = form.cleaned_data.get('id_repuesto')
                cantidad = form.cleaned_data.get('cantidad', 0)
                if repuesto and cantidad and repuesto.stock < cantidad:
                    errores.append(
                        f'❌ Stock insuficiente para repuesto "{repuesto.nombre}": '
                        f'disponible {repuesto.stock}, solicitado {cantidad}.'
                    )

        for form in insumo_formset:
            if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                insumo   = form.cleaned_data.get('id_insumos')
                cantidad = form.cleaned_data.get('cantidad', 0)
                if insumo and cantidad and insumo.stock < cantidad:
                    errores.append(
                        f'❌ Stock insuficiente para insumo "{insumo.nombre}": '
                        f'disponible {insumo.stock}, solicitado {cantidad}.'
                    )
        return errores

    def _notificar_stock_bajo_servicio(self, request, repuesto_formset, insumo_formset):
        """
        Emite warnings para ítems con stock bajo tras descontar del inventario.
        Usa refresh_from_db() para leer el stock actualizado por las señales.
        """
        for form in repuesto_formset:
            if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                repuesto = form.cleaned_data.get('id_repuesto')
                if repuesto:
                    repuesto.refresh_from_db()
                    if repuesto.stock_bajo:
                        messages.warning(
                            request,
                            f'⚠️ Repuesto "{repuesto.nombre}": quedan {repuesto.stock} unidades '
                            f'(mínimo: {repuesto.stock_minimo}). Considera reabastecer.'
                        )

        for form in insumo_formset:
            if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                insumo = form.cleaned_data.get('id_insumos')
                if insumo:
                    insumo.refresh_from_db()
                    if insumo.stock_bajo:
                        messages.warning(
                            request,
                            f'⚠️ Insumo "{insumo.nombre}": quedan {insumo.stock} unidades '
                            f'(mínimo: {insumo.stock_minimo}). Considera reabastecer.'
                        )


# ─────────────────────────────────────────────────────────────
# EDITAR SERVICIO
# ─────────────────────────────────────────────────────────────
class UpdateServicioView(PermisoRequeridoMixin, UpdateView):

    module_name = 'Factura'
    permission_required = 'change'

    model = DetalleServicio
    form_class = DetalleServicioForm
    template_name = 'detalle_servicio/crear_servicio.html'
    success_url = reverse_lazy('apy:lista_servicios')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.POST:
            context['repuesto_formset']      = DetalleRepuestoFormSet(self.request.POST, instance=self.object, prefix='repuestos')
            context['mantenimiento_formset'] = DetalleTipoMantenimientoFormSet(self.request.POST, instance=self.object, prefix='mantenimientos')
            context['insumo_formset']        = DetalleInsumosFormSet(self.request.POST, instance=self.object, prefix='insumos')
        else:
            context['repuesto_formset']            = DetalleRepuestoFormSet(instance=self.object, prefix='repuestos')
            context['repuesto_formset'].extra       = 0
            context['mantenimiento_formset']        = DetalleTipoMantenimientoFormSet(instance=self.object, prefix='mantenimientos')
            context['mantenimiento_formset'].extra  = 0
            context['insumo_formset']               = DetalleInsumosFormSet(instance=self.object, prefix='insumos')
            context['insumo_formset'].extra         = 0

        context['repuestos']           = Repuesto.objects.filter(estado=True)
        context['tipos_mantenimiento'] = TipoMantenimiento.objects.filter(estado=True)
        context['insumos']             = Insumos.objects.filter(estado=True)
        context['perfiles']            = Profile.objects.select_related('user').filter(user__is_active=True)
        context['modo_edicion']        = True

        return context

    @transaction.atomic
    def form_valid(self, form):
        repuesto_formset      = DetalleRepuestoFormSet(self.request.POST, instance=self.object, prefix='repuestos')
        mantenimiento_formset = DetalleTipoMantenimientoFormSet(self.request.POST, instance=self.object, prefix='mantenimientos')
        insumo_formset        = DetalleInsumosFormSet(self.request.POST, instance=self.object, prefix='insumos')

        if repuesto_formset.is_valid() and mantenimiento_formset.is_valid() and insumo_formset.is_valid():
            self.object = form.save()

            repuesto_formset.instance      = self.object
            mantenimiento_formset.instance = self.object
            insumo_formset.instance        = self.object

            repuesto_formset.save()
            mantenimiento_formset.save()
            insumo_formset.save()

            # Mensaje seguro con refresh_from_db
            try:
                self.object.refresh_from_db()
                placa = self.object.id_vehiculo.placa
            except Exception:
                placa = f"ID {self.object.id}"

            messages.success(
                self.request,
                f'Servicio #{self.object.id} — Vehículo {placa} actualizado correctamente.'
            )
            return redirect(self.success_url)

        else:
            messages.error(self.request, 'Corrige los errores antes de guardar.')
            return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form):
        print("ERRORES FORM:", form.errors)
        return super().form_invalid(form)


# ─────────────────────────────────────────────────────────────
# ELIMINAR SERVICIO (lógico)
# ─────────────────────────────────────────────────────────────
class DeleteServicioView(PermisoRequeridoMixin, DeleteView):

    module_name = 'Factura'
    permission_required = 'delete'

    model = DetalleServicio
    template_name = 'detalle_servicio/eliminar_servicio.html'
    success_url = reverse_lazy('apy:lista_servicios')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.estado = False
        self.object.save()
        messages.success(self.request, f'Servicio #{self.object.id} desactivado correctamente.')
        return HttpResponseRedirect(self.get_success_url())


# ─────────────────────────────────────────────────────────────
# ACTIVAR SERVICIO
# ─────────────────────────────────────────────────────────────
class ServicioActivateView(PermisoRequeridoMixin, DeleteView):

    module_name = 'Factura'
    permission_required = 'delete'

    model = DetalleServicio
    template_name = 'detalle_servicio/activar_servicio.html'
    success_url = reverse_lazy('apy:lista_servicios')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.estado = True
        self.object.save()
        messages.success(self.request, f'Servicio #{self.object.id} activado correctamente.')
        return HttpResponseRedirect(self.get_success_url())


# ─────────────────────────────────────────────────────────────
# DETALLE / VER SERVICIO
# ─────────────────────────────────────────────────────────────
class DetalleServicioView(PermisoRequeridoMixin, DetailView):

    module_name = 'Factura'
    permission_required = 'view'

    model = DetalleServicio
    template_name = 'detalle_servicio/detalle_servicio.html'
    context_object_name = 'servicio'

    def get_queryset(self):
        return DetalleServicio.objects.prefetch_related(
            'detallerepuesto_set__id_repuesto',
            'detalletipomantenimiento_set__id_tipo_mantenimiento',
            'detalleinsumos_set__id_insumos__id_marca',
            'id_vehiculo__id_cliente',
        ).select_related('id_vehiculo')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        servicio = self.get_object()
        context.update({
            'repuestos':      servicio.detallerepuesto_set.all(),
            'mantenimientos': servicio.detalletipomantenimiento_set.all(),
            'insumos':        servicio.detalleinsumos_set.all(),
            'subtotal':       servicio.subtotal,
        })
        return context


# ─────────────────────────────────────────────────────────────
# CREAR SERVICIO DESDE MODAL
# ─────────────────────────────────────────────────────────────
class DetalleCreateModalView(PermisoRequeridoMixin, CreateView):

    module_name = 'Factura'
    permission_required = 'add'

    model = DetalleServicio
    form_class = DetalleServicioForm
    template_name = 'detalle_servicio/modal_detalle.html'
    success_url = reverse_lazy('apy:lista_servicios')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.estado = True
        try:
            self.object = form.save()
            return JsonResponse({
                'success': True,
                'id':      self.object.id,
                'text':    str(self.object),
                'message': 'Servicio registrado correctamente ✅',
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error al guardar: {str(e)}',
            }, status=500)

    def form_invalid(self, form):
        html = render_to_string(self.template_name, {'form': form}, request=self.request)
        return JsonResponse({
            'success': False,
            'html':    html,
            'message': 'Por favor, corrige los errores en el formulario ❌',
        })


# ─────────────────────────────────────────────────────────────
# IMPRIMIR FACTURA EN PDF
# ─────────────────────────────────────────────────────────────
def imprimir_servicio_factura(request, pk):
    servicio = get_object_or_404(DetalleServicio, pk=pk)

    context = {
        'servicio':       servicio,
        'vehiculo':       servicio.id_vehiculo,
        'cliente':        servicio.id_vehiculo.id_cliente,
        'repuestos':      servicio.detallerepuesto_set.all(),
        'mantenimientos': servicio.detalletipomantenimiento_set.all(),
        'insumos':        servicio.detalleinsumos_set.all(),
        'total': (
            sum(r.subtotal for r in servicio.detallerepuesto_set.all()) +
            sum(m.subtotal for m in servicio.detalletipomantenimiento_set.all()) +
            sum(i.subtotal for i in servicio.detalleinsumos_set.all())
        ),
    }

    html_string = render_to_string('detalle_servicio/factura_impresion.html', context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Factura_{pk}.pdf"'

    pisa_status = pisa.CreatePDF(html_string, dest=response)

    if pisa_status.err:
        return HttpResponse('Ocurrió un error al generar el PDF', status=500)

    return response