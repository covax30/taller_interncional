from django.shortcuts import render, redirect
from apy.models import * # Asegúrate de que Nomina, Module, y Permission sean importados
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from apy.forms import *
from django.contrib import messages
# Se elimina la importación de AccessMixin ya que no se usa localmente.
from apy.decorators import PermisoRequeridoMixin # <-- Se mantiene solo la importación


# --------------Vistas de Nómina---------------

class NominaListView(PermisoRequeridoMixin, ListView): 
    model = Nomina
    template_name = 'Nomina/listar_nomina.html'
    
    # --- Configuración de Permisos ---
    module_name = 'Nomina'
    permission_required = 'view'
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        # Usa el Mixin importado de apy.decorators
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        nombre = {'nombre' : 'Yury'}
        return JsonResponse(nombre)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista pago de Nomina'
        context['crear_url'] = reverse_lazy('apy:nomina_crear')
        context['entidad'] = 'Nomina'
        return context
    
class NominaCreateView(PermisoRequeridoMixin, CreateView): 
    model = Nomina
    form_class = NominaForm
    template_name = 'Nomina/crear_nomina.html'
    success_url = reverse_lazy('apy:nomina_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'Nomina'
    permission_required = 'add'
    
    def form_valid(self, form):
        messages.success(self.request, "Nomina creada correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Nomina'
        context['entidad'] = 'Nomina'
        context['listar_url'] = reverse_lazy('apy:nomina_lista')
        return context
    
class NominaUpdateView(PermisoRequeridoMixin, UpdateView): 
    model = Nomina
    form_class = NominaForm
    template_name = 'Nomina/crear_nomina.html'
    success_url = reverse_lazy('apy:nomina_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'Nomina'
    permission_required = 'change'
    
    def form_valid(self, form):
        messages.success(self.request, "Nomina actualizada correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar empleado'
        context['entidad'] = 'Nomina'
        context['listar_url'] = reverse_lazy('apy:nomina_lista')
        return context

class NominaDeleteView(PermisoRequeridoMixin, DeleteView): 
    model = Nomina
    template_name = 'Nomina/eliminar_nomina.html'
    success_url = reverse_lazy('apy:nomina_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'Nomina'
    permission_required = 'delete'
    
    def form_valid(self, form):
        messages.success(self.request, "Nomina eliminado correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar pago de Nomina'
        context['entidad'] = 'Nomina'
        context['listar_url'] = reverse_lazy('apy:nomina_lista')
        return context