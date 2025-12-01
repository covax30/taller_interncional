from django.shortcuts import render, redirect, reverse
from apy.models import Module, Permission 
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import transaction
# IMPORTACIONES NECESARIAS PARA PROTEGER LA VISTA
from django.contrib.auth.decorators import login_required 
from apy.decorators import permiso_requerido_fbv # <-- Usamos el decorador FBV

# Usamos el decorador de función que lanza el 403
# Requerimos el permiso 'view' para el módulo 'Permisos'
@permiso_requerido_fbv(module_name='Permisos', permission_required='view')
def permisos_usuarios(request):
    user_to_edit = None
    
    # --- 1. Obtener posibles fuentes del ID de usuario ---
    user_id_from_select = request.POST.get('user') 
    user_id_from_hidden = request.POST.get('user_id_to_edit') 
    user_id_from_get = request.GET.get('user_id')  
    
    selected_user_id = user_id_from_select or user_id_from_hidden or user_id_from_get

    # --- 2. Determinar el tipo de acción (CLAVE) ---
    is_post = request.method == 'POST'
    is_save_action = is_post and 'save_permissions' in request.POST 

    # --- 3. Guardado de permisos ---
    # NOTA: No se requiere una protección 'add/change' aquí porque 
    # solo los superusuarios o aquellos con permisos de 'Permisos:view' 
    # pueden acceder a esta URL, y la lógica de guardado está dentro.
    if is_save_action:
        user_id_to_save = user_id_from_hidden 
        
        try:
            user_to_edit = User.objects.get(id=user_id_to_save)
        except User.DoesNotExist:
            messages.error(request, "Error: el usuario no existe.")
            return redirect('apy:permisos_usuarios')

        try:
            with transaction.atomic():
                # Borramos permisos previos del usuario
                Permission.objects.filter(user=user_to_edit).delete()

                for module in Module.objects.all():
                    view_perm = f'perm_{module.id}_view' in request.POST
                    add_perm = f'perm_{module.id}_add' in request.POST
                    change_perm = f'perm_{module.id}_change' in request.POST
                    delete_perm = f'perm_{module.id}_delete' in request.POST

                    if view_perm or add_perm or change_perm or delete_perm:
                        Permission.objects.create(
                            user=user_to_edit,
                            module=module,
                            view=view_perm,
                            add=add_perm,
                            change=change_perm,
                            delete=delete_perm
                        )

            messages.success(request, f"Permisos del usuario {user_to_edit.username} guardados con éxito. ✅")
            return redirect(f"{reverse('apy:permisos_usuarios')}?user_id={user_to_edit.id}")

        except Exception as e:
            messages.error(request, f"Error al guardar permisos: {e}")
            return redirect(f"{reverse('apy:permisos_usuarios')}?user_id={user_to_edit.id}")

    # --- 4. Carga del usuario seleccionado/por defecto (GET o POST sin acción de guardar) ---
    if selected_user_id:
        try:
            user_to_edit = User.objects.get(id=selected_user_id)
        except User.DoesNotExist:
            user_to_edit = None

    if not user_to_edit:
        user_to_edit = User.objects.first()
        if not user_to_edit:
            messages.warning(request, "No hay usuarios registrados para gestionar permisos.")
            return render(request, 'Permisos/permisos.html', {'users': [], 'modules': []})

    # --- 5. Construcción del contexto (Igual que antes) ---
    all_users = User.objects.all().order_by('username')
    modules = Module.objects.all()

    for module in modules:
        permissions = Permission.objects.filter(user=user_to_edit, module=module).first()
        module.current_permissions = {
            'view': permissions.view if permissions else False,
            'add': permissions.add if permissions else False,
            'change': permissions.change if permissions else False,
            'delete': permissions.delete if permissions else False,
        }

    context = {
        'users': all_users,
        'modules': modules,
        'user_to_edit': user_to_edit,
        'titulo': 'Administración de Permisos'
    }

    return render(request, 'Permisos/permisos.html', context)