from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from apy.models import Module, Permission 
from functools import wraps
from django.shortcuts import redirect
from django.http import JsonResponse

# =======================================================
# 1. MIXIN PARA VISTAS BASADAS EN CLASES (CBVs)
#    - Lanza PermissionDenied (HTTP 403)
# =======================================================

class PermisoRequeridoMixin(AccessMixin):
    """
    Mixin para verificar los permisos del usuario actual.
    """ 
    module_name = None      
    permission_required = None 
    redirect_url = reverse_lazy('apy:vehiculo_lista') # Default fallback URL

    def dispatch(self, request, *args, **kwargs):
        # 1. Verificar Autenticación (maneja redirección a login)
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
            # Buscar el Módulo
            module = Module.objects.get(name=self.module_name)
            
            # Buscar el objeto Permission específico para el usuario y módulo
            permission_obj = Permission.objects.filter(user=request.user, module=module).first()
            
            has_permission = False
            if permission_obj:
                # Verificar si el campo de permiso (ej: 'view') es True
                has_permission = getattr(permission_obj, self.permission_required, False)
                
            if has_permission:
                # Si tiene permiso, continúa con la vista
                return super().dispatch(request, *args, **kwargs)
            else:
                # Si NO tiene permiso, lanza PermissionDenied (Error 403)
                raise PermissionDenied(
                    f"Acceso denegado. No tienes permiso de {self.permission_required.upper()} para el módulo '{self.module_name}'."
                )
                
        except Module.DoesNotExist:
            # Si el módulo no existe (error de configuración), lanzar 403
            raise PermissionDenied(f"Error de configuración: Módulo '{self.module_name}' no encontrado o no autorizado.")


# =======================================================
# 2. DECORADOR PARA VISTAS BASADAS EN FUNCIÓN (FBVs y APIs)
#    - Usa 'api=True' para devolver JsonResponse 403
# =======================================================

def permiso_requerido_fbv(module_name, permission_required, api=False):
    """
    Decorador para vistas basadas en función.
    Si api=True, devuelve JsonResponse 403.
    Si api=False (default), lanza PermissionDenied (Error 403).
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # 1. Verificar Autenticación (simplemente retornar 403 si no está autenticado)
            if not request.user.is_authenticated:
                error_message = "Acceso denegado. El usuario no está autenticado."
                if api:
                    return JsonResponse({'detail': error_message}, status=403)
                else:
                    # Usar AccessMixin.handle_no_permission() no funciona aquí, 
                    # así que lanzamos directamente el 403 (o podrías redirigir al login)
                    raise PermissionDenied(error_message) 

            # 2. Permitir Superusuario
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
                
            # 3. Lógica de Permisos Personalizados
            try:
                module = Module.objects.get(name=module_name)
                permission_obj = Permission.objects.filter(user=request.user, module=module).first()
                
                has_permission = False
                if permission_obj:
                    has_permission = getattr(permission_obj, permission_required, False)
                    
                if has_permission:
                    return view_func(request, *args, **kwargs)
                else:
                    # Acceso denegado (el permiso existe pero está en False)
                    error_message = f"Acceso denegado. No tienes permiso de {permission_required.upper()} para el módulo '{module_name}'."
                    
                    if api:
                        # Para APIs, devolver JSON 403
                        return JsonResponse({'detail': error_message}, status=403)
                    else:
                        # Para vistas regulares, lanzar 403
                        raise PermissionDenied(error_message)

            except Module.DoesNotExist:
                # Módulo no encontrado (error de configuración)
                error_message = f"Error de configuración: Módulo '{module_name}' no encontrado."
                if api:
                    return JsonResponse({'detail': error_message}, status=403)
                else:
                    raise PermissionDenied(error_message)
                
        return _wrapped_view
    return decorator