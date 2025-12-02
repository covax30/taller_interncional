from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.mixins import AccessMixin # <-- Necesaria
# Asegúrate de importar tus modelos de permiso
from apy.models import Module, Permission 


class PermisoRequeridoMixin(AccessMixin):
    """
    Mixin para verificar los permisos del usuario actual.
    """ 
    module_name = None      
    permission_required = None 
    redirect_url = reverse_lazy('apy:vehiculo_lista') # Default fallback URL

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        
        # 1. Verificar Autenticación
        if not user.is_authenticated:
            return self.handle_no_permission() 

        # 2. Permitir Superusuario
        if user.is_superuser:
            return super().dispatch(request, *args, **kwargs)

        # 3. Verificar Configuración (Implementación omitida para brevedad)
        # ...
        
        # 4. Lógica de Permisos Personalizados
        try:
            module = Module.objects.get(name=self.module_name)
            permission_obj = Permission.objects.filter(user=user, module=module).first()
            
            has_permission = False
            if permission_obj:
                has_permission = getattr(permission_obj, self.permission_required, False)
                
            if has_permission:
                return super().dispatch(request, *args, **kwargs)
            else:
                messages.warning(request, f"Acceso denegado. No tienes permiso de {self.permission_required.upper()} para el módulo '{self.module_name}'.")
                return redirect(self.redirect_url) 
                
        except Module.DoesNotExist:
            messages.error(request, f"Error de configuración: Módulo '{self.module_name}' no encontrado. ⚙️")
            return redirect(self.redirect_url)

    def handle_no_permission(self):
        # Si no está autenticado, redirigir al login
        return redirect('login:login')
        

# (Tu decorador permission_required_decorator también puede ir aquí)
# ...