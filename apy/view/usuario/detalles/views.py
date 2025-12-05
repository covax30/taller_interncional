# apy/views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from apy.models import Profile 

@login_required
def datos_usuario(request):
    """
    Vista para mostrar los detalles del perfil del usuario (solo lectura).
    Recupera los datos del modelo User y el campo 'telefono' del modelo Profile asociado.
    """
    user = request.user
    
    # 1. Recuperar el campo 'telefono' del modelo Profile
    telefono_valor = "(No Registrado)"
    
    try:
        # Intenta acceder al objeto Profile que está vinculado al usuario
        profile = user.profile
        
        # Usa el valor del teléfono si existe, si no, usa el mensaje por defecto
        if profile.telefono:
            telefono_valor = profile.telefono
            
    except Profile.DoesNotExist:
        pass
    
    # 2. Configurar el contexto
    context = {
        'user': user,
        'telefono_valor': telefono_valor, 
    }
    
    # 3. Renderizar la plantilla de detalles
    return render(request, 'usuario/usuario.html', context)