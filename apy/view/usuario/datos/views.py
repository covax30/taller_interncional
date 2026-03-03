from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View, TemplateView
from django.contrib.auth.forms import PasswordChangeForm 
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin

# Importar tus formularios y modelos
from apy.forms import PerfilUsuarioForm, ProfileForm 
from apy.models import Profile 

class PerfilEditarView(LoginRequiredMixin, View):
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
            # 1. Detectar si el POST es para cambiar CONTRASEÑA
            if 'old_password' in request.POST:
                password_form = PasswordChangeForm(user=request.user, data=request.POST)
                if password_form.is_valid():
                    user = password_form.save()
                    update_session_auth_hash(request, user)
                    messages.success(request, "¡Contraseña actualizada con éxito!")
                    return redirect(self.success_url)
                else:
                    # Si falla el password, recargamos con errores
                    return render(request, self.template_name, {
                        'form': self.get_user_form(),
                        'profile_form': self.get_profile_form(),
                        'password_form': password_form,
                    })

            # 2. Lógica para DATOS PERSONALES
            user_form = self.get_user_form(request.POST)
            profile_form = self.get_profile_form(request.POST, request.FILES)

            if user_form.is_valid() and profile_form.is_valid():
                try:
                    with transaction.atomic():
                        user_form.save()
                        profile_form.save()
                    messages.success(request, "Perfil actualizado correctamente.")
                    return redirect(self.success_url)
                except Exception as e:
                    messages.error(request, f"Error al guardar: {e}")
            
            # 3. Si llega aquí es porque hubo errores de validación (campos vacíos, etc)
            messages.error(request, "Por favor, corrige los errores en el formulario.")
            return render(request, self.template_name, {
                'form': user_form,
                'profile_form': profile_form,
                'password_form': self.get_password_form(),
            })
        

class ActualizarPerfilImagenView(LoginRequiredMixin, View):
    success_url = reverse_lazy('apy:editar_usuario') 

    def post(self, request, *args, **kwargs):
        # 1. Obtenemos el perfil
        profile_instance, _ = Profile.objects.get_or_create(user=request.user)
        
        # 2. Lógica para ELIMINAR la imagen
        if request.POST.get('imagen_clear') == 'on':
            if profile_instance.imagen:
                # Borra el archivo físico y pone el campo en NULL
                profile_instance.imagen.delete(save=False) 
                profile_instance.imagen = None
                profile_instance.save(update_fields=['imagen']) 
            
            messages.success(request, "Imagen eliminada. Ahora verás tu avatar de rol.")
            return redirect(self.success_url)

        # 3. Lógica para SUBIR/ACTUALIZAR imagen
        if 'imagen' in request.FILES:
            profile_instance.imagen = request.FILES['imagen']
            
            try:
                profile_instance.save(update_fields=['imagen'])
                messages.success(request, "¡Imagen de perfil actualizada!")
            except Exception as e:
                messages.error(request, f"Error al guardar la imagen: {e}")
            
            return redirect(self.success_url)

        # Si llegan aquí sin enviar nada
        messages.warning(request, "No se seleccionó ninguna imagen.")
        return redirect(self.success_url)
    

class PerfilPasswordChangeDoneView(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        messages.success(request, "¡Contraseña cambiada con éxito!")
        return redirect('apy:editar_usuario')