from django.shortcuts import render, redirect
from apy.models import * # Asegúrate de que PagoServiciosPublicos, Module, y Permission sean importados
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from apy.forms import *
from django.contrib import messages
# Se elimina la importación de AccessMixin ya que no se usa localmente.

# Importar el Mixin Corregido (que lanza 403)
from apy.decorators import PermisoRequeridoMixin 

# --------------Vistas de pago servicios publicos---------------

class PagoServiciosListView(PermisoRequeridoMixin, ListView): 
    model = PagoServiciosPublicos
    template_name ='Pago_Servicios/listar_pagoservicios.html'
    
    # --- Configuración de Permisos ---
    module_name = 'PagoServicios' 
    permission_required = 'view' 
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        # Usa el Mixin importado de apy.decorators
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        nombre = {'nombre' : 'pago servicios'}
        return JsonResponse(nombre)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Pago Servicios Publicos'
        context['crear_url'] = reverse_lazy('apy:pago_servicios_crear')
        context['entidad'] = 'PagoServiciosPublicos'
        return context
    
class PagoServiciosCreateView(PermisoRequeridoMixin, CreateView): 
    model = PagoServiciosPublicos
    form_class = PagoServiciosForm
    template_name = 'Pago_Servicios/crear_pagoservicios.html'
    success_url = reverse_lazy('apy:pago_servicios_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'PagoServicios'
    permission_required = 'add'
    
    def form_valid(self, form):
        messages.success(self.request, "Pago de servicio creado correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context ['titulo'] = 'Crear Pago Servicios Publicos'
        context ['entidad'] = 'PagoServiciosPublicos'
        context ['listar_url'] = reverse_lazy('apy:pago_servicios_lista')
        return context
    
class PagoServiciosUpdateView(PermisoRequeridoMixin, UpdateView):
    model = PagoServiciosPublicos
    form_class = PagoServiciosForm
    template_name = 'Pago_Servicios/crear_pagoservicios.html'
    success_url = reverse_lazy('apy:pago_servicios_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'PagoServicios'
    permission_required = 'change'
    
    def form_valid(self, form):
        messages.success(self.request, "Pago de servicio actualizado correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Pago Servicios Publicos'
        context['entidad'] = 'PagoServiciosPublicos'
        context['listar_url'] = reverse_lazy('apy:pago_servicios_lista')
        return context

class PagoServiciosDeleteView(PermisoRequeridoMixin, DeleteView): 
    model = PagoServiciosPublicos
    template_name = 'Pago_Servicios/eliminar_pagoservicios.html'
    success_url = reverse_lazy('apy:pago_servicios_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'PagoServicios'
    permission_required = 'delete'
    
    def form_valid(self, form):
        # Esta es la implementación estándar para agregar un mensaje en DeleteView.
        # No se necesita el argumento 'request' en form_valid de DeleteView.
        messages.success(self.request, "Pago de servicio eliminado correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Pago Servicios Publicos'
        context['entidad'] = 'PagoServiciosPublicos'
        context['listar_url'] = reverse_lazy('apy:pago_servicios_lista')
        return context