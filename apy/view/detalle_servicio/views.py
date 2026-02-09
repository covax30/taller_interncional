from django.views.generic import CreateView, UpdateView, ListView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.db import transaction
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse


from apy.models import (
    DetalleServicio,      
    Repuesto,              
    TipoMantenimiento,    
    Insumos,              
    Vehiculo              
)

from apy.forms import (
    DetalleServicioForm, 
    DetalleRepuestoFormSet, 
    DetalleTipoMantenimientoFormSet, 
    DetalleInsumosFormSet
)

class ListServicioView(ListView):
    model = DetalleServicio
    template_name = 'detalle_servicio/lista_servicios.html'
    context_object_name = 'servicios'
    ordering = ['-fecha_creacion']
    
    def get_queryset(self):
        return DetalleServicio.objects.filter(estado=True)

    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_servicios'] = DetalleServicio.objects.count() 
        context['servicios_activos'] = DetalleServicio.objects.filter(estado=True).count()

        return context
    
#---- vista para listar servicios inactivos -----
class ServicioInactivosListView(ListView):
    model = DetalleServicio
    template_name = 'detalle_servicio/modal_inactivos.html'
    context_object_name = 'servicios_inactivos'
    
    def get_queryset(self):
        return DetalleServicio.objects.filter(estado=False) 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_servicios'] = DetalleServicio.objects.count() 
        context['servicios_activos'] = DetalleServicio.objects.filter(estado=True).count()

        return context    

class CreateServicioView(CreateView):
    model = DetalleServicio
    form_class = DetalleServicioForm
    template_name = 'detalle_servicio/crear_servicio.html'
    success_url = reverse_lazy('apy:lista_servicios')

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
        
        context['repuestos'] = Repuesto.objects.all()
        context['tipos_mantenimiento'] = TipoMantenimiento.objects.all()
        context['insumos'] = Insumos.objects.all()  
        
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
            return redirect('/apy/servicios/')
        else:
            print("Errores en repuesto_formset:", repuesto_formset.errors)
            print("Errores en mantenimiento_formset:", mantenimiento_formset.errors)
            print("Errores en insumo_formset:", insumo_formset.errors)
            
            form.instance.estado = True 
            messages.error(self.request, 'Por favor corrige los errores en el formulario.')
            return self.render_to_response(self.get_context_data(form=form))

class UpdateServicioView(UpdateView):
    model = DetalleServicio
    form_class = DetalleServicioForm
    template_name = 'detalle_servicio/crear_servicio.html'
    success_url = reverse_lazy('apy:lista_servicios')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.POST:
            # Si el formulario fue enviado (POST), usamos los datos del POST
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
            # Si solo se carga la página (GET), cargamos los datos existentes
            context['repuesto_formset'] = DetalleRepuestoFormSet(
                instance=self.object, prefix='repuestos'
            )
            context['repuesto_formset'].extra = 0  # No mostrar formularios vacíos al editar

            context['mantenimiento_formset'] = DetalleTipoMantenimientoFormSet(
                instance=self.object, prefix='mantenimientos'
            )
            context['mantenimiento_formset'].extra = 0

            context['insumo_formset'] = DetalleInsumosFormSet(
                instance=self.object, prefix='insumos'
            )
            context['insumo_formset'].extra = 0

        # Agregamos listas auxiliares para los selects o datos del template
        context['repuestos'] = Repuesto.objects.all()
        context['tipos_mantenimiento'] = TipoMantenimiento.objects.all()
        context['insumos'] = Insumos.objects.all()

        # Bandera para el template (por si deseas diferenciar entre crear y editar)
        context['modo_edicion'] = True  

        return context

    @transaction.atomic
    def form_valid(self, form):
        context = self.get_context_data()
        repuesto_formset = context['repuesto_formset']
        mantenimiento_formset = context['mantenimiento_formset']
        insumo_formset = context['insumo_formset']

        # Validamos todos los formsets antes de guardar
        if repuesto_formset.is_valid() and mantenimiento_formset.is_valid() and insumo_formset.is_valid():
            self.object = form.save()

            # Guardamos los formsets relacionados
            repuesto_formset.instance = self.object
            repuesto_formset.save()

            mantenimiento_formset.instance = self.object
            mantenimiento_formset.save()

            insumo_formset.instance = self.object
            insumo_formset.save()

            messages.success(self.request, '¡Servicio actualizado exitosamente!')
            return super().form_valid(form)
        else:
            messages.error(self.request, 'Corrige los errores antes de guardar.')
            return self.render_to_response(self.get_context_data(form=form))

class DeleteServicioView(DeleteView):
    model = DetalleServicio
    template_name = 'detalle_servicio/eliminar_servicio.html'
    success_url = reverse_lazy('apy:lista_servicios')  # cambia por tu URL real

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.estado = False
        self.object.save()
        messages.success(self.request, f"Servicio {self.object.id} desactivado correctamente")

        return HttpResponseRedirect(self.get_success_url())
    
#---- vista para activar servicio -----
class ServicioActivateView(DeleteView):
    model = DetalleServicio
    template_name = 'detalle_servicio/activar_servicio.html'
    success_url = reverse_lazy('apy:lista_servicios')  # cambia por tu URL real

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.estado = True
        self.object.save()
        messages.success(self.request, f"Servicio {self.object.id} activado correctamente")

        return HttpResponseRedirect(self.get_success_url())    

class DetalleServicioView(DetailView):
    model = DetalleServicio
    template_name = 'detalle_servicio/detalle_servicio.html'
    context_object_name = 'servicio'

    def get_queryset(self):
        return DetalleServicio.objects.prefetch_related(
            'detallerepuesto_set__id_repuesto',
            'detalletipomantenimiento_set__id_tipo_mantenimiento', 
            'detalleinsumos_set__id_insumos__id_marca',
            'vehiculo__id_cliente'
        ).select_related('vehiculo')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        servicio = self.get_object()
        
        context.update({
            'repuestos': servicio.detallerepuesto_set.all(),
            'mantenimientos': servicio.detalletipomantenimiento_set.all(),
            'insumos': servicio.detalleinsumos_set.all(),
            'subtotal': servicio.subtotal,
        })
        
        return context