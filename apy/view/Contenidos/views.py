from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from apy.forms import *
from django.contrib import messages
# Importar modelos necesarios
from apy.models import Factura 
# Importar el Mixin Corregido (que lanza 403)
from apy.decorators import PermisoRequeridoMixin 


# --------------Vistas de Facturas---------------
class FacturaListView(PermisoRequeridoMixin, ListView):
    model = Factura
    template_name ='Contenido/listar_factura.html'
    
    # --- Configuración de Permisos ---
    module_name = 'Facturas' 
    permission_required = 'view'
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        # El Mixin se ejecuta antes de super().dispatch (lanzará 403)
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        nombre = {'nombre' : 'Karol'}
        return JsonResponse(nombre)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Facturas'
        context['crear_url'] = reverse_lazy('apy:factura_crear')
        context['entidad'] = 'Factura'
        return context
    
class FacturaCreateView(PermisoRequeridoMixin, CreateView): 
    model = Factura
    form_class = FacturaForm
    template_name = 'Contenido/crear_factura.html'
    success_url = reverse_lazy('apy:factura_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'Facturas'
    permission_required = 'add'
    
    def form_valid(self, form):
        messages.success(self.request, "Factura creada correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context ['titulo'] = 'Crear Factura'
        context ['entidad'] = 'Facturas'
        context ['listar_url'] = reverse_lazy('apy:factura_lista')
        return context
    
class FacturaUpdateView(PermisoRequeridoMixin, UpdateView): 
    model = Factura
    form_class = FacturaForm
    template_name = 'Contenido/crear_factura.html'
    success_url = reverse_lazy('apy:factura_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'Facturas'
    permission_required = 'change'
    
    def form_valid(self, form):
        messages.success(self.request, "Factura actualizada correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Factura'
        context['entidad'] = 'Facturas'
        context['listar_url'] = reverse_lazy('apy:factura_lista')
        return context

class FacturaDeleteView(PermisoRequeridoMixin, DeleteView):
    model = Factura
    template_name = 'Contenido/eliminar_factura.html'
    success_url = reverse_lazy('apy:factura_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'Facturas'
    permission_required = 'delete'
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Factura eliminada correctamente")
        return super().delete(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Factura'
        context['entidad'] = 'Facturas'
        context['listar_url'] = reverse_lazy('apy:factura_lista')
        return context