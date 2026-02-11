# apy/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View # Usamos View en lugar de UpdateView para manejar dos formularios
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm 
from django.contrib.auth.mixins import LoginRequiredMixin

# Importamos los modelos y formularios necesarios
from apy.models import Profile # ¡Asegúrate de que este import sea correcto!
from apy.forms import PerfilUsuarioForm, ProfileForm 
# Importamos ProfileForm si usas la solución de dos formularios

# -----------------------------------------------------------------
# VISTA DE EDICIÓN (MANEJA DOS FORMULARIOS: User y Profile)
# -----------------------------------------------------------------
class PerfilUsuarioUpdateView(LoginRequiredMixin, View):
    template_name = 'usuario/editar_usuario.html'
    success_url = reverse_lazy('apy:editar_usuario') 
    
    def get(self, request, *args, **kwargs):
        # 1. Obtener los formularios con datos actuales
        user_form = PerfilUsuarioForm(instance=request.user)
        password_form = PasswordChangeForm(request.user)
        
        # 2. Obtener la instancia del Profile (o crearlo si no existe)
        profile_instance, created = Profile.objects.get_or_create(user=request.user)
        profile_form = ProfileForm(instance=profile_instance)
        
        context = {
            'user': request.user, # Necesario para la barra lateral
            'form': user_form, # Formulario de datos de Usuario
            'password_form': password_form, # Formulario de Contraseña
            'profile_form': profile_form, # Formulario del Teléfono (Profile)
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user_form = PerfilUsuarioForm(request.POST, instance=request.user)
        password_form = PasswordChangeForm(request.user, request.POST)
        
        profile_instance, created = Profile.objects.get_or_create(user=request.user)
        profile_form = ProfileForm(request.POST, instance=profile_instance)
        
        # Bandera para rastrear si al menos un formulario de datos es válido
        forms_valid = True
        
        # 1. Validar y guardar PerfilUsuarioForm (Nombre, Email, etc.)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, "Los datos de usuario han sido actualizados.")
        else:
            forms_valid = False
        
        # 2. Validar y guardar ProfileForm (Teléfono)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, "La información de contacto ha sido actualizada.")
        else:
            forms_valid = False

        # NOTA: El cambio de contraseña requiere un manejo especial y una URL/Vista separada,
        # pero para que no lance un error aquí si se envían datos inválidos, 
        # mantenemos el formulario para que se muestren los errores en el GET.
        
        if forms_valid:
            return redirect(self.success_url)
        
        # Si alguno falló, volvemos a renderizar con errores
        context = {
            'user': request.user,
            'form': user_form,
            'password_form': password_form, # Pasa el formulario de contraseña para que se muestre vacío/con errores
            'profile_form': profile_form,
        }
        return render(request, self.template_name, context)

# -----------------------------------------------------------------
# VISTA DE DETALLE (SOLO LECTURA) - Asumiendo que es una función
# -----------------------------------------------------------------
# def datos_usuario(request):
#     # Aquí podrías obtener el perfil para mostrar el teléfono
#     try:
#         telefono = request.user.profile.telefono
#     except Profile.DoesNotExist:
#         telefono = "(No Registrado)"
        
#     context = {
#         'user': request.user,
#         'telefono_perfil': telefono
#     }
#     return render(request, 'usuario/usuario.html', context)