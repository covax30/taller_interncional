# ============================================================
# apy/view/pagos/views.py
# ============================================================

from builtins import dict, float, print, super
from django.utils import timezone  # ← CORREGIDO (antes era from datetime import timezone)

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.db import transaction
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from apy.decorators import PermisoRequeridoMixin
from apy.models import Gastos, Pagos, DetallePago, Repuesto, Insumos, Herramienta
from apy.forms import (
    PagoForm,
    DetallePagoRepuestoFormSet,
    DetallePagoInsumoFormSet,
    DetallePagoHerramientaFormSet,
)


# ─────────────────────────────────────────────────────────────
# Helper: construye los tres formsets según GET o POST
# ─────────────────────────────────────────────────────────────
def _build_formsets(request, instance=None):
    kwargs_rep = {'prefix': 'repuestos'}
    kwargs_ins = {'prefix': 'insumos'}
    kwargs_her = {'prefix': 'herramientas'}

    if instance:
        kwargs_rep['instance'] = instance
        kwargs_ins['instance'] = instance
        kwargs_her['instance'] = instance

        if request.POST:
            return (
                DetallePagoRepuestoFormSet(request.POST, **kwargs_rep),
                DetallePagoInsumoFormSet(request.POST, **kwargs_ins),
                DetallePagoHerramientaFormSet(request.POST, **kwargs_her),
            )
        else:
            rep_fs = DetallePagoRepuestoFormSet(**kwargs_rep)
            ins_fs = DetallePagoInsumoFormSet(**kwargs_ins)
            her_fs = DetallePagoHerramientaFormSet(**kwargs_her)
            rep_fs.extra = 0
            ins_fs.extra = 0
            her_fs.extra = 0
            return rep_fs, ins_fs, her_fs
    else:
        if request.POST:
            return (
                DetallePagoRepuestoFormSet(request.POST, **kwargs_rep),
                DetallePagoInsumoFormSet(request.POST, **kwargs_ins),
                DetallePagoHerramientaFormSet(request.POST, **kwargs_her),
            )
        return (
            DetallePagoRepuestoFormSet(**kwargs_rep),
            DetallePagoInsumoFormSet(**kwargs_ins),
            DetallePagoHerramientaFormSet(**kwargs_her),
        )


# ─────────────────────────────────────────────────────────────
# LISTAR
# ─────────────────────────────────────────────────────────────
class PagosListView(PermisoRequeridoMixin, ListView):
    model               = Pagos
    template_name       = 'Pagos/listar_pago.html'
    module_name         = 'Pagos'
    permission_required = 'view'

    def get_queryset(self):
        return Pagos.objects.filter(estado=True).prefetch_related('detalles')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo']    = 'Lista de Pagos'
        context['crear_url'] = reverse_lazy('apy:pagos_crear')
        context['entidad']   = 'Pagos'
        return context


class PagosInactivosListView(PermisoRequeridoMixin, ListView):
    model               = Pagos
    template_name       = 'Pagos/pago_inactivos.html'
    module_name         = 'Pagos'
    permission_required = 'view'

    def get_queryset(self):
        return Pagos.objects.filter(estado=False).prefetch_related('detalles')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo']    = 'Lista de Pagos Inactivos'
        context['crear_url'] = reverse_lazy('apy:pagos_crear')
        context['entidad']   = 'Pagos'
        return context


# ─────────────────────────────────────────────────────────────
# CREAR  (una sola definición)
# ─────────────────────────────────────────────────────────────
class PagosCreateView(PermisoRequeridoMixin, CreateView):
    model               = Pagos
    form_class          = PagoForm
    template_name       = 'Pagos/crear_pago.html'
    success_url         = reverse_lazy('apy:pagos_lista')
    module_name         = 'Pagos'
    permission_required = 'add'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rep_fs, ins_fs, her_fs = _build_formsets(self.request)
        context.update({
            'repuesto_formset':    rep_fs,
            'insumo_formset':      ins_fs,
            'herramienta_formset': her_fs,
            'repuestos':           Repuesto.objects.filter(estado=True),
            'insumos':             Insumos.objects.filter(estado=True),
            'herramientas':        Herramienta.objects.filter(estado=True),
            'titulo':              'Crear Pago',
            'entidad':             'Pagos',
            'modo_edicion':        False,
        })
        return context

    def _notificar_stock_bajo(self):
        """
        Solo emite advertencias visuales.
        El signal sumar_stock_al_comprar en signals.py ya actualizó el stock.
        Esta función NO modifica stock.
        """
        for detalle in self.object.detalles.all():
            if detalle.tipo_item == 'Repuesto' and detalle.repuesto:
                item = detalle.repuesto
                item.refresh_from_db()
                if item.stock_bajo:
                    messages.warning(
                        self.request,
                        f'⚠️ Repuesto "{item.nombre}": stock actual {item.stock} uds '
                        f'(mínimo recomendado: {item.stock_minimo}).'
                    )

            elif detalle.tipo_item == 'Insumo' and detalle.insumo:
                item = detalle.insumo
                item.refresh_from_db()
                if item.stock_bajo:
                    messages.warning(
                        self.request,
                        f'⚠️ Insumo "{item.nombre}": stock actual {item.stock} '
                        f'(mínimo recomendado: {item.stock_minimo}).'
                    )

            elif detalle.tipo_item == 'Herramienta' and detalle.herramienta:
                item = detalle.herramienta
                item.refresh_from_db()
                if item.stock_bajo:
                    messages.warning(
                        self.request,
                        f'⚠️ Herramienta "{item.nombre}": stock actual {item.stock} uds '
                        f'(mínimo recomendado: {item.stock_minimo}).'
                    )

    @transaction.atomic
    def form_valid(self, form):
        rep_fs, ins_fs, her_fs = _build_formsets(self.request)

        if rep_fs.is_valid() and ins_fs.is_valid() and her_fs.is_valid():
            # 1. Guardar el pago principal (monto_total=0 todavía)
            self.object = form.save()

            # 2. Guardar los detalles (el signal suma el stock automáticamente)
            rep_fs.instance = self.object
            ins_fs.instance = self.object
            her_fs.instance = self.object
            rep_fs.save()
            ins_fs.save()
            her_fs.save()

            # 3. Recalcular total y sincronizar con Gastos/Caja
            self.object.recalcular_total()

            # 4. Notificar stock bajo (solo warnings, sin tocar stock)
            self._notificar_stock_bajo()

            messages.success(self.request, 'Pago registrado correctamente.')
            return redirect(self.success_url)
        else:
            print("=" * 50)
            print("ERRORES EN FORMSETS:")
            print("Repuesto:", rep_fs.errors if rep_fs.errors else "OK")
            print("Insumo:",   ins_fs.errors if ins_fs.errors else "OK")
            print("Herramienta:", her_fs.errors if her_fs.errors else "OK")
            print("=" * 50)
            messages.error(self.request, 'Corrige los errores en el formulario.')
            return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form):
        print("ERRORES FORM PRINCIPAL:", form.errors)
        messages.error(self.request, 'Por favor, corrige los errores en el formulario.')
        return super().form_invalid(form)


# ─────────────────────────────────────────────────────────────
# EDITAR
# ─────────────────────────────────────────────────────────────
class PagosUpdateView(PermisoRequeridoMixin, UpdateView):
    model               = Pagos
    form_class          = PagoForm
    template_name       = 'Pagos/crear_pago.html'
    success_url         = reverse_lazy('apy:pagos_lista')
    module_name         = 'Pagos'
    permission_required = 'change'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rep_fs, ins_fs, her_fs = _build_formsets(self.request, instance=self.object)
        context.update({
            'repuesto_formset':    rep_fs,
            'insumo_formset':      ins_fs,
            'herramienta_formset': her_fs,
            'repuestos':           Repuesto.objects.filter(estado=True),
            'insumos':             Insumos.objects.filter(estado=True),
            'herramientas':        Herramienta.objects.filter(estado=True),
            'titulo':              'Editar Pago',
            'entidad':             'Pagos',
            'listar_url':          reverse_lazy('apy:pagos_lista'),
            'modo_edicion':        True,
        })
        return context

    @transaction.atomic
    def form_valid(self, form):
        rep_fs, ins_fs, her_fs = _build_formsets(self.request, instance=self.object)

        if rep_fs.is_valid() and ins_fs.is_valid() and her_fs.is_valid():
            self.object = form.save()

            rep_fs.instance = self.object
            ins_fs.instance = self.object
            her_fs.instance = self.object
            rep_fs.save()
            ins_fs.save()
            her_fs.save()

            self.object.recalcular_total()

            messages.success(self.request, 'Pago actualizado correctamente.')
            return redirect(self.success_url)
        else:
            messages.error(self.request, 'Corrige los errores antes de guardar.')
            return self.render_to_response(self.get_context_data(form=form))

    def form_invalid(self, form):
        print("ERRORES FORM:", form.errors)
        return super().form_invalid(form)


# ─────────────────────────────────────────────────────────────
# ELIMINAR (lógico)
# ─────────────────────────────────────────────────────────────
class PagosDeleteView(PermisoRequeridoMixin, DeleteView):
    model               = Pagos
    template_name       = 'Pagos/eliminar_pago.html'
    success_url         = reverse_lazy('apy:pagos_lista')
    module_name         = 'Pagos'
    permission_required = 'delete'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.estado = False
        self.object.save()
        messages.success(request, f'Pago #{self.object.id_pago} desactivado correctamente.')
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo']     = 'Eliminar Pago'
        context['listar_url'] = reverse_lazy('apy:pagos_lista')
        return context


# ─────────────────────────────────────────────────────────────
# ACTIVAR
# ─────────────────────────────────────────────────────────────
class PagosActivateView(PermisoRequeridoMixin, DeleteView):
    model               = Pagos
    template_name       = 'Pagos/activar_pago.html'
    success_url         = reverse_lazy('apy:pagos_lista')
    module_name         = 'Pagos'
    permission_required = 'delete'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.estado = True
        self.object.save()
        messages.success(request, f'Pago #{self.object.id_pago} activado correctamente.')
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Activar Pago'
        return context