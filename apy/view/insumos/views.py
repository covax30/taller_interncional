from django.shortcuts import render, redirect
from apy.models import * # Necesitas importar los modelos, incluyendo 'Insumos', 'Module', y 'Permission'
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from apy.forms import *
from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin

# PERMISO REQUERIDO MIXIN
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
            # Asumiendo que Module y Permission son los modelos correctos
            module = Module.objects.get(name=self.module_name)
            permission_obj = Permission.objects.filter(user=request.user, module=module).first()
            
            has_permission = False
            if permission_obj:
                # Usa getattr para verificar el permiso (ej: permission_obj.view)
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
        # Redirige a la lista de insumos como fallback
        return reverse_lazy('apy:insumo_lista') 

# --------------Vistas de Insumos---------------

class InsumoListView(PermisoRequeridoMixin, ListView): 
    model = Insumos
    template_name = 'insumos/listar.html'
    
    # --- Configuración de Permisos ---
    module_name = 'Insumos' 
    permission_required = 'view'
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        # El dispatch del Mixin se ejecuta antes
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Insumos'
        context['crear_url'] = reverse_lazy('apy:insumo_crear')
        context['entidad'] = 'Insumo'
        return context
    
class InsumoCreateView(PermisoRequeridoMixin, CreateView): 
    model = Insumos
    form_class = InsumoForm
    template_name = 'insumos/crear.html'
    success_url = reverse_lazy('apy:insumo_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'Insumos' 
    permission_required = 'add'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Insumo'
        context['entidad'] = 'Insumo'
        context['listar_url'] = reverse_lazy('apy:insumo_lista')
        return context
    
class InsumoUpdateView(PermisoRequeridoMixin, UpdateView):
    model = Insumos
    form_class = InsumoForm
    template_name = 'insumos/crear.html'
    success_url = reverse_lazy('apy:insumo_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'Insumos' 
    permission_required = 'change'
    
    def form_valid(self, form):
        messages.success(self.request, "Insumo actualizado correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Insumo'
        context['entidad'] = 'Insumo'
        context['listar_url'] = reverse_lazy('apy:insumo_lista')
        return context
    
class InsumoDeleteView(PermisoRequeridoMixin, DeleteView): # ORDEN CORREGIDO
    model = Insumos
    template_name = 'insumos/eliminar.html'
    success_url = reverse_lazy('apy:insumo_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'Insumos' 
    permission_required = 'delete'
    
    def form_valid(self, form):
        messages.success(self.request, "Insumo eliminado correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Insumo'
        context['entidad'] = 'Insumo'
        context['listar_url'] = reverse_lazy('apy:insumo_lista')
        return context
    
# Vista para mostrar estadísticas (No se aplica Mixin)
def estadisticas_view(request):
    # Contar total de insumos
    total_insumos = Insumos.objects.count()

    # Puedes agregar más estadísticas aquí
    context = {
        'total_insumos': total_insumos,
    }
    return render(request, 'estadisticas.html', context)

# API para actualización dinámica del contador de insumos (No se aplica Mixin)
def api_contador_insumos(request):
    total_insumos = Insumos.objects.count()
    return JsonResponse({'total_insumos': total_insumos})