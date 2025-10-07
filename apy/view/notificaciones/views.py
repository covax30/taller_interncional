from django.http import JsonResponse
from django.db.models import F
from apy.models import Repuesto

def stock_notifications_api(request):
    # Filtra los repuestos cuyo stock actual es menor o igual al stock mínimo
    repuestos_bajo_stock = Repuesto.objects.filter(stock_actual__lte=F('stock_minimo'))

    notificaciones = []
    for repuesto in repuestos_bajo_stock:
        notificaciones.append({
            'id': repuesto.id,
            'nombre': repuesto.nombre,
            'stock': repuesto.stock_actual,   # este campo lo usa tu JS
            'stock_minimo': repuesto.stock_minimo,
        })

    return JsonResponse({'notificaciones': notificaciones, 'count': len(notificaciones)})
