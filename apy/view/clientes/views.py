from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from django.contrib.auth.mixins import AccessMixin # Solo necesaria si defines mixins locales
# Importaciones de modelos, formularios y Mixin corregido
from apy.models import *
from apy.forms import *
from apy.decorators import PermisoRequeridoMixin, permiso_requerido_fbv # <-- Asumo que 'permiso_requerido_fbv' es tu decorador de función 

# --- VISTAS BASADAS EN CLASES (CBVs) - PROTEGIDAS ---

class ClienteListView(PermisoRequeridoMixin, ListView):
    model = Cliente
    template_name = 'clientes/listar_clientes.html'
    
    # --- Configuración de Permisos ---
    module_name = 'Clientes' 
    permission_required = 'view' 
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        nombre = {'nombre' : 'Cliente'}
        return JsonResponse(nombre)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Clientes'
        context['crear_url'] = reverse_lazy('apy:cliente_crear')
        context['entidad'] = 'Cliente'
        return context
    
class ClienteCreateView(PermisoRequeridoMixin, CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'clientes/crear_clientes.html'
    success_url = reverse_lazy('apy:cliente_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'Clientes'
    permission_required = 'add'
    
    def form_valid(self, form):
        # El mensaje de success se añade aquí, después de la validación
        response = super().form_valid(form)
        messages.success(self.request, "Cliente creado correctamente")
        
        # Si la request es AJAX, devolver JSON con el nuevo contador
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            total_clientes = Cliente.objects.count()
            return JsonResponse({
                'success': True, 
                'total_clientes': total_clientes,
                'message': 'Cliente creado correctamente'
            })
        
        return response
    
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear de Clientes'
        context['entidad'] = 'Cliente'
        context['listar_url'] = reverse_lazy('apy:cliente_lista')
        return context
    
class ClienteUpdateView(PermisoRequeridoMixin, UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'clientes/crear_clientes.html'
    success_url = reverse_lazy('apy:cliente_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'Clientes'
    permission_required = 'change'
    
    def form_valid(self, form):
        messages.success(self.request, "Cliente actualizado correctamente")
        return super().form_valid(form)
    
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar de Clientes'
        context['entidad'] = 'Cliente'
        context['listar_url'] = reverse_lazy('apy:cliente_lista')
        return context
    
class ClienteDeleteView(PermisoRequeridoMixin, DeleteView): 
    model = Cliente
    template_name = 'clientes/eliminar_clientes.html'
    success_url = reverse_lazy('apy:cliente_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'Clientes'
    permission_required = 'delete'
    
    def form_valid(self, form):
        messages.success(self.request, "Cliente eliminado correctamente")
        return super().form_valid(form)
    
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar de Clientes'
        context['entidad'] = 'Cliente'
        context['listar_url'] = reverse_lazy('apy:cliente_lista')
        return context
    
# --- VISTAS BASADAS EN FUNCIÓN (FBVs) - PROTEGIDAS ---

@permiso_requerido_fbv(module_name='Clientes', permission_required='view')
def estadisticas_view(request):
    """Muestra estadísticas, requiere permiso 'view' de Clientes."""
    # Contar total de clientes
    total_clientes = Cliente.objects.count()
    
    context = {
        'total_clientes': total_clientes,
        'titulo': 'Estadísticas de Clientes'
    }
    return render(request, 'clientes/estadisticas.html', context)

# API para actualización dinámica del contador de clientes (No protegida con 403, solo autenticación si es necesario)
def api_contador_clientes(request):
    """Retorna el total de clientes para actualización AJAX."""
    total_clientes = Cliente.objects.count()
    return JsonResponse({'total_clientes': total_clientes})