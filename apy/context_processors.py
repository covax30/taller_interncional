# apy/context_processors.py
from apy.models import Permission, Module
from .models import AlertaStock

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


def alertas_stock(request):
    """
    Disponible en todos los templates como:
      {{ alertas_no_leidas }}        → queryset con las alertas
      {{ total_alertas_no_leidas }}  → entero con el conteo
    """
    if not request.user.is_authenticated:
        return {}

    alertas = AlertaStock.objects.filter(leida=False).order_by('-fecha')[:20]
    return {
        'alertas_no_leidas':       alertas,
        'total_alertas_no_leidas': alertas.count(),
    }


# ═══════════════════════════════════════════════════════════════
# apy/view/notificaciones/views.py   (actualiza el archivo)
# ═══════════════════════════════════════════════════════════════

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.db.models import F
from apy.models import Repuesto, Insumos, Herramienta, AlertaStock


@login_required
def api_stock_bajo(request):
    """
    Devuelve JSON con todos los ítems cuyo stock está en o por debajo
    del stock_minimo. Consumido por el widget de la campana del header.
    """
    repuestos = (
        Repuesto.objects
        .filter(estado=True, stock__lte=F('stock_minimo'))
        .values('id', 'nombre', 'stock', 'stock_minimo')
    )
    insumos = (
        Insumos.objects
        .filter(estado=True, stock__lte=F('stock_minimo'))
        .values('id', 'nombre', 'stock', 'stock_minimo')
    )
    herramientas = (
        Herramienta.objects
        .filter(estado=True, stock__lte=F('stock_minimo'))
        .values('id', 'nombre', 'stock', 'stock_minimo')
    )

    def _fmt(tipo, items):
        return [
            {
                'tipo':         tipo,
                'id':           i['id'],
                'nombre':       i['nombre'],
                'stock':        i['stock'],
                'stock_minimo': i['stock_minimo'],
                'nivel':        '🔴 Sin stock' if i['stock'] == 0 else '🟡 Stock bajo',
            }
            for i in items
        ]

    alertas = _fmt('Repuesto', repuestos) + _fmt('Insumo', insumos) + _fmt('Herramienta', herramientas)

    return JsonResponse({'total': len(alertas), 'alertas': alertas})


@login_required
@require_POST
def marcar_alerta_leida(request, pk):
    """
    Marca una AlertaStock como leída (descartada por el admin).
    Llamado por el botón ✕ del toast o del panel de la campana.
    """
    alerta = get_object_or_404(AlertaStock, pk=pk)
    alerta.leida = True
    alerta.save(update_fields=['leida'])
    return JsonResponse({'ok': True})


@login_required
@require_POST
def marcar_todas_leidas(request):
    """Marca TODAS las alertas no leídas como leídas."""
    AlertaStock.objects.filter(leida=False).update(leida=True)
    return JsonResponse({'ok': True})