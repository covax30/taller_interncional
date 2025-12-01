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
        # Redirige a la lista de pagos de servicios como fallback
        return reverse_lazy('apy:pago_servicios_lista') 

# --------------Vistas de pago servicios publicos---------------

# NOTA: Se elimina la función 'def pago_servicios(request)'

class PagoServiciosListView(PermisoRequeridoMixin, ListView): 
    model = PagoServiciosPublicos
    template_name ='Pago_Servicios/listar_pagoservicios.html'
    
    # --- Configuración de Permisos ---
    module_name = 'PagoServicios' 
    permission_required = 'view' 
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        nombre = {'nombre' : 'pago servicios'}
        return JsonResponse(nombre)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Pago Servicios Publicos'
        context['crear_url'] = reverse_lazy('apy:pago_servicios_crear')
        context['entidad'] = 'PagoServiciosPublicos'
        return context
    
class PagoServiciosCreateView(PermisoRequeridoMixin, CreateView): 
    model = PagoServiciosPublicos
    form_class = PagoServiciosForm
    template_name = 'Pago_Servicios/crear_pagoservicios.html'
    success_url = reverse_lazy('apy:pago_servicios_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'PagoServicios'
    permission_required = 'add'
    
    def form_valid(self, form):
        messages.success(self.request, "Pago de servicio creado correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context ['titulo'] = 'Crear Pago Servicios Publicos'
        context ['entidad'] = 'PagoServiciosPublicos'
        context ['listar_url'] = reverse_lazy('apy:pago_servicios_lista')
        return context
    
class PagoServiciosUpdateView(PermisoRequeridoMixin, UpdateView):
    model = PagoServiciosPublicos
    form_class = PagoServiciosForm
    template_name = 'Pago_Servicios/crear_pagoservicios.html'
    success_url = reverse_lazy('apy:pago_servicios_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'PagoServicios'
    permission_required = 'change'
    
    def form_valid(self, form):
        messages.success(self.request, "Pago de servicio actualizado correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Pago Servicios Publicos'
        context['entidad'] = 'PagoServiciosPublicos'
        context['listar_url'] = reverse_lazy('apy:pago_servicios_lista')
        return context

class PagoServiciosDeleteView(PermisoRequeridoMixin, DeleteView): 
    model = PagoServiciosPublicos
    template_name = 'Pago_Servicios/eliminar_pagoservicios.html'
    success_url = reverse_lazy('apy:pago_servicios_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'PagoServicios'
    permission_required = 'delete'
    
    def form_valid(self, request, *args, **kwargs):
        # Nota: En DeleteView, el mensaje de éxito se suele poner después de la eliminación.
        # Si usas form_valid para el mensaje, es una lógica personalizada que mantengo aquí.
        messages.success(self.request, "Pago de servicio eliminado correctamente")
        return super().delete(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Pago Servicios Publicos'
        context['entidad'] = 'PagoServiciosPublicos'
        context['listar_url'] = reverse_lazy('apy:pago_servicios_lista')
        return context