from django.shortcuts import render, redirect
# Se asume que apy.models, apy.view.clientes.views, y apy.forms contienen las clases necesarias
from apy.models import *
# from apy.view.clientes.views import * # Si este archivo contiene estas vistas, esta importación puede ser redundante o generar un conflicto circular. Se recomienda revisar su necesidad.
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from apy.forms import *
from django.contrib.auth.mixins import AccessMixin
from apy.decorators import PermisoRequeridoMixin

## MIXIN DE PERMISOS
class PermisoRequeridoMixin(AccessMixin):
    """
    Mixin para verificar los permisos del usuario actual.
    Requiere que se definan 'module_name' y 'permission_required'.
    """
    module_name = None      
    permission_required = None 

    def dispatch(self, request, *args, **kwargs):
        # 1. Verificar Autenticación
        if not request.user.is_authenticated:
            # Llama a la lógica de AccessMixin para redirigir al login
            return self.handle_no_permission() 

        # 2. Permitir Superusuario
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)

        # 3. Verificar Configuración
        if self.module_name is None or self.permission_required is None:
            raise NotImplementedError(
                f'{self.__class__.__name__} debe definir module_name y permission_required.'
            )

        # 4. Lógica de Permisos Personalizados
        try:
            # Asegurar que Module y Permission son los modelos correctos
            module = Module.objects.get(name=self.module_name)
            permission_obj = Permission.objects.filter(user=request.user, module=module).first()
            
            has_permission = False
            if permission_obj:
                has_permission = getattr(permission_obj, self.permission_required, False)
                
            if has_permission:
                return super().dispatch(request, *args, **kwargs)
            else:
                messages.warning(request, f"Acceso denegado. No tienes permiso de {self.permission_required.upper()} para el módulo '{self.module_name}'.")
                return redirect(self.get_permission_denied_url())
                
        except Module.DoesNotExist:
            messages.error(request, f"Error de configuración: Módulo '{self.module_name}' no encontrado.")
            return redirect(self.get_permission_denied_url())

    def get_permission_denied_url(self):
        return reverse_lazy('apy:cliente_lista')
    

## VISTAS BASADAS EN CLASES (CBVs)

class ClienteListView(PermisoRequeridoMixin, ListView):
    model = Cliente
    template_name = 'clientes/listar_clientes.html'
    
    # --- Configuración de Permisos ---
    module_name = 'Clientes' 
    permission_required = 'view' 
    # --------------------------------

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
        messages.success(self.request, "Cliente creado correctamente")
        response = super().form_valid(form)
        
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
    
    def form_valid(self, form):
        messages.success(self.request, "Cliente eliminado correctamente")
        return super().form_valid(form)
    
    # --- Configuración de Permisos ---
    module_name = 'Clientes'
    permission_required = 'delete'
    
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar de Clientes'
        context['entidad'] = 'Cliente'
        context['listar_url'] = reverse_lazy('apy:cliente_lista')
        return context
    
# Vista para mostrar estadísticas
def estadisticas_view(request):
    # Contar total de clientes
    total_clientes = Cliente.objects.count()
    
    # Puedes agregar más estadísticas aquí
    context = {
        'total_clientes': total_clientes,
    }
    return render(request, 'estadisticas.html', context)

# API para actualización dinámica del contador de clientes
def api_contador_clientes(request):
    total_clientes = Cliente.objects.count()
    return JsonResponse({'total_clientes': total_clientes})