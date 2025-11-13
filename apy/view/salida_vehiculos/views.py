from django.shortcuts import render, redirect
from apy.models import *
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from apy.forms import *
from django.contrib import messages
# Se elimina la importación local de AccessMixin
from apy.decorators import PermisoRequeridoMixin # <-- Se mantiene solo la importación

# --------------Vistas de Salida de Vehículos---------------

class SalidaVehiculoListView(PermisoRequeridoMixin, ListView): 
    model = SalidaVehiculo
    template_name = 'salida_vehiculos/listar_salida_vehiculos.html'

    # --- Configuración de Permisos ---
    module_name = 'Salida Vehiculo' 
    permission_required = 'view'
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        nombre = {'nombre' : 'Salida de Vehiculos'}
        return JsonResponse(nombre)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Salida de Vehiculos'
        context['crear_url'] = reverse_lazy('apy:salida_vehiculo_crear')
        context['entidad'] = 'Salida de Vehiculos' 
        return context

class SalidaVehiculoCreateView(PermisoRequeridoMixin, CreateView): 
    model = SalidaVehiculo
    form_class = SalidaVehiculoForm
    template_name = 'salida_vehiculos/crear_salida_vehiculos.html'
    success_url = reverse_lazy('apy:salida_vehiculo_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'Salida Vehiculo'
    permission_required = 'add'

    def form_valid(self, form):
        messages.success(self.request, "Salida de Vehiculo creada correctamente")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear de Salida de Vehiculos'
        context['entidad'] = 'Salida de Vehiculos' 
        context['listar_url'] = reverse_lazy('apy:salida_vehiculo_lista')
        return context

class SalidaVehiculoUpdateView(PermisoRequeridoMixin, UpdateView): 
    model = SalidaVehiculo
    form_class = SalidaVehiculoForm
    template_name = 'salida_vehiculos/crear_salida_vehiculos.html'
    success_url = reverse_lazy('apy:salida_vehiculo_lista')

    # --- Configuración de Permisos ---
    module_name = 'Salida Vehiculo'
    permission_required = 'change'

    def form_valid(self, form):
        messages.success(self.request, "Salida de Vehiculo actualizada correctamente")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar de Salida de Vehiculos'
        context['entidad'] = 'Salida de Vehiculos'
        context['listar_url'] = reverse_lazy('apy:salida_vehiculo_lista')
        return context

class SalidaVehiculoDeleteView(PermisoRequeridoMixin, DeleteView): 
    model = SalidaVehiculo
    template_name = 'salida_vehiculos/eliminar_salida_vehiculos.html'
    success_url = reverse_lazy('apy:salida_vehiculo_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'Salida Vehiculo'
    permission_required = 'delete'
    
    def form_valid(self, form):
        messages.success(self.request, "Salida de Vehiculo eliminada correctamente")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar de Salida de Vehiculos'
        context['entidad'] = 'Salida de Vehiculos' 
        context['listar_url'] = reverse_lazy('apy:salida_vehiculo_lista')
        return context