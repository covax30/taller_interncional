from django.shortcuts import render, redirect
from apy.models import *
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from apy.forms import *
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
        # Redirige a la lista de entrada de vehículos como fallback
        return reverse_lazy('apy:entrada_vehiculo_lista') 

# --------------Vistas de Entrada de Vehículos---------------

# NOTA: La función 'def lista_entrada_vehiculos(request)' se elimina

class EntradaVehiculoListView(PermisoRequeridoMixin, ListView):
    model = EntradaVehiculo
    template_name = 'entrada_vehiculos/listar_entrada_vehiculos.html'

    # --- Configuración de Permisos ---
    module_name = 'EntradaVehiculos' 
    permission_required = 'view'
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        nombre = {'nombre' : 'Entrada de Vehiculos'}
        return JsonResponse(nombre)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Entrada de Vehiculos'
        context['crear_url'] = reverse_lazy('apy:entrada_vehiculo_crear')
        context['entidad'] = 'Entrada de Vehiculos'
        return context

class EntradaVehiculoCreateView(PermisoRequeridoMixin, CreateView): 
    model = EntradaVehiculo
    form_class = EntradaVehiculoForm
    template_name = 'entrada_vehiculos/crear_entrada_vehiculos.html'
    success_url = reverse_lazy('apy:entrada_vehiculo_lista')

    # --- Configuración de Permisos ---
    module_name = 'EntradaVehiculos'
    permission_required = 'add'

    def form_valid(self, form):
        messages.success(self.request, "Entrada de Vehiculo creada correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear de Entrada de Vehiculos'
        context['entidad'] = 'Entrada de Vehiculos'
        context['listar_url'] = reverse_lazy('apy:entrada_vehiculo_lista')
        return context

class EntradaVehiculoUpdateView(PermisoRequeridoMixin, UpdateView):
    model = EntradaVehiculo
    form_class = EntradaVehiculoForm
    template_name = 'entrada_vehiculos/crear_entrada_vehiculos.html'
    success_url = reverse_lazy('apy:entrada_vehiculo_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'EntradaVehiculos'
    permission_required = 'change'
    
    def form_valid(self, form):
        messages.success(self.request, "Entrada de Vehiculo actualizada correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar de Entrada de Vehiculos'
        context['entidad'] = 'Entrada de Vehiculos' 
        context['listar_url'] = reverse_lazy('apy:entrada_vehiculo_lista')
        return context

class EntradaVehiculoDeleteView(PermisoRequeridoMixin, DeleteView): 
    model = EntradaVehiculo
    template_name = 'entrada_vehiculos/eliminar_entrada_vehiculos.html'
    success_url = reverse_lazy('apy:entrada_vehiculo_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'EntradaVehiculos'
    permission_required = 'delete'
    
    def form_valid(self, form):
        messages.success(self.request, "Entrada de Vehiculo eliminada correctamente")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar de Entrada de Vehiculos'
        context['entidad'] = 'Entrada de Vehiculos'
        context['listar_url'] = reverse_lazy('apy:entrada_vehiculo_lista')
        return context