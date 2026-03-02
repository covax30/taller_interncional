# ============================================================
# apy/view/pagos/views.py
# ============================================================

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.db import transaction
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# ⚠️ Se eliminó: from urllib3 import request
# Esa línea pisaba el objeto request de Django y causaba el TypeError

from apy.decorators import PermisoRequeridoMixin
from apy.models import Pagos, DetallePago, Repuesto, Insumos, Herramienta
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


# ─────────────────────────────────────────────────────────────
# CREAR
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
        })
        return context

    @transaction.atomic
    def form_valid(self, form):
        rep_fs, ins_fs, her_fs = _build_formsets(self.request)

        if rep_fs.is_valid() and ins_fs.is_valid() and her_fs.is_valid():
            self.object = form.save()

            rep_fs.instance = self.object
            ins_fs.instance = self.object
            her_fs.instance = self.object

            rep_fs.save()
            ins_fs.save()
            her_fs.save()

            self.object.recalcular_total()

            # Notificar stock bajo (método de la misma clase)
            self._notificar_stock_bajo()

            messages.success(self.request, 'Pago registrado correctamente.')
            return redirect(self.success_url)
        else:
            print("Errores repuesto_formset:",    rep_fs.errors)
            print("Errores insumo_formset:",      ins_fs.errors)
            print("Errores herramienta_formset:", her_fs.errors)
            messages.error(self.request, 'Corrige los errores en el formulario.')
            return self.render_to_response(self.get_context_data(form=form))

    # ─── Método hermano de form_valid, DENTRO de PagosCreateView ───
    def _notificar_stock_bajo(self):
        """
        Recorre los ítems del pago guardado y emite warnings
        para los que queden con stock por debajo del mínimo.
        """
        for detalle in self.object.detalles.all():
            if detalle.tipo_item == 'Repuesto' and detalle.repuesto:
                item = detalle.repuesto
                if item.stock_bajo:
                    messages.warning(
                        self.request,
                        f'⚠️ Repuesto "{item.nombre}": stock actual {item.stock} unidades '
                        f'(mínimo recomendado: {item.stock_minimo}).'
                    )
            elif detalle.tipo_item == 'Insumo' and detalle.insumo:
                item = detalle.insumo
                if item.stock_bajo:
                    messages.warning(
                        self.request,
                        f'⚠️ Insumo "{item.nombre}": stock actual {item.stock} unidades '
                        f'(mínimo recomendado: {item.stock_minimo}).'
                    )
            elif detalle.tipo_item == 'Herramienta' and detalle.herramienta:
                item = detalle.herramienta
                if item.stock_bajo:
                    messages.warning(
                        self.request,
                        f'⚠️ Herramienta "{item.nombre}": stock actual {item.stock} unidades '
                        f'(mínimo recomendado: {item.stock_minimo}).'
                    )


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