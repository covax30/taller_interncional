from django.shortcuts import render
from django.db.models.functions import TruncMonth
from django.db.models import Sum
from datetime import datetime
from calendar import month_name
from django.shortcuts import render
from apy.models import Caja

from django.http import HttpResponse

def estadisticas(request):
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
        meses.append(month_name[mes_num])  # convierte 1 → "January"
        totales.append(float(ingreso['total']))

    context = {
        'meses': meses,
        'totales': totales,
    }

    return render(request, 'estadisticas.html', context)