# ─────────────────────────────────────────────────────────────
# apy/view/notificaciones/views.py   (archivo NUEVO)
# ─────────────────────────────────────────────────────────────

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import F
from apy.models import Repuesto, Insumos, Herramienta


@login_required
def api_stock_bajo(request):
    """
    Devuelve un JSON con todos los ítems cuyo stock está en o por debajo
    del stock_minimo. Lo consume el widget de notificaciones del header.
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

    def _label(item_type, item):
        nivel = "🔴 Sin stock" if item['stock'] == 0 else "🟡 Stock bajo"
        return {
            'tipo':        item_type,
            'id':          item['id'],
            'nombre':      item['nombre'],
            'stock':       item['stock'],
            'stock_minimo': item['stock_minimo'],
            'nivel':       nivel,
        }

    alertas = (
        [_label('Repuesto',    r) for r in repuestos]   +
        [_label('Insumo',      i) for i in insumos]     +
        [_label('Herramienta', h) for h in herramientas]
    )

    return JsonResponse({
        'total':   len(alertas),
        'alertas': alertas,
    })