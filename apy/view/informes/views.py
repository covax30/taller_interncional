from django.shortcuts import render, redirect
from apy.models import Informes, Module, Permission 
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from apy.forms import *
from django.contrib import messages
# Se elimina la importación de AccessMixin ya que no se usa localmente.
from apy.decorators import PermisoRequeridoMixin

# --------------Vistas de informes---------------

class InformesListView(PermisoRequeridoMixin, ListView): 
    model = Informes
    template_name ='Informes/listar_informe.html'
    
    # --- Configuración de Permisos ---
    module_name = 'Informes' 
    permission_required = 'view'
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        # Usa el Mixin importado de apy.decorators
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        nombre = {'nombre' : 'Informes'}
        return JsonResponse(nombre)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Informes'
        context['crear_url'] = reverse_lazy('apy:informes_crear')
        context['entidad'] = 'Informes'
        return context
    
class InformesCreateView(PermisoRequeridoMixin, CreateView): 
    model = Informes
    form_class = InformeForm
    template_name = 'Informes/crear_informe.html'
    success_url = reverse_lazy('apy:informes_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'Informes'
    permission_required = 'add'
    
    def form_valid(self, form):
        messages.success(self.request, "Informe creado correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context ['titulo'] = 'Crear Informe'
        context ['entidad'] = 'Informes'
        context ['listar_url'] = reverse_lazy('apy:informes_lista')
        return context
    
class InformesUpdateView(PermisoRequeridoMixin, UpdateView): 
    model = Informes
    form_class = InformeForm
    template_name = 'Informes/crear_informe.html'
    success_url = reverse_lazy('apy:informes_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'Informes'
    permission_required = 'change'
    
    def form_valid(self, form):
        messages.success(self.request, "Informe actualizado correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Informe'
        context['entidad'] = 'Informes'
        context['listar_url'] = reverse_lazy('apy:informes_lista')
        return context

class InformesDeleteView(PermisoRequeridoMixin, DeleteView): 
    model = Informes
    template_name = 'Informes/eliminar_informe.html'
    success_url = reverse_lazy('apy:informes_lista')
    context_object_name = 'object'
    
    # --- Configuración de Permisos ---
    module_name = 'Informes'
    permission_required = 'delete'
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form): 
        messages.success(self.request, "Informe eliminado correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Informe'
        context['entidad'] = 'Informes'
        context['listar_url'] = reverse_lazy('apy:informes_lista')
        return context