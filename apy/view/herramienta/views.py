from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from apy.forms import *
from django.contrib import messages
# Se elimina la importación de AccessMixin ya que no se usa localmente.

# Importar modelos necesarios para la vista
from apy.models import Herramienta 
# Importar el Mixin Corregido (que lanza 403)
from apy.decorators import PermisoRequeridoMixin

# --------------Vistas de Herramientas---------------

class HerramientaListView(PermisoRequeridoMixin, ListView): 
    model = Herramienta
    template_name = 'herramienta/listar.html'
    
    # --- Configuración de Permisos ---
    module_name = 'Herramientas' 
    permission_required = 'view'
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        # Usa el Mixin importado de apy.decorators
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Herramientas'
        context['crear_url'] = reverse_lazy('apy:herramienta_crear')
        context['entidad'] = 'Herramienta'
        return context

class HerramientaCreateView(PermisoRequeridoMixin, CreateView): 
    model = Herramienta
    form_class = HerramientaForm
    template_name = 'herramienta/crear.html'
    success_url = reverse_lazy('apy:herramienta_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'Herramientas'
    permission_required = 'add'
    
    def form_valid(self, form):
        messages.success(self.request, "herramienta creada correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Herramienta'
        context['entidad'] = 'Herramienta'
        context['listar_url'] = reverse_lazy('apy:herramienta_lista')
        return context

class HerramientaUpdateView(PermisoRequeridoMixin, UpdateView): 
    model = Herramienta
    form_class = HerramientaForm
    template_name = 'herramienta/crear.html'
    success_url = reverse_lazy('apy:herramienta_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'Herramientas'
    permission_required = 'change'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Herramienta'
        context['entidad'] = 'Herramienta'
        context['listar_url'] = reverse_lazy('apy:herramienta_lista')
        return context

class HerramientaDeleteView(PermisoRequeridoMixin, DeleteView): 
    model = Herramienta
    template_name = 'herramienta/eliminar.html'
    success_url = reverse_lazy('apy:herramienta_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'Herramientas'
    permission_required = 'delete'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Herramienta'
        context['entidad'] = 'Herramienta'
        context['listar_url'] = reverse_lazy('apy:herramienta_lista')
        return context