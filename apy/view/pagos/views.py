from django.shortcuts import render, redirect
from apy.models import *
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from apy.forms import *
from django.contrib import messages
# Se elimina la importación de AccessMixin ya que no se usa localmente.
from apy.decorators import PermisoRequeridoMixin 

# --------------Vistas de pagos---------------

class PagosListView(PermisoRequeridoMixin, ListView): 
    model = Pagos
    template_name ='Pagos/listar_pago.html'
    
    # --- Configuración de Permisos ---
    module_name = 'Pagos' 
    permission_required = 'view' 
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        nombre = {'nombre' : 'pago'}
        return JsonResponse(nombre)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Pagos'
        context['crear_url'] = reverse_lazy('apy:pagos_crear')
        context['entidad'] = 'Pagos'
        return context
    
class PagosCreateView(PermisoRequeridoMixin, CreateView): 
    model = Pagos
    form_class = PagosForm
    template_name = 'Pagos/crear_pago.html'
    success_url = reverse_lazy('apy:pagos_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'Pagos'
    permission_required = 'add'
    
    def form_valid(self, form):
        messages.success(self.request, "Pago creado correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context ['titulo'] = 'Crear Pagos'
        context ['entidad'] = 'Pagos'
        context ['listar_url'] = reverse_lazy('apy:pagos_lista')
        return context
    
class PagosUpdateView(PermisoRequeridoMixin, UpdateView): 
    model = Pagos
    form_class = PagosForm
    template_name = 'Pagos/crear_pago.html'
    success_url = reverse_lazy('apy:pagos_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'Pagos'
    permission_required = 'change'
    
    def form_valid(self, form):
        messages.success(self.request, "Pago actualizado correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Pagos'
        context['entidad'] = 'Pagos'
        context['listar_url'] = reverse_lazy('apy:pagos_lista')
        return context

class PagosDeleteView(PermisoRequeridoMixin, DeleteView): 
    model = Pagos 
    template_name = 'Pagos/eliminar_pago.html'
    success_url = reverse_lazy('apy:pagos_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'Pagos'
    permission_required = 'delete'
    
    def form_valid(self, form):
        messages.success(self.request, "Pago eliminado correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Pagos'
        context['entidad'] = 'Pagos'
        context['listar_url'] = reverse_lazy('apy:pagos_lista')
        return context