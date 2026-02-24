from django.shortcuts import render, redirect
from django.db.models.functions import TruncMonth
from django.db.models import Sum
from datetime import datetime
from calendar import month_name
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache  # Para evitar el "atrás" del navegador
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse

# Importación de tus modelos
from apy.models import Caja, Module, Permission 

# --- LÓGICA DE PERMISOS PARA VISTAS BASADAS EN FUNCIÓN ---

def check_custom_permission(user, module_name, permission_required):
    """
    Verifica si un usuario tiene el permiso requerido.
    Lanza PermissionDenied (403) si no lo tiene.
    """
    if user.is_superuser:
        return None 
    
    try:
        module = Module.objects.get(name=module_name)
        permission_obj = Permission.objects.filter(user=user, module=module).first()
        
        has_permission = False
        if permission_obj:
            has_permission = getattr(permission_obj, permission_required, False)
            
        if has_permission:
            return None 
        else:
            raise PermissionDenied(
                f"Acceso denegado. No tienes permiso de {permission_required.upper()} para el módulo '{module_name}'."
            )
            
    except Module.DoesNotExist:
        raise PermissionDenied(
            f"Error de configuración: Módulo '{module_name}' no encontrado."
        )

<<<<<<< HEAD
@login_required(login_url=reverse_lazy('apy:login'))
def estadisticas(request):
    
    # --- 1. VERIFICACIÓN DE PERMISOS INDEPENDIENTE ---
=======
# --- VISTA DE ESTADÍSTICAS ---

@never_cache  # Capa de seguridad: prohíbe al navegador cachear esta página
@login_required(login_url=reverse_lazy('login:login'))  # Corregido: apunta a tu app 'login'
def estadisticas(request):
    
    # --- 1. VERIFICACIÓN DE PERMISOS ---
>>>>>>> erick
    try:
        check_custom_permission(
            request.user, 
        module_name='EstadisticasGenerales',
            permission_required='view'
        )
    except PermissionDenied as e:
<<<<<<< HEAD
        # Si no tiene permiso, lo mandamos al index (o dashboard)
        # para evitar el bucle de redirección infinita.
        messages.error(request, "No tienes acceso al panel de estadísticas.")
        return redirect('apy:index') 

    # --- 2. OBTENCIÓN DE DATOS ---
=======
        # UX: Si no tiene permiso, lo mandamos a la lista con un aviso
        messages.warning(request, str(e))
        return redirect(reverse_lazy('apy:caja_lista')) 

    # --- 2. LÓGICA DE NEGOCIO (INGRESOS) ---
>>>>>>> erick
    ingresos_por_mes = (
        Caja.objects
        .filter(tipo_movimiento='Ingreso')
        .annotate(mes=TruncMonth('fecha'))
        .values('mes')
        .annotate(total=Sum('monto'))
        .order_by('mes')
    )

<<<<<<< HEAD
    # Nombres de meses en español
    meses_es = [
        "", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
=======
    meses_espanol = [
        "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
>>>>>>> erick
        "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
    ]

    meses = []
    totales = []

    for ingreso in ingresos_por_mes:
<<<<<<< HEAD
        if ingreso['mes']:
            mes_num = ingreso['mes'].month
            meses.append(meses_es[mes_num])
            totales.append(float(ingreso['total'] or 0))
=======
        mes_num = ingreso['mes'].month
        # Usamos el array en español para que se vea mejor
        meses.append(meses_espanol[mes_num - 1]) 
        totales.append(float(ingreso['total']))
>>>>>>> erick

    context = {
        'meses': meses,
        'totales': totales,
        'titulo': 'Panel General de Estadísticas',
        'entidad': 'Reportes'
    }

    return render(request, 'estadisticas.html', context)