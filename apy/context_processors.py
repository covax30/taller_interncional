# apy/context_processors.py
from apy.models import Permission, Module

def user_permissions(request):
    # Si el usuario no está logueado, devolvemos un dict vacío para no romper el template
    if not request.user or not request.user.is_authenticated:
        return {'user_perms': {}}

    if request.user.is_superuser:
        return {'user_perms': 'all'}
    
    perms_dict = {}
    # Traemos los permisos del usuario
    permissions = Permission.objects.filter(user=request.user).select_related('module')
    
    for p in permissions:
        perms_dict[p.module.name] = {
            'view': p.view,
            'add': p.add,
            'change': p.change,
            'delete': p.delete
        }
    
    return {'user_perms': perms_dict}