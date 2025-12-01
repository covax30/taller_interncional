from django.shortcuts import render, redirect
from django.db.models.functions import TruncMonth
from django.db.models import Sum
from datetime import datetime
from calendar import month_name
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied # <-- NUEVA IMPORTACIÓN PARA ERRORES 403
from apy.models import Caja, Module, Permission 
from apy.decorators import PermisoRequeridoMixin

from django.http import HttpResponse


# LÓGICA DE PERMISOS PARA VISTAS BASADAS EN FUNCIÓN (Lanza 403)

def check_custom_permission(user, module_name, permission_required):
    """
    Verifica si un usuario tiene el permiso requerido para un módulo específico.
    Si no lo tiene, lanza PermissionDenied (Error 403).
    Si tiene permiso, retorna None.
    """
    # 1. Permitir Superusuario
    if user.is_superuser:
        return None # Permiso concedido
    
    # 2. Lógica de Permisos Personalizados
    try:
        module = Module.objects.get(name=module_name)
        permission_obj = Permission.objects.filter(user=user, module=module).first()
        
        has_permission = False
        if permission_obj:
            # Usa getattr para verificar el permiso (ej: permission_obj.view)
            has_permission = getattr(permission_obj, permission_required, False)
            
        if has_permission:
            return None # Permiso concedido
        else:
            # Lanza la excepción PermissionDenied, que Django maneja como 403
            raise PermissionDenied(
                f"Acceso denegado. No tienes permiso de {permission_required.upper()} para el módulo '{module_name}'."
            )
            
    except Module.DoesNotExist:
        # Lanza la excepción indicando un error de configuración
        raise PermissionDenied(
            f"Error de configuración: Módulo '{module_name}' no encontrado."
        )


@login_required(login_url=reverse_lazy('apy:login'))
def estadisticas(request):
    
    # --- 1. VERIFICACIÓN DE PERMISOS PERSONALIZADOS ---
    try:
        check_custom_permission(
            request.user, 
            module_name='Caja', 
            permission_required='view'
        )
    except PermissionDenied as e:
        # Si la excepción es capturada, puedes usar messages antes de redirigir
        # o simplemente dejar que el manejador 403 de Django actúe.
        # Aquí elegimos redirigir con un mensaje para el flujo de UX (User Experience).
        messages.warning(request, str(e))
        return redirect(reverse_lazy('apy:caja_lista')) # Usamos la lista de caja como fallback
        

    # Filtramos solo los ingresos
    ingresos_por_mes = (
        Caja.objects
        .filter(tipo_movimiento='Ingreso')  # Filtra solo los movimientos de ingreso
        .annotate(mes=TruncMonth('fecha'))
        .values('mes')
        .annotate(total=Sum('monto'))
        .order_by('mes')
    )

    meses = []
    totales = []

    for ingreso in ingresos_por_mes:
        mes_num = ingreso['mes'].month
        # NOTA: month_name devuelve nombres de meses en inglés. 
        # Si necesitas español, considera usar un array predefinido de meses en español.
        meses.append(month_name[mes_num])  # convierte 1 → "January"
        totales.append(float(ingreso['total']))

    context = {
        'meses': meses,
        'totales': totales,
        'titulo': 'Estadísticas de Ingresos',
        'entidad': 'Caja'
    }

    return render(request, 'estadisticas.html', context)