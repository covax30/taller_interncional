from django.shortcuts import render, redirect
from django.db.models.functions import TruncMonth
from django.db.models import Sum
from datetime import datetime
from calendar import month_name
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from apy.models import Caja, Module, Permission # Importamos Module y Permission
from apy.decorators import PermisoRequeridoMixin
from django.urls import reverse_lazy

from django.http import HttpResponse

# ************************************************
# LÓGICA DE PERMISOS PARA VISTAS BASADAS EN FUNCIÓN
# ************************************************

def check_custom_permission(user, module_name, permission_required, redirect_url_name='home'):
    """
    Verifica si un usuario tiene el permiso requerido para un módulo específico.
    Si no lo tiene, retorna una respuesta de redirección con un mensaje de error.
    Si tiene permiso, retorna None.
    """
    if user.is_superuser:
        return None # Permiso concedido
    
    try:
        module = Module.objects.get(name=module_name)
        permission_obj = Permission.objects.filter(user=user, module=module).first()
        
        has_permission = False
        if permission_obj:
            has_permission = getattr(permission_obj, permission_required, False)
            
        if has_permission:
            return None # Permiso concedido
        else:
            messages.warning(user, f"Acceso denegado. No tienes permiso de {permission_required.upper()} para el módulo '{module_name}'.")
            # Redirigir a una página de inicio o lista por defecto
            return redirect(reverse_lazy(redirect_url_name)) 
            
    except Module.DoesNotExist:
        messages.error(user, f"Error de configuración: Módulo '{module_name}' no encontrado.")
        return redirect(reverse_lazy(redirect_url_name)) 


# Usaremos la lista de caja como URL de redirección en caso de denegación.
REDIRECT_ON_DENIAL = 'apy:caja_lista' 


@login_required(login_url='/login/') # Asegura que el usuario esté autenticado
def estadisticas(request):
    
    # --- 1. VERIFICACIÓN DE PERMISOS PERSONALIZADOS ---
    permission_denied_response = check_custom_permission(
        request.user, 
        module_name='Caja', 
        permission_required='view', # Se asume 'view' para estadísticas
        redirect_url_name=REDIRECT_ON_DENIAL
    )
    if permission_denied_response:
        return permission_denied_response
    # --------------------------------------------------
    
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
        # Si necesitas español, deberás usar una configuración regional (locale) o un array de meses en español.
        meses.append(month_name[mes_num])  # convierte 1 → "January"
        totales.append(float(ingreso['total']))

    context = {
        'meses': meses,
        'totales': totales,
        'titulo': 'Estadísticas de Ingresos',
        'entidad': 'Caja'
    }

    return render(request, 'estadisticas.html', context)