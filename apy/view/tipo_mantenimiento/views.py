from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from apy.forms import *
from django.contrib import messages
# Se elimina la importación local de AccessMixin
# Importar modelos necesarios para el Mixin
from apy.models import TipoMantenimiento, Module, Permission 
from apy.decorators import PermisoRequeridoMixin # <-- Se mantiene solo la importación

# --------------Vistas de Tipo de Mantenimiento---------------

class TipoMantenimientoListView(PermisoRequeridoMixin, ListView):
    model = TipoMantenimiento
    template_name = 'tipo_mantenimiento/listar.html'
    
    # --- Configuración de Permisos ---
    module_name = 'Tipo Mantenimiento' 
    permission_required = 'view'
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Tipos de Mantenimiento'
        context['crear_url'] = reverse_lazy('apy:tipo_mantenimiento_crear')
        context['entidad'] = 'Tipo de Mantenimiento'
        return context

class TipoMantenimientoCreateView(PermisoRequeridoMixin, CreateView): 
    model = TipoMantenimiento
    form_class = TipoMantenimientoForm
    template_name = 'tipo_mantenimiento/crear.html'
    success_url = reverse_lazy('apy:tipo_mantenimiento_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'Tipo Mantenimiento'
    permission_required = 'add'
    
    def form_valid(self, form):
        messages.success(self.request, "tipo de mantnimiento creado correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Tipo de Mantenimiento'
        context['entidad'] = 'Tipo de Mantenimiento'
        context['listar_url'] = reverse_lazy('apy:tipo_mantenimiento_lista')
        return context

class TipoMantenimientoUpdateView(PermisoRequeridoMixin, UpdateView): 
    model = TipoMantenimiento
    form_class = TipoMantenimientoForm
    template_name = 'tipo_mantenimiento/crear.html'
    success_url = reverse_lazy('apy:tipo_mantenimiento_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'Tipo Mantenimiento'
    permission_required = 'change'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Tipo de Mantenimiento'
        context['entidad'] = 'Tipo de Mantenimiento'
        context['listar_url'] = reverse_lazy('apy:tipo_mantenimiento_lista')
        return context

class TipoMantenimientoDeleteView(PermisoRequeridoMixin, DeleteView):
    model = TipoMantenimiento
    template_name = 'tipo_mantenimiento/eliminar.html'
    success_url = reverse_lazy('apy:tipo_mantenimiento_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'Tipo Mantenimiento'
    permission_required = 'delete'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar tipo de mantenimiento'
        context['entidad'] = 'tipo de mantenimiento'
        context['listar_url'] = reverse_lazy('apy:tipo_mantenimiento_lista')
        return context