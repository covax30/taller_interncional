from django.views.generic import UpdateView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm 

# Importar el Mixin necesario para requerir login
from django.contrib.auth.mixins import LoginRequiredMixin
from apy.decorators import PermisoRequeridoMixin
from apy.forms import PerfilUsuarioForm


# Heredamos de LoginRequiredMixin primero para asegurar la protección
class PerfilUsuarioUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = PerfilUsuarioForm 
    template_name = 'usuario/usuario.html' 
    success_url = reverse_lazy('apy:perfil_usuarios') 
    
    # Redirige a la página de login si el usuario no está autenticado
    login_url = '/login/' 

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
        messages.success(self.request, "Tu perfil ha sido actualizado con éxito. ✨")
        return super().form_valid(form)