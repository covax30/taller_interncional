from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from apy.forms import UserProfileForm

def perfil_usuario(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('apy:perfil_usuario')  # Actualiza con el nombre correcto de la vista
    else:
        form = UserProfileForm(instance=user)
    
    return render(request, 'Usuario/usuario.html', {'form': form})  # Ruta correcta

