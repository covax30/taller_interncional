from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View, TemplateView
from django.contrib.auth.forms import PasswordChangeForm 
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash

# Importar tus formularios y modelos
from apy.forms import PerfilUsuarioForm, ProfileForm 
from apy.models import Profile 

@method_decorator(login_required, name='dispatch')
class PerfilEditarView(View):
    template_name = 'usuario/editar_usuario.html' 
    success_url = reverse_lazy('apy:editar_usuario') 

    def get_user_form(self, data=None):
        return PerfilUsuarioForm(data=data, instance=self.request.user)

    def get_profile_form(self, data=None, files=None):
        # Usamos get_or_create para evitar errores si el perfil no existe
        profile_instance, _ = Profile.objects.get_or_create(user=self.request.user)
        return ProfileForm(data=data, files=files, instance=profile_instance)
    
    def get_password_form(self):
        return PasswordChangeForm(user=self.request.user) 

    def get(self, request, *args, **kwargs):
        context = {
            'form': self.get_user_form(), 
            'profile_form': self.get_profile_form(), 
            'password_form': self.get_password_form(),
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user_form = self.get_user_form(request.POST)
        profile_form = self.get_profile_form(request.POST, request.FILES) 
    
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            # Verificamos si se marcó la eliminación (el name debe ser 'imagen_clear')
            if request.POST.get('imagen_clear') == 'on':
                messages.success(request, "Datos actualizados e imagen de perfil eliminada (ahora ves la imagen por defecto).")
            else:
                messages.success(request, "Datos de perfil y foto actualizados con éxito.")
        
            return redirect(self.success_url)
        
        else:
            context = {
                'form': user_form,
                'profile_form': profile_form,
                'password_form': self.get_password_form(), 
            }
            messages.error(request, "Error al guardar los datos. Revisa los campos marcados.")
            return render(request, self.template_name, context)

@method_decorator(login_required, name='dispatch')
class ActualizarPerfilImagenView(View):
    success_url = reverse_lazy('apy:editar_usuario') 

    def post(self, request, *args, **kwargs):
        profile_instance, _ = Profile.objects.get_or_create(user=request.user)
        
        if request.POST.get('imagen_clear') == 'on':
            if profile_instance.imagen:
                profile_instance.imagen.delete(save=True) # Borra archivo físico y limpia el campo
            messages.success(request, "Imagen eliminada. Se ha restaurado la imagen por defecto.")
            return redirect(self.success_url)

    # Si no es borrar, procesamos la subida normal
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile_instance)
        if profile_form.is_valid():
            profile_form.save() 
            messages.success(request, "¡Imagen de perfil actualizada!")
            return redirect(self.success_url)
        else:
            # Reutilizamos la lógica de carga para no perder el contexto en caso de error
            user_form = PerfilUsuarioForm(instance=request.user)
            password_form = PasswordChangeForm(request.user)
            context = {
                'form': user_form,
                'profile_form': profile_form,
                'password_form': password_form,
            }
            messages.error(request, "No se pudo procesar la imagen. Inténtalo de nuevo.")
            return render(request, 'usuario/editar_usuario.html', context)

@method_decorator(login_required, name='dispatch')
class PerfilPasswordChangeDoneView(TemplateView):
    def get(self, request, *args, **kwargs):
        messages.success(request, "¡Contraseña cambiada con éxito!")
        return redirect('apy:editar_usuario')