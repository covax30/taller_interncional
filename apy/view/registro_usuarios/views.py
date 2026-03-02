from gettext import translation

from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib import messages
from apy.forms import ProfileForm, ProfileForm, RegistroUsuarioForm 
from apy.decorators import PermisoRequeridoMixin
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string

# MIXINS DE PROTECCIÓN
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from apy.models import Profile

# Clase base que implementa la lógica para verificar si el usuario es superusuario
class SuperuserRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    # Asegura que el usuario esté logueado
    login_url = '/login/' 
    
    # URL a la que se redirige si el usuario no pasa la prueba (no es Superuser)
    raise_exception = False
    permission_denied_message = "Solo el Administrador tiene acceso a esta sección."
    
    def test_func(self):
        """Verifica si el usuario es un superusuario."""
        # Se asegura de que esté autenticado Y que sea un superusuario
        return self.request.user.is_authenticated and self.request.user.is_superuser

# 1. VISTA DE CREACIÓN (RegistroUsuarioCreateView) - PROTEGIDA

# Ahora heredamos de la clase SuperuserRequiredMixin
class RegistroUsuarioCreateView(SuperuserRequiredMixin, CreateView):
    model = User
    form_class = RegistroUsuarioForm
    template_name = 'registro_usuarios/registro_usuarios.html' 
    success_url = reverse_lazy('apy:registro_usuario_lista') 
    
    # --- Configuración de Permisos ---
    module_name = 'GestionUsuarios'
    permission_required = 'add'

    def form_valid(self, form):
        messages.success(self.request, f"¡Éxito! El usuario '{form.cleaned_data.get('username')}' ha sido creado.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Registro de Nuevo Usuario'
        context['entidad'] = 'Usuarios'
        context['listar_url'] = reverse_lazy('apy:registro_usuario_lista') 
        return context

# 2. VISTA DE ACTUALIZACIÓN (RegistroUpdateView) - PROTEGIDA

# Ahora heredamos de la clase SuperuserRequiredMixin
class RegistroUpdateView(SuperuserRequiredMixin, UpdateView):
    model = User
    form_class = RegistroUsuarioForm 
    template_name = 'registro_usuarios/registro_usuarios.html' 
    success_url = reverse_lazy('apy:registro_usuario_lista') 
    
    # --- Configuración de Permisos ---
    module_name = 'GestionUsuarios'
    permission_required = 'change'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Usuario'
        context['entidad'] = 'Usuarios'
        context['listar_url'] = reverse_lazy('apy:registro_usuario_lista')
        return context

    def form_valid(self, form):
        # Al llamar a form.save(), se ejecuta nuestra lógica personalizada de roles y perfil
        self.object = form.save() 
        messages.success(self.request, f"Usuario {self.object.username} actualizado correctamente.")
        return super().form_valid(form)


# 3. VISTA DE ELIMINACIÓN (RegistroDeleteView) - PROTEGIDA

# Ahora heredamos de la clase SuperuserRequiredMixin
class RegistroDeleteView(SuperuserRequiredMixin, DeleteView):
    model = User
    template_name = 'registro_usuarios/eliminar_registro_usuarios.html'
    success_url = reverse_lazy('apy:registro_usuario_lista') 
    
    # --- Configuración de Permisos ---
    module_name = 'GestionUsuarios'
    permission_required = 'delete'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Usuario'
        context['entidad'] = 'Usuarios'
        context['listar_url'] = reverse_lazy('apy:registro_usuario_lista')
        return context
    
    def form_valid(self, form):
        messages.success(self.request, f"Usuario '{self.object.username}' eliminado correctamente.")
        return super().form_valid(form)
    
    def dispatch(self, request, *args, **kwargs):
        # Obtenemos el usuario que se quiere eliminar
        user_to_delete = self.get_object()
        
        # 1. EVITAR AUTO-ELIMINACIÓN
        if user_to_delete.id == request.user.id:
            messages.error(request, "¡Operación cancelada! No puedes eliminar tu propia cuenta de administrador.")
            return redirect('apy:registro_usuario_lista')
            
        # 2. EVITAR ELIMINAR AL ÚLTIMO ADMIN
        if user_to_delete.is_superuser:
            total_admins = User.objects.filter(is_superuser=True).count()
            if total_admins <= 1:
                messages.error(request, "No puedes eliminar al único administrador del sistema.")
                return redirect('apy:registro_usuario_lista')
                
        return super().dispatch(request, *args, **kwargs)
    

# 4. VISTA DE LISTADO (RegistroUsuarioListView) - PROTEGIDA

# Ahora heredamos de la clase SuperuserRequiredMixin
class RegistroUsuarioListView(SuperuserRequiredMixin, ListView):
    model = User 
    template_name = 'registro_usuarios/listar_registro_usuarios.html' 
    context_object_name = 'object_list' 
    
    # --- Configuración de Permisos ---
    module_name = 'GestionUsuarios'
    permission_required = 'view'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['crear_url'] = reverse_lazy('apy:registro_usuario_crear') 
        context['entidad'] = 'Usuarios'
        context['titulo'] = 'Gestión de Usuarios'
        return context
    
class EmpleadoCreateModalView(CreateView):
    model = Profile
    form_class = ProfileForm
    template_name = "registro_usuarios/modal_empleado.html"

    def form_valid(self, form):
        try:
            with translation.atomic():
                # 1. Creamos un usuario básico vinculado a la identificación
                ident = form.cleaned_data['identificacion']
                user, created = User.objects.get_or_create(
                    username=ident,
                    defaults={
                        'first_name': 'Empleado',
                        'last_name': ident,
                        'is_active': True
                    }
                )
                
                # 2. Vinculamos el usuario al perfil antes de guardar
                self.object = form.save(commit=False)
                self.object.user = user
                self.object.save()

            return JsonResponse({
                "success": True,
                "id": self.object.id,
                "text": f"{self.object.identificacion} - {self.object.telefono}",
                "message": "Empleado registrado correctamente ✅"
            })
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=500)

    def form_invalid(self, form):
        # Asegúrate de que render_to_string esté importado arriba
        html = render_to_string(self.template_name, {"form": form}, request=self.request)
        return JsonResponse({
            "success": False,
            "html": html,
            "message": "Por favor, corrige los errores ❌"
        })