from django.shortcuts import render, redirect
from apy.models import * # Asegúrate de que Marca, Module, y Permission sean importados
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from apy.forms import *
from django.contrib import messages
# Se elimina la importación de AccessMixin ya que no se usa localmente.

# Importar el Mixin Corregido (que lanza 403)
from apy.decorators import PermisoRequeridoMixin


# --------------Vistas de Marca---------------

class MarcaListView(PermisoRequeridoMixin, ListView): 
    model = Marca
    template_name ='Marca/listar_marca.html'
    
    # --- Configuración de Permisos ---
    module_name = 'Marca' 
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
        context['titulo'] = 'Lista de Marcas'
        context['crear_url'] = reverse_lazy('apy:marca_crear')
        context['entidad'] = 'Marcas'
        return context
    
class MarcaCreateView(PermisoRequeridoMixin, CreateView): 
    model = Marca
    form_class = MarcaForm
    template_name = 'Marca/crear_marca.html'
    success_url = reverse_lazy('apy:marca_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'Marca'
    permission_required = 'add'
    
    # --- Configuración de Permisos ---
    module_name = 'Marca'
    permission_required = 'add'
    
    def form_valid(self, form):
        messages.success(self.request, "Marca creada correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context ['titulo'] = 'Crear Marca'
        context ['entidad'] = 'Marca'
        context ['listar_url'] = reverse_lazy('apy:marca_lista')
        return context
    
class MarcaUpdateView(PermisoRequeridoMixin, UpdateView): 
    model = Marca
    form_class = MarcaForm
    template_name = 'Marca/crear_marca.html'
    success_url = reverse_lazy('apy:marca_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'Marca'
    permission_required = 'change'
    
    def form_valid(self, form):
        messages.success(self.request, "Marca actualizada correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar marca'
        context['entidad'] = 'Marcas' 
        context['listar_url'] = reverse_lazy('apy:marca_lista')
        return context

class MarcaDeleteView(PermisoRequeridoMixin, DeleteView): 
    model = Marca
    template_name = 'Marca/eliminar_marca.html'
    success_url = reverse_lazy('apy:marca_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'Marca'
    permission_required = 'delete'
    
    def form_valid(self, form):
        messages.success(self.request, "Marca eliminada correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Marca'
        context['entidad'] = 'Marcas' 
        context['listar_url'] = reverse_lazy('apy:marca_lista')
        return context

class MarcaCreateModalView(CreateView):
    model = Marca
    form_class = MarcaForm
    template_name = "Marca/modal_marca.html"
    success_url = reverse_lazy("apy:marca_lista")

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        try:
            self.object = form.save()
            return JsonResponse({
                "success": True,
                "id": self.object.id,
                "text": str(self.object),
                "message": "Marca registrada correctamente ✅"
            })
        except Exception as e:
            return JsonResponse({
                "success": False,
                "message": f"Error al guardar: {str(e)}"
            }, status=500)
    
    def form_invalid(self, form):
        html = render_to_string(self.template_name, {"form": form}, request=self.request)
        return JsonResponse({
            "success": False,
            "html": html,
            "message": "Por favor, corrige los errores en el formulario ❌"
        })