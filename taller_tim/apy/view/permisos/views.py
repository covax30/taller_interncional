from django.shortcuts import render
from apy.models import Module, Permission
from django.contrib.auth.models import User

def permisos_usuarios(request):
    # Obtener todos los usuarios
    users = User.objects.all()
    reverse_lazy = lambda x: x  # Placeholder for reverse_lazy if needed
    # Obtener todos los módulos
    modules = Module.objects.all()

    # Consultar los permisos para el usuario actual
    user_permissions = {}
    for module in modules:
        permissions = Permission.objects.filter(user=request.user, module=module).first()
        if permissions:
            user_permissions[module.id] = {
                'view': permissions.view,
                'add': permissions.add,
                'change': permissions.change,
                'delete': permissions.delete
            }
        else:
            # Si no tiene permisos, asignamos valores predeterminados
            user_permissions[module.id] = {
                'view': False,
                'add': False,
                'change': False,
                'delete': False
            }

    return render(request, 'Permisos/permisos.html', {
        'users': users,
        'modules': modules,
        'user_permissions': user_permissions,  # Pasar permisos de manera explícita
    })
