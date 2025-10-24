from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from apy.forms import *
from django.db.models import F
from apy.models import Repuesto, Module, Permission
from apy.forms import RepuestoForm
from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin
from apy.decorators import PermisoRequeridoMixin

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
        # Redirige a la lista de repuestos como fallback
        return reverse_lazy('apy:repuesto_lista') 

# --------------Vistas de Repuestos---------------

class RepuestoListView(PermisoRequeridoMixin, ListView): 
    model = Repuesto
    template_name = 'repuestos/listar.html'
    
    # --- Configuración de Permisos ---
    module_name = 'Repuestos' 
    permission_required = 'view'
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Repuestos'
        context['crear_url'] = reverse_lazy('apy:repuesto_crear')
        context['entidad'] = 'Repuesto'
        return context
    
class RepuestoCreateView(PermisoRequeridoMixin, CreateView): 
    model = Repuesto
    form_class = RepuestoForm
    template_name = 'repuestos/crear.html'
    success_url = reverse_lazy('apy:repuesto_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'Repuestos'
    permission_required = 'add'
    
    def form_valid(self, form):
        messages.success(self.request, "repuesto creado correctamente")
        return super().form_valid(form) 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Repuesto'
        context['entidad'] = 'Repuesto'
        context['listar_url'] = reverse_lazy('apy:repuesto_lista')
        return context
    
class RepuestoUpdateView(PermisoRequeridoMixin, UpdateView): 
    model = Repuesto
    form_class = RepuestoForm
    template_name = 'repuestos/crear.html'
    success_url = reverse_lazy('apy:repuesto_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'Repuestos'
    permission_required = 'change'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Repuesto'
        context['entidad'] = 'Repuesto'
        context['listar_url'] = reverse_lazy('apy:repuesto_lista')
        return context
    
class RepuestoDeleteView(PermisoRequeridoMixin, DeleteView): 
    model = Repuesto
    template_name = 'repuestos/eliminar.html'
    success_url = reverse_lazy('apy:repuesto_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'Repuestos'
    permission_required = 'delete'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Repuesto'
        context['entidad'] = 'Repuesto'
        context['listar_url'] = reverse_lazy('apy:repuesto_lista')
        return context


@csrf_exempt
def repuestos_bajo_stock_api(request):
    """
    API para listar repuestos cuyo stock es menor que el stock mínimo.
    """
    # Esta vista basada en función queda sin el Mixin
    repuestos = Repuesto.objects.filter(stock__lt=F('stock_minimo'))
    data = [
        {
            'id': r.id,
            'nombre': r.nombre,
            'stock': r.stock,
            'stock_minimo': r.stock_minimo
        }
        for r in repuestos
    ]
    return JsonResponse(data, safe=False)