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
from apy.decorators import PermisoRequeridoMixin # Usando el Mixin centralizado

# --------------Vistas de Entrada de Vehículos---------------

class EntradaVehiculoListView(PermisoRequeridoMixin, ListView):
    model = EntradaVehiculo
    template_name = 'entrada_vehiculos/listar_entrada_vehiculos.html'

    # --- Configuración de Permisos ---
    module_name = 'Entrada Vehiculo' 
    permission_required = 'view'
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        nombre = {'nombre' : 'Entrada de Vehiculos'}
        return JsonResponse(nombre)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Entrada de Vehiculos'
        context['crear_url'] = reverse_lazy('apy:entrada_vehiculo_crear')
        context['entidad'] = 'Entrada de Vehiculos'
        return context

class EntradaVehiculoCreateView(PermisoRequeridoMixin, CreateView): 
    model = EntradaVehiculo
    form_class = EntradaVehiculoForm
    template_name = 'entrada_vehiculos/crear_entrada_vehiculos.html'
    success_url = reverse_lazy('apy:entrada_vehiculo_lista')

    # --- Configuración de Permisos ---
    module_name = 'Entrada Vehiculo'
    permission_required = 'add'

    def form_valid(self, form):
        messages.success(self.request, "Entrada de Vehiculo creada correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear de Entrada de Vehiculos'
        context['entidad'] = 'Entrada de Vehiculos'
        context['listar_url'] = reverse_lazy('apy:entrada_vehiculo_lista')
        return context

class EntradaVehiculoUpdateView(PermisoRequeridoMixin, UpdateView):
    model = EntradaVehiculo
    form_class = EntradaVehiculoForm
    template_name = 'entrada_vehiculos/crear_entrada_vehiculos.html'
    success_url = reverse_lazy('apy:entrada_vehiculo_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'Entrada Vehiculo'
    permission_required = 'change'
    
    def form_valid(self, form):
        messages.success(self.request, "Entrada de Vehiculo actualizada correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar de Entrada de Vehiculos'
        context['entidad'] = 'Entrada de Vehiculos' 
        context['listar_url'] = reverse_lazy('apy:entrada_vehiculo_lista')
        return context

class EntradaVehiculoDeleteView(PermisoRequeridoMixin, DeleteView): 
    model = EntradaVehiculo
    template_name = 'entrada_vehiculos/eliminar_entrada_vehiculos.html'
    success_url = reverse_lazy('apy:entrada_vehiculo_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'Entrada Vehiculo'
    permission_required = 'delete'
    
    def form_valid(self, form):
        messages.success(self.request, "Entrada de Vehiculo eliminada correctamente")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar de Entrada de Vehiculos'
        context['entidad'] = 'Entrada de Vehiculos'
        context['listar_url'] = reverse_lazy('apy:entrada_vehiculo_lista')
        return context