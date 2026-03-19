from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from django.views import View
from django.contrib.auth import update_session_auth_hash

# Importar tus formularios y modelos
from apy.forms import PerfilUsuarioForm, ProfileForm 
from apy.models import Profile 

class PerfilPasswordChangeView(PasswordChangeView):
    template_name = 'usuario/editar_usuario.html'
    success_url = reverse_lazy('apy:editar_usuario') 
    
    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)        
        # 1. Renombrar el formulario para que coincida con tu HTML
        context['password_form'] = context.pop('form')
        
        # 2. Inyectar los otros formularios para mantener la UI completa
        profile_instance, _ = Profile.objects.get_or_create(user=self.request.user)
        context['form'] = PerfilUsuarioForm(instance=self.request.user)
        context['profile_form'] = ProfileForm(instance=profile_instance)
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        update_session_auth_hash(self.request, form.user)
        messages.success(self.request, "Tu contraseña ha sido cambiada con éxito.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Error al cambiar la contraseña. Por favor, revisa los requisitos.")
        return self.render_to_response(self.get_context_data(form=form))

# Vista para manejar el redireccionamiento tras el éxito
class PerfilPasswordChangeDoneView(View):
    def get(self, request, *args, **kwargs):
        messages.success(request, "¡Contraseña actualizada con éxito!")
        return redirect('apy:editar_usuario')