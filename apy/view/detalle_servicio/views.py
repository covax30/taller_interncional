from builtins import sum, super
from email.message import EmailMessage

from multiprocessing import context
import io
from io import BytesIO
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
from django.conf import settings
# Librería para el PDF
from xhtml2pdf import pisa

# Modelos y Formularios
from apy.models import (
    DetalleServicio,
    Empresa,
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
# ─────────────────────────────────────────────────────────────
# LISTAR SERVICIOS (Vista Única - Historial Completo)
# ─────────────────────────────────────────────────────────────

# ─────────────────────────────────────────────────────────────
# CREAR SERVICIO
# ─────────────────────────────────────────────────────────────
class CreateServicioView(PermisoRequeridoMixin, CreateView):
    module_name = 'DetalleServicio'
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

        # Datos para los selectores en el template
        context['repuestos']           = Repuesto.objects.filter(estado=True)
        context['tipos_mantenimiento'] = TipoMantenimiento.objects.filter(estado=True)
        context['insumos']             = Insumos.objects.filter(estado=True)
        context['perfiles']            = Profile.objects.select_related('user').filter(user__is_active=True)
        
        # Información del usuario actual para el frontend
        try:
            perfil_actual = Profile.objects.get(user=self.request.user)
            context['perfil_actual_id'] = perfil_actual.pk
            context['perfil_actual_nombre'] = self.request.user.get_full_name() or self.request.user.username
        except Profile.DoesNotExist:
            context['perfil_actual_id'] = None

        

        try:
            empresa_default = Empresa.objects.filter(estado=True).first()
            context['empresa_default_id'] = empresa_default.pk if empresa_default else None
        except:
            context['empresa_default_id'] = None
        return context        

    @transaction.atomic
    def form_valid(self, form):
        instance = form.save(commit=False)
        
        # 1. Forzar que todo servicio nuevo inicie "en proceso"
        instance.proceso = 'proceso'
        instance.estado = True
        
        # 2. Asignación automática de Empleado y Empresa
        try:
            instance.empleado = Profile.objects.get(user=self.request.user)
        except Profile.DoesNotExist:
            pass
            
        try:
            from apy.models import Empresa
            instance.empresa = Empresa.objects.filter(estado=True).first()
        except:
            pass
        
        # Guardamos la instancia principal para tener ID
        instance.save()

        # 3. Procesar Formsets
        repuesto_formset      = DetalleRepuestoFormSet(self.request.POST, prefix='repuestos')
        mantenimiento_formset = DetalleTipoMantenimientoFormSet(self.request.POST, prefix='mantenimientos')
        insumo_formset        = DetalleInsumosFormSet(self.request.POST, prefix='insumos')

        if repuesto_formset.is_valid() and mantenimiento_formset.is_valid() and insumo_formset.is_valid():
            
            # Validación de Stock (opcional, según tu lógica de _validar_stock_suficiente)
            # Si tienes el método definido en la clase, llámalo aquí.

            repuesto_formset.instance      = instance
            mantenimiento_formset.instance = instance
            insumo_formset.instance        = instance

            repuesto_formset.save()
            mantenimiento_formset.save()
            insumo_formset.save()

            messages.success(self.request, f'Servicio #{instance.id} creado correctamente.')
            return redirect(self.success_url)
        else:
            # Si los formsets fallan, borramos la instancia para no dejar datos huérfanos
            instance.delete() 
            messages.error(self.request, 'Error en los detalles del servicio. Verifique cantidades y stock.')
            return self.render_to_response(self.get_context_data(form=form))
        
class ListServicioView(PermisoRequeridoMixin, ListView):
    module_name = 'DetalleServicio'
    permission_required = 'view'
    model = DetalleServicio
    template_name = 'detalle_servicio/lista_servicios.html'
    context_object_name = 'servicios'
    ordering = ['-fecha_creacion']

    def get_queryset(self):
        # Mostramos TODO. Ya no filtramos por estado=True para no ocultar nada.
        return DetalleServicio.objects.all().select_related(
            'id_vehiculo', 
            'id_vehiculo__id_cliente'
        ).order_by('-fecha_creacion')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Estadísticas para tus tarjetas informativas
        queryset_base = DetalleServicio.objects.all()
        context['total_servicios'] = queryset_base.count()
        context['servicios_en_proceso'] = queryset_base.filter(proceso='proceso').count()
        context['servicios_terminados'] = queryset_base.filter(proceso='terminado').count()
        return context


# ─────────────────────────────────────────────────────────────
# ELIMINAR SERVICIO (Borrado físico condicional)
# ─────────────────────────────────────────────────────────────
class DeleteServicioView(PermisoRequeridoMixin, DeleteView):
    module_name = 'DetalleServicio'
    permission_required = 'delete'
    model = DetalleServicio
    template_name = 'detalle_servicio/eliminar_servicio.html'
    success_url = reverse_lazy('apy:lista_servicios')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        # LÓGICA: Solo borramos de la BD si el trabajo NO ha terminado.
        if self.object.proceso != 'terminado':
            id_servicio = self.object.id
            self.object.delete()
            messages.success(
                request, 
                f'Servicio #{id_servicio} eliminado correctamente de la base de datos.'
            )
        else:
            # Bloqueo de seguridad para registros terminados (facturas)
            messages.error(
                request, 
                f'No se puede eliminar el Servicio #{self.object.id} porque ya está finalizado/facturado.'
            )

        return HttpResponseRedirect(self.get_success_url())


# ─────────────────────────────────────────────────────────────
# IMPRIMIR FACTURA (Validación al inicio)
# ─────────────────────────────────────────────────────────────
def imprimir_servicio_factura(request, pk):
    servicio = get_object_or_404(DetalleServicio, pk=pk)

    # Validamos primero: Solo se imprime lo que ya se terminó
    if servicio.proceso != 'terminado':
        messages.error(request, '❌ No se puede imprimir la factura de un servicio que sigue en proceso.')
        return redirect('apy:lista_servicios')

    # Si pasa la validación, generamos el PDF
    context = {
        'servicio': servicio,
        'vehiculo': servicio.id_vehiculo,
        'cliente': servicio.id_vehiculo.id_cliente,
        'repuestos': servicio.detallerepuesto_set.all(),
        'mantenimientos': servicio.detalletipomantenimiento_set.all(),
        'insumos': servicio.detalleinsumos_set.all(),
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

# ─────────────────────────────────────────────────────────────
# EDITAR SERVICIO (Con bloqueo por finalización)
# ─────────────────────────────────────────────────────────────
class UpdateServicioView(PermisoRequeridoMixin, UpdateView):
    module_name = 'Factura'
    permission_required = 'change'
    model = DetalleServicio
    form_class = DetalleServicioForm
    template_name = 'detalle_servicio/crear_servicio.html'
    success_url = reverse_lazy('apy:lista_servicios')

    def dispatch(self, request, *args, **kwargs):
        """Validar antes de entrar a la vista si el servicio permite edición"""
        obj = self.get_object()
        if obj.proceso == 'terminado':
            messages.error(request, f'El Servicio #{obj.id} está TERMINADO y no puede ser modificado.')
            return redirect('apy:lista_servicios')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['repuesto_formset']      = DetalleRepuestoFormSet(self.request.POST, instance=self.object, prefix='repuestos')
            context['mantenimiento_formset'] = DetalleTipoMantenimientoFormSet(self.request.POST, instance=self.object, prefix='mantenimientos')
            context['insumo_formset']        = DetalleInsumosFormSet(self.request.POST, instance=self.object, prefix='insumos')
        else:
            context['repuesto_formset']      = DetalleRepuestoFormSet(instance=self.object, prefix='repuestos')
            context['repuesto_formset'].extra = 0
            context['mantenimiento_formset'] = DetalleTipoMantenimientoFormSet(instance=self.object, prefix='mantenimientos')
            context['mantenimiento_formset'].extra = 0
            context['insumo_formset']        = DetalleInsumosFormSet(instance=self.object, prefix='insumos')
            context['insumo_formset'].extra = 0

        # Datos para los selects del frontend
        context['repuestos']           = Repuesto.objects.filter(estado=True)
        context['tipos_mantenimiento'] = TipoMantenimiento.objects.filter(estado=True)
        context['insumos']             = Insumos.objects.filter(estado=True)
        context['perfiles']            = Profile.objects.select_related('user').filter(user__is_active=True)
        context['modo_edicion']        = True
        return context

    @transaction.atomic
    def form_valid(self, form):
        # Cargamos los formsets con la instancia actual
        repuesto_formset      = DetalleRepuestoFormSet(self.request.POST, instance=self.object, prefix='repuestos')
        mantenimiento_formset = DetalleTipoMantenimientoFormSet(self.request.POST, instance=self.object, prefix='mantenimientos')
        insumo_formset        = DetalleInsumosFormSet(self.request.POST, instance=self.object, prefix='insumos')

        if repuesto_formset.is_valid() and mantenimiento_formset.is_valid() and insumo_formset.is_valid():
            # Guardamos el servicio principal
            self.object = form.save()

            # Guardamos los detalles
            repuesto_formset.save()
            mantenimiento_formset.save()
            insumo_formset.save()

            # Mensaje de éxito con placa del vehículo
            try:
                self.object.refresh_from_db()
                placa = self.object.id_vehiculo.placa
            except:
                placa = "N/A"

            messages.success(
                self.request, 
                f'Servicio #{self.object.id} (Vehículo {placa}) actualizado correctamente.'
            )
            return redirect(self.success_url)
        else:
            messages.error(self.request, 'Error al actualizar los detalles del servicio. Revisa los datos.')
            return self.render_to_response(self.get_context_data(form=form))
        
        # ─────────────────────────────────────────────────────────────
# DETALLE / VER SERVICIO (Optimizado con prefetch_related)
# ─────────────────────────────────────────────────────────────
class DetalleServicioView(PermisoRequeridoMixin, DetailView):
    module_name = 'Factura'
    permission_required = 'view'
    model = DetalleServicio
    template_name = 'detalle_servicio/detalle_servicio.html'
    context_object_name = 'servicio'

    def get_queryset(self):
        """
        Optimizamos la consulta para traer los datos de las tablas relacionadas
        evitando el error de 'N+1 queries'.
        """
        return DetalleServicio.objects.prefetch_related(
            'detallerepuesto_set__id_repuesto',
            'detalletipomantenimiento_set__id_tipo_mantenimiento',
            'detalleinsumos_set__id_insumos__id_marca',  # Traemos hasta la marca del insumo
        ).select_related(
            'id_vehiculo__id_cliente',  # Traemos vehículo y cliente de un solo golpe
            'empleado__user',           # Traemos los datos del mecánico/empleado
            'empresa'
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        servicio = self.get_object()

        # Agrupamos los totales para mostrarlos fácilmente en el template
        context.update({
            'repuestos':      servicio.detallerepuesto_set.all(),
            'mantenimientos': servicio.detalletipomantenimiento_set.all(),
            'insumos':        servicio.detalleinsumos_set.all(),
            # Puedes calcular el subtotal aquí o usar el método que tengas en el modelo
            'total_items': (
                servicio.detallerepuesto_set.count() + 
                servicio.detalletipomantenimiento_set.count() + 
                servicio.detalleinsumos_set.count()
            )
        })
        return context