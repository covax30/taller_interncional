from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from apy.models import Module, Permission 
from functools import wraps
from django.shortcuts import redirect
from django.http import JsonResponse
from django.contrib import messages

# Diccionario para traducir las acciones al español
TRADUCCIONES_PERMISOS = {
    'view': 'ver',
    'add': 'crear',
    'change': 'editar',
    'delete': 'eliminar'
}

# Diccionario nombres para los módulos
NOMBRES_MODULOS_ESTETICOS = {
    'EstadisticasGenerales': 'Estadísticas Generales',
    'Informes': 'Informes',
    'EntradaVehiculos': 'Entrada de Vehículo',
    'SalidaVehiculos': 'Salida de Vehículo',
    'Vehiculos': 'Vehículos',
    'Marca': 'Marcas',
    'GestionMantenimiento': 'Mantenimientos',
    'Repuestos': 'Repuestos',
    'TipoMantenimientos': 'Tipos de Mantenimiento',
    'Herramientas': 'Herramientas',
    'Insumos': 'Insumos',
    'Gastos': 'Gastos',
    'Factura': 'Facturación',
    'Pagos': 'Pagos',
    'Caja': 'Caja',
    'PagoServicios': 'Servicios Públicos',
    'Proveedor': 'Proveedores',
    'Clientes': 'Clientes',
    'GestionUsuarios': 'Usuarios',
    'Permisos': 'Gestión de Permisos',
    'Respaldos': 'Respaldos',
}

# =======================================================
# 1. MIXIN PARA VISTAS BASADAS EN CLASES (CBVs)
# =======================================================

class PermisoRequeridoMixin(AccessMixin):
    module_name = None      
    permission_required = None 
    redirect_url = reverse_lazy('apy:vehiculo_lista')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission() 

        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)

        if self.module_name is None or self.permission_required is None:
            raise NotImplementedError(f'{self.__class__.__name__} debe definir module_name y permission_required.')

        try:
            module = Module.objects.get(name=self.module_name)
            permission_obj = Permission.objects.filter(user=request.user, module=module).first()
            
            has_permission = getattr(permission_obj, self.permission_required, False) if permission_obj else False
                
            if has_permission:
                return super().dispatch(request, *args, **kwargs)
            else:
                # Mensaje de error personalizado con traducción y nombre estético del módulo
                accion_es = TRADUCCIONES_PERMISOS.get(self.permission_required, self.permission_required)
                modulo_es = NOMBRES_MODULOS_ESTETICOS.get(self.module_name, self.module_name)
                error_message = f"No tienes permiso para {accion_es} en el módulo {modulo_es}."
                                
                if self.permission_required == 'view':
                    raise PermissionDenied(error_message) # Bloqueo total
                
                # Si es otra acción, mandamos alerta y redirigimos
                messages.error(request, error_message)
                return redirect(request.META.get('HTTP_REFERER', self.redirect_url))
                
        except Module.DoesNotExist:
            raise PermissionDenied(f"Módulo '{self.module_name}' no encontrado.")


# =======================================================
# 2. DECORADOR PARA VISTAS BASADAS EN FUNCIÓN (FBVs)
# =======================================================

def permiso_requerido_fbv(module_name, permission_required, api=False):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                error_message = "Usuario no autenticado."
                if api: return JsonResponse({'detail': error_message}, status=403)
                raise PermissionDenied(error_message) 

            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
                
            try:
                module = Module.objects.get(name=module_name)
                permission_obj = Permission.objects.filter(user=request.user, module=module).first()
                
                has_permission = getattr(permission_obj, permission_required, False) if permission_obj else False
                    
                if has_permission:
                    return view_func(request, *args, **kwargs)
                else:
                    error_message = f"No tienes permiso de {permission_required.upper()} para el módulo '{module_name}'."
                    
                    if api:
                        return JsonResponse({'detail': error_message}, status=403)
                    
                    if permission_required == 'view':
                        raise PermissionDenied(error_message) # Bloqueo total
                    
                    # Mensaje de error personalizado con traducción y nombre estético del módulo
                    accion_es = TRADUCCIONES_PERMISOS.get(permission_required, permission_required)
                    modulo_es = NOMBRES_MODULOS_ESTETICOS.get(module_name, module_name)
                    error_message = f"No tienes permiso para {accion_es} en el módulo {modulo_es}."

            except Module.DoesNotExist:
                raise PermissionDenied(f"Módulo '{module_name}' no encontrado.")
                
        return _wrapped_view
    return decorator