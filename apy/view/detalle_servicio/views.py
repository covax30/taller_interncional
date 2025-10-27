from django.views.generic import CreateView, UpdateView, ListView, DeleteView, DetailView  # <- Agregar DetailView aquí
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.db import transaction
from django.contrib import messages
from django.http import JsonResponse
from apy.models import DetalleServicio
from apy.forms import (
    DetalleServicioForm, 
    DetalleRepuestoFormSet, 
    DetalleTipoMantenimientoFormSet, 
    DetalleInsumosFormSet
)

class ListaServiciosView(ListView):
    model = DetalleServicio
    template_name = 'detalle_servicio/lista_servicios.html'
    context_object_name = 'servicios'
    ordering = ['-fecha_creacion']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Agregar estadísticas rápidas
        context['total_servicios'] = DetalleServicio.objects.count()
        context['servicios_pendientes'] = DetalleServicio.objects.filter(estado='pendiente').count()
        return context

class CrearServicioView(CreateView):
    model = DetalleServicio
    form_class = DetalleServicioForm
    template_name = 'detalle_servicio/crear_servicio.html'
    success_url = reverse_lazy('lista_servicios')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['repuesto_formset'] = DetalleRepuestoFormSet(self.request.POST, prefix='repuestos')
            context['mantenimiento_formset'] = DetalleTipoMantenimientoFormSet(self.request.POST, prefix='mantenimientos')
            context['insumo_formset'] = DetalleInsumosFormSet(self.request.POST, prefix='insumos')
        else:
            context['repuesto_formset'] = DetalleRepuestoFormSet(prefix='repuestos')
            context['mantenimiento_formset'] = DetalleTipoMantenimientoFormSet(prefix='mantenimientos')
            context['insumo_formset'] = DetalleInsumosFormSet(prefix='insumos')
        return context

    @transaction.atomic
    def form_valid(self, form):
        context = self.get_context_data()
        repuesto_formset = context['repuesto_formset']
        mantenimiento_formset = context['mantenimiento_formset']
        insumo_formset = context['insumo_formset']
        
        if (repuesto_formset.is_valid() and 
            mantenimiento_formset.is_valid() and 
            insumo_formset.is_valid()):
            
            self.object = form.save()
            repuesto_formset.instance = self.object
            repuesto_formset.save()
            
            mantenimiento_formset.instance = self.object
            mantenimiento_formset.save()
            
            insumo_formset.instance = self.object
            insumo_formset.save()
            
            messages.success(self.request, 'Servicio creado exitosamente!')
            return redirect(self.success_url)
        else:
            messages.error(self.request, 'Por favor corrige los errores en el formulario.')
            return self.render_to_response(self.get_context_data(form=form))

class EditarServicioView(UpdateView):
    model = DetalleServicio
    form_class = DetalleServicioForm
    template_name = 'detalle_servicio/editar_servicio.html'
    success_url = reverse_lazy('lista_servicios')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['repuesto_formset'] = DetalleRepuestoFormSet(
                self.request.POST, instance=self.object, prefix='repuestos'
            )
            context['mantenimiento_formset'] = DetalleTipoMantenimientoFormSet(
                self.request.POST, instance=self.object, prefix='mantenimientos'
            )
            context['insumo_formset'] = DetalleInsumosFormSet(
                self.request.POST, instance=self.object, prefix='insumos'
            )
        else:
            context['repuesto_formset'] = DetalleRepuestoFormSet(
                instance=self.object, prefix='repuestos'
            )
            context['mantenimiento_formset'] = DetalleTipoMantenimientoFormSet(
                instance=self.object, prefix='mantenimientos'
            )
            context['insumo_formset'] = DetalleInsumosFormSet(
                instance=self.object, prefix='insumos'
            )
        
        # Agregar totales para mostrar en el template
        context['subtotal'] = self.object.subtotal
        return context

    @transaction.atomic
    def form_valid(self, form):
        context = self.get_context_data()
        repuesto_formset = context['repuesto_formset']
        mantenimiento_formset = context['mantenimiento_formset']
        insumo_formset = context['insumo_formset']
        
        if (repuesto_formset.is_valid() and 
            mantenimiento_formset.is_valid() and 
            insumo_formset.is_valid()):
            
            self.object = form.save()
            repuesto_formset.instance = self.object
            repuesto_formset.save()
            
            mantenimiento_formset.instance = self.object
            mantenimiento_formset.save()
            
            insumo_formset.instance = self.object
            insumo_formset.save()
            
            messages.success(self.request, 'Servicio actualizado exitosamente!')
            return redirect(self.success_url)
        else:
            messages.error(self.request, 'Por favor corrige los errores en el formulario.')
            return self.render_to_response(self.get_context_data(form=form))

class EliminarServicioView(DeleteView):
    model = DetalleServicio
    template_name = 'detalle_servicio/eliminar_servicio.html'
    success_url = reverse_lazy('lista_servicios')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Servicio eliminado exitosamente!')
        return super().delete(request, *args, **kwargs)

# Vista para detalles del servicio - AHORA CORREGIDA
class DetalleServicioView(DetailView):
    model = DetalleServicio
    template_name = 'detalle_servicio/detalle_servicio.html'
    context_object_name = 'servicio'

    def get_queryset(self):
        """Optimización: precargar relaciones para evitar consultas N+1"""
        return DetalleServicio.objects.prefetch_related(
            'detallerepuesto_set__id_repuesto',
            'detalletipomantenimiento_set__id_tipo_mantenimiento', 
            'detalleinsumos_set__id_insumos__id_marca',
            'id_vehiculo__id_cliente'
        ).select_related('id_vehiculo')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        servicio = self.get_object()
        
        # Los datos ya vienen precargados gracias al get_queryset
        context.update({
            'repuestos': servicio.detallerepuesto_set.all(),
            'mantenimientos': servicio.detalletipomantenimiento_set.all(),
            'insumos': servicio.detalleinsumos_set.all(),
            'subtotal': servicio.subtotal,
            # Las propiedades total_repuestos, total_mantenimientos, total_insumos
            # ahora están disponibles directamente del modelo
        })
        
        return context