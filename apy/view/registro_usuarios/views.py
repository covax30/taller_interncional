from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib import messages
from apy.forms import RegistroUsuarioForm 
from apy.decorators import PermisoRequeridoMixin

# MIXINS DE PROTECCIÓN
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

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

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, form.success_message) 
        return response

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Usuario'
        context['entidad'] = 'Usuarios'
        context['listar_url'] = reverse_lazy('apy:registro_usuario_lista')
        return context

    def form_valid(self, form):
        self.object = form.save() 
        messages.success(self.request, "Usuario actualizado correctamente.")
        return super().form_valid(form)


# 3. VISTA DE ELIMINACIÓN (RegistroDeleteView) - PROTEGIDA

# Ahora heredamos de la clase SuperuserRequiredMixin
class RegistroDeleteView(SuperuserRequiredMixin, DeleteView):
    model = User
    template_name = 'registro_usuarios/eliminar_registro_usuarios.html'
    success_url = reverse_lazy('apy:registro_usuario_lista') 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Usuario'
        context['entidad'] = 'Usuarios'
        context['listar_url'] = reverse_lazy('apy:registro_usuario_lista')
        return context
    
    def form_valid(self, form):
        messages.success(self.request, f"Usuario '{self.object.username}' eliminado correctamente.")
        return super().form_valid(form)

# 4. VISTA DE LISTADO (RegistroUsuarioListView) - PROTEGIDA

# Ahora heredamos de la clase SuperuserRequiredMixin
class RegistroUsuarioListView(SuperuserRequiredMixin, ListView):
    model = User 
    template_name = 'registro_usuarios/listar_registro_usuarios.html' 
    context_object_name = 'object_list' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['crear_url'] = reverse_lazy('apy:registro_usuario_crear') 
        context['entidad'] = 'Usuarios'
        return context