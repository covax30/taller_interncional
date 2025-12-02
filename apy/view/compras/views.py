from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from apy.forms import *
from django.contrib import messages
# Importar modelos necesarios
from apy.models import Compra 
# Importar el Mixin Corregido (que lanza 403)
from apy.decorators import PermisoRequeridoMixin 


# --------------Vistas de Compras---------------
class CompraListView(PermisoRequeridoMixin, ListView): 
    model = Compra
    template_name = 'compras/listar_compras.html'

    # --- Configuración de Permisos ---
    module_name = 'Compras' 
    permission_required = 'view'
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        nombre = {'nombre' : 'Compra'}
        return JsonResponse(nombre)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Compras'
        context['crear_url'] = reverse_lazy('apy:compra_crear')
        context['entidad'] = 'Compra'
        return context

class CompraCreateView(PermisoRequeridoMixin, CreateView):
    model = Compra
    form_class = CompraForm
    template_name = 'compras/crear_compras.html'
    success_url = reverse_lazy('apy:compra_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'Compras'
    permission_required = 'add'
    
    def form_valid(self, form):
        messages.success(self.request, "Compra creada correctamente")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear de Compras'
        context['entidad'] = 'Compra'
        context['listar_url'] = reverse_lazy('apy:compra_lista')
        return context

class CompraUpdateView(PermisoRequeridoMixin, UpdateView): 
    model = Compra
    form_class = CompraForm
    template_name = 'compras/crear_compras.html'
    success_url = reverse_lazy('apy:compra_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'Compras'
    permission_required = 'change'
    
    def form_valid(self, form):
        messages.success(self.request, "Compra actualizada correctamente")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar de Compras'
        context['entidad'] = 'Compra'
        context['listar_url'] = reverse_lazy('apy:compra_lista')
        return context

class CompraDeleteView(PermisoRequeridoMixin, DeleteView):
    model = Compra
    template_name = 'compras/eliminar_compras.html'
    success_url = reverse_lazy('apy:compra_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'Compras'
    permission_required = 'delete'
    
    def form_valid(self, form):
        messages.success(self.request, "Compra eliminada correctamente")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar de Compras'
        context['entidad'] = 'Compra'
        context['listar_url'] = reverse_lazy('apy:compra_lista')
        return context