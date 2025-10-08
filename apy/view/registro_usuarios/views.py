# apy/view/registro_usuarios/views.py

from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib import messages
from apy.forms import RegistroUsuarioForm # Formulario Unificado (para CreateView y UpdateView)

# ====================================================================
# 1. VISTA DE CREACIÓN (RegistroUsuarioCreateView)
# ====================================================================

class RegistroUsuarioCreateView(CreateView):
    model = User
    form_class = RegistroUsuarioForm
    template_name = 'registro_usuarios/registro_usuarios.html' 
    # 🟢 CORREGIDO: URL correcta de listado
    success_url = reverse_lazy('apy:registro_usuario_lista') 

    def form_valid(self, form):
        # El método save del formulario maneja la creación y el rol
        response = super().form_valid(form)
        messages.success(self.request, form.success_message) 
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Registro de Nuevo Usuario'
        context['entidad'] = 'Usuarios'
        context['listar_url'] = reverse_lazy('apy:registro_usuario_lista') 
        return context

# ====================================================================
# 2. VISTA DE ACTUALIZACIÓN (RegistroUpdateView)
# ====================================================================

class RegistroUpdateView(UpdateView):
    model = User
    form_class = RegistroUsuarioForm # Usa el formulario unificado
    template_name = 'registro_usuarios/registro_usuarios.html' 
    success_url = reverse_lazy('apy:registro_usuario_lista') 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Usuario'
        context['entidad'] = 'Usuarios'
        context['listar_url'] = reverse_lazy('apy:registro_usuario_lista')
        return context

    def form_valid(self, form):
        # 🟢 IMPLEMENTACIÓN CRÍTICA para el formulario unificado:
        # Llamamos al save del formulario que contiene la lógica para 
        # actualizar el rol (is_superuser/is_staff) y la contraseña (si fue cambiada).
        self.object = form.save() 
        messages.success(self.request, "Usuario actualizado correctamente.")
        # Usamos redirect para asegurar que el mensaje se muestre después del guardado
        return super().form_valid(form)

# ====================================================================
# 3. VISTA DE ELIMINACIÓN (RegistroDeleteView)
# ====================================================================

class RegistroDeleteView(DeleteView):
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
    
# ====================================================================
# 4. VISTA DE LISTADO (RegistroUsuarioListView)
# ====================================================================

class RegistroUsuarioListView(ListView):
    model = User 
    template_name = 'registro_usuarios/listar_registro_usuarios.html' 
    context_object_name = 'object_list' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # CORRECCIÓN: El nombre correcto es 'registro_usuario_crear'
        context['crear_url'] = reverse_lazy('apy:registro_usuario_crear') 
        context['entidad'] = 'Usuarios'
        return context
