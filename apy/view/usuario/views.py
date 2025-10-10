# apy/view/registro_usuarios/views.py

from django.views.generic import UpdateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib import messages
from apy.forms import PerfilUsuarioForm
from django.contrib.auth.forms import PasswordChangeForm # Para el formulario de cambio de contraseña
from apy.forms import PerfilUsuarioForm

# La clase PerfilUsuarioUpdateView debe ir en tu archivo de vistas.

class PerfilUsuarioUpdateView(UpdateView):
    model = User
    # Utiliza el formulario simplificado que creamos (sin campos de rol/contraseña)
    form_class = PerfilUsuarioForm 
    
    # Apunta a la plantilla HTML que proporcionaste y corregimos
    template_name = 'usuario/usuario.html' 
    
    # Redirige a la misma vista de perfil después de guardar
    success_url = reverse_lazy('apy:perfil_usuarios') 

    def get_object(self):
        """Método CRÍTICO: Asegura que el objeto a editar sea el usuario actual."""
        # Esto pre-rellena el formulario con los datos del usuario logueado.
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # 1. 'user': Pasa el objeto User completo para la columna de información lateral
        context['user'] = self.request.user 
        
        # 2. 'password_form': Pasa el formulario de cambio de contraseña de Django
        # para la columna de la derecha.
        context['password_form'] = PasswordChangeForm(self.request.user)
        
        return context
    
    def form_valid(self, form):
        # Muestra un mensaje de éxito después de guardar el perfil
        messages.success(self.request, "Tu perfil ha sido actualizado con éxito.")
        return super().form_valid(form)