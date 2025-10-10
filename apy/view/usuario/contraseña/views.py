from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib import messages
from apy.forms import PerfilUsuarioForm  # Asegúrate de importar tu formulario de perfil

class PerfilPasswordChangeView(PasswordChangeView):

    template_name = 'usuario/usuario.html'
    
    # Redirecciona a la misma vista de perfil en caso de éxito
    success_url = reverse_lazy('apy:perfil_usuarios') 
    
    # Función para manejar el éxito (ya la tenías)
    def form_valid(self, form):
        messages.success(self.request, "Tu contraseña ha sido cambiada con éxito.")
        return super().form_valid(form)
        

    # para renderizar la plantilla 'usuario/usuario.html'
    def get_context_data(self, **kwargs):
        # Llama a la implementación base para obtener el formulario de contraseña (que tendrá los errores)
        context = super().get_context_data(**kwargs)
        
        # Agrega el contexto que requiere la plantilla de perfil:
        context['user'] = self.request.user 
        
        # Pasa el formulario de edición de perfil, incluso si no estamos usándolo en este POST
        # Usamos PerfilUsuarioForm, el formulario que maneja los datos (nombre, email, etc.)
        context['form'] = PerfilUsuarioForm(instance=self.request.user)
        
        # El formulario de contraseña (con los errores) ya está en 'context' con la clave 'form'.
        # Para evitar conflictos con tu plantilla que usa 'password_form', necesitamos renombrar:
        context['password_form'] = context.pop('form')
        
        return context


    def form_invalid(self, form):
        # Esto asegura que si la validación falla, se renderice la plantilla con el contexto completo.
        # Esencialmente, llama a get_context_data y renderiza la plantilla.
        return self.render_to_response(self.get_context_data(form=form))