from builtins import Exception, any

from django.shortcuts import render, redirect, reverse
from apy.models import Module, Permission 
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required 
from apy.decorators import permiso_requerido_fbv

@login_required
@permiso_requerido_fbv(module_name='Permisos', permission_required='view')
def permisos_usuarios(request):
    user_to_edit = None
    selected_user_id = request.POST.get('user') or request.POST.get('user_id_to_edit') or request.GET.get('user_id')

    # --- Lógica de Guardado ---
    if request.method == 'POST' and 'save_permissions' in request.POST:
        user_id_to_save = request.POST.get('user_id_to_edit')
        try:
            user_to_edit = User.objects.get(id=user_id_to_save)
            if user_to_edit.is_superuser:
                messages.error(request, "No se pueden alterar los permisos de un Administrador.")
            else:
                with transaction.atomic():
                    Permission.objects.filter(user=user_to_edit).delete()
                    for module in Module.objects.all():
                        v = f'perm_{module.id}_view' in request.POST
                        a = f'perm_{module.id}_add' in request.POST
                        c = f'perm_{module.id}_change' in request.POST
                        d = f'perm_{module.id}_delete' in request.POST
                        if any([v, a, c, d]):
                            Permission.objects.create(user=user_to_edit, module=module, view=v, add=a, change=c, delete=d)
                messages.success(request, f"Permisos de {user_to_edit.username} guardados. ✅")
            return redirect(f"{reverse('apy:permisos_usuarios')}?user_id={user_to_edit.id}")
        except Exception as e:
            messages.error(request, f"Error: {e}")

    # --- Carga de Usuario ---
    if selected_user_id:
        user_to_edit = User.objects.filter(id=selected_user_id).first()
    
    if not user_to_edit:
        # Evitar errores si no hay usuarios, pero priorizar el primero no-superuser si existe
        user_to_edit = User.objects.filter(is_superuser=False).first() or User.objects.first()

    # --- Estructura basada en tu nuevo Sidebar ---
    # Las llaves son los "Super Items" y las listas son los nombres de los módulos en la DB
    menu_estructurado = {
        "Análisis y Reportes": [
            {"nombre": "Estadísticas Generales", "module": "EstadisticasGenerales"},
            {"nombre": "Informes", "module": "Informes"},
        ],
        "Gestión de Vehículos": [
            {"nombre": "Entrada de Vehículo", "module": "EntradaVehiculos"},
            {"nombre": "Salida de Vehículo", "module": "SalidaVehiculos"},
            {"nombre": "Vehículos", "module": "Vehiculos"},
            {"nombre": "Marcas", "module": "Marca"},
        ],
        "Mantenimiento y Repuestos": [
            {"nombre": "Gestión de Mantenimientos", "module": "GestionMantenimiento"},
            {"nombre": "Gestión de Repuestos", "module": "Repuestos"},
            {"nombre": "Tipos de Mantenimiento", "module": "TipoMantenimientos"},
            {"nombre": "Herramientas", "module": "Herramientas"},
            {"nombre": "Gestión de Insumos", "module": "Insumos"},
        ],
        "Administración": [
            {"nombre": "Gastos", "module": "Gastos"},
            {"nombre": "Factura", "module": "Factura"},
            {"nombre": "Pagos", "module": "Pagos"},
            {"nombre": "Caja", "module": "Caja"},
            {"nombre": "Servicios Públicos", "module": "PagoServicios"},
        ],
        "Gestión de Clientes": [
            {"nombre": "Proveedores", "module": "Proveedor"},
            {"nombre": "Clientes", "module": "Clientes"},
        ],
        "Gestión y Seguridad": [
            {"nombre": "Gestión de Usuarios", "module": "GestionUsuarios"},
            {"nombre": "Permisos", "module": "Permisos"},
            {"nombre": "Respaldos", "module": "Respaldos"},
        ]
    }
    
    modulos_agrupados = {}
    ids_procesados = []

    if user_to_edit:
        for categoria, items in menu_estructurado.items():
            lista_objs = []
            for item in items:
                # Buscamos por el nombre técnico que definimos arriba
                m = Module.objects.filter(name=item['module']).first()
                if m and m.id not in ids_procesados:
                    p = Permission.objects.filter(user=user_to_edit, module=m).first()
                    m.current_permissions = {
                        'view': p.view if p else False,
                        'add': p.add if p else False,
                        'change': p.change if p else False,
                        'delete': p.delete if p else False,
                    }
                    lista_objs.append(m)
                    ids_procesados.append(m.id)
            
            if lista_objs:
                modulos_agrupados[categoria] = lista_objs

        # Módulos huérfanos
        otros = Module.objects.exclude(id__in=ids_procesados)
        if otros.exists():
            lista_otros = []
            for m in otros:
                p = Permission.objects.filter(user=user_to_edit, module=m).first()
                m.current_permissions = {
                    'view': p.view if p else False, 
                    'add': p.add if p else False, 
                    'change': p.change if p else False, 
                    'delete': p.delete if p else False
                }
                lista_otros.append(m)
            modulos_agrupados["Módulos Adicionales (Revisar)"] = lista_otros

        # Módulos huérfanos (por si olvidaste alguno en la lista de arriba)
        otros = Module.objects.exclude(id__in=ids_procesados)
        if otros.exists():
            lista_otros = []
            for m in otros:
                p = Permission.objects.filter(user=user_to_edit, module=m).first()
                m.current_permissions = {
                    'view': p.view if p else False, 
                    'add': p.add if p else False, 
                    'change': p.change if p else False, 
                    'delete': p.delete if p else False
                }
                lista_otros.append(m)
            modulos_agrupados["Módulos Adicionales (Sin Categoría)"] = lista_otros

    context = {
        'users': User.objects.all().order_by('username'),
        'user_to_edit': user_to_edit,
        'modulos_agrupados': modulos_agrupados,
        'titulo': 'Administración de Permisos'
    }
    return render(request, 'Permisos/permisos.html', context)