# apy/view/estadisticas/views.py  — ARCHIVO COMPLETO

from datetime import timedelta
import json

from django.utils import timezone
from django.shortcuts import render
from django.db.models import Sum, Count, Avg, Q
from django.db.models.functions import TruncMonth
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.http import JsonResponse

from apy.models import (
    Caja, Cliente, DetalleServicio, Gastos, Insumos,
    Module, Nomina, Pagos, Permission, Vehiculo,
    DetalleRepuesto, DetalleInsumos  # para top 5
)
from apy.view.informes.views import get_rango_fechas


# ─────────────────────────────────────────────────────────────
# Helper de permisos
# ─────────────────────────────────────────────────────────────
def check_custom_permission(user, module_name, permission_required):
    if user.is_superuser:
        return None
    try:
        module = Module.objects.get(name=module_name)
        perm   = Permission.objects.filter(user=user, module=module).first()
        if perm and getattr(perm, permission_required, False):
            return None
        raise PermissionDenied(
            f"No tienes permiso de {permission_required.upper()} para '{module_name}'."
        )
    except Module.DoesNotExist:
        raise PermissionDenied(f"Módulo '{module_name}' no encontrado.")


# ─────────────────────────────────────────────────────────────
# Helper: ¿es gerente?
# ─────────────────────────────────────────────────────────────
def es_gerente(user):
    return user.is_superuser or user.is_staff


# ─────────────────────────────────────────────────────────────
# VISTA PRINCIPAL DE ESTADÍSTICAS
# ─────────────────────────────────────────────────────────────
@never_cache
@login_required(login_url=reverse_lazy('login:login'))
def estadisticas(request):
    hoy        = timezone.now()
    mes_actual = hoy.month
    anio_actual= hoy.year

    # ── Servicios del mes (para tablas/métricas, no financiero) ──
    servicios_mes = DetalleServicio.objects.filter(
        fecha_creacion__month=mes_actual,
        fecha_creacion__year=anio_actual,
        proceso='terminado'
    )
    # Ingresos del mes (total en Caja tipo 'Ingreso')
    ingresos_mes = Caja.objects.filter(
        fecha__month=mes_actual,
        fecha__year=anio_actual,
        tipo_movimiento='Ingreso'
    ).aggregate(t=Sum('monto'))['t'] or 0
    ingresos_mes = float(ingresos_mes)

    # ── Ingresos vs Gastos por mes (últimos 6 meses) ───────────
    # Construimos manualmente los últimos 6 meses para el gráfico
    meses_labels  = []
    datos_ingresos = []
    datos_gastos   = []
    NOMBRES_MESES  = ['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic']

    for i in range(5, -1, -1):
        # Mes i meses atrás
        if mes_actual - i <= 0:
            m = mes_actual - i + 12
            a = anio_actual - 1
        else:
            m = mes_actual - i
            a = anio_actual

        meses_labels.append(f"{NOMBRES_MESES[m-1]} {a}")

        # Ingresos ese mes (todo lo que haya en Caja como Ingreso)
        ingreso_m = Caja.objects.filter(
            fecha__month=m,
            fecha__year=a,
            tipo_movimiento='Ingreso'
        ).aggregate(t=Sum('monto'))['t'] or 0
        datos_ingresos.append(round(float(ingreso_m), 2))

        # Gastos ese mes desde Caja
        gasto_m = Caja.objects.filter(
            fecha__month=m,
            fecha__year=a
        ).exclude(tipo_movimiento='Ingreso').aggregate(t=Sum('monto'))['t'] or 0
        datos_gastos.append(float(gasto_m))

    # ── Gastos del mes actual ──────────────────────────────────
    gastos_mes = Caja.objects.filter(
        fecha__month=mes_actual,
        fecha__year=anio_actual
    ).exclude(tipo_movimiento='Ingreso').aggregate(total=Sum('monto'))['total'] or 0
    gastos_mes = float(gastos_mes)

    utilidad_mes = ingresos_mes - gastos_mes

    # ── Métricas de servicios ──────────────────────────────────
    servicios_en_proceso = DetalleServicio.objects.filter(
        proceso='proceso', estado=True
    ).count()

    servicios_terminados_mes = servicios_mes.count()

    # Ticket promedio (evitar división por cero)
    ticket_promedio = (
        round(ingresos_mes / servicios_terminados_mes, 0)
        if servicios_terminados_mes > 0 else 0
    )

    # Comparativo mes anterior
    mes_ant = mes_actual - 1 if mes_actual > 1 else 12
    anio_ant = anio_actual if mes_actual > 1 else anio_actual - 1
    
    ingresos_mes_anterior = Caja.objects.filter(
        fecha__month=mes_ant,
        fecha__year=anio_ant,
        tipo_movimiento='Ingreso'
    ).aggregate(t=Sum('monto'))['t'] or 0
    ingresos_mes_anterior = float(ingresos_mes_anterior)

    variacion_ingresos = (
        round(((ingresos_mes - ingresos_mes_anterior) / ingresos_mes_anterior) * 100, 1)
        if ingresos_mes_anterior > 0 else 0
    )

    # ── Servicios recientes (últimos 8) ────────────────────────
    servicios_recientes = DetalleServicio.objects.filter(
        estado=True
    ).select_related(
        'id_vehiculo', 'empleado'
    ).order_by('-fecha_creacion')[:8]

    # ── Top 5 repuestos más usados ─────────────────────────────
    top_repuestos = (
        DetalleRepuesto.objects
        .values('id_repuesto__nombre')
        .annotate(total_usado=Sum('cantidad'))
        .order_by('-total_usado')[:5]
    )

    # ── Top 5 insumos más usados ───────────────────────────────
    top_insumos = (
        DetalleInsumos.objects
        .values('id_insumos__nombre')
        .annotate(total_usado=Sum('cantidad'))
        .order_by('-total_usado')[:5]
    )

    # ── Contadores generales ───────────────────────────────────
    total_insumos   = Insumos.objects.filter(estado=True).count()
    total_vehiculos = Vehiculo.objects.filter(estado=True).count()
    total_clientes  = Cliente.objects.filter(estado=True).count()
    total_gastos    = Gastos.objects.filter(estado=True).count()

    # ── Empleado más productivo del mes ───────────────────────
    empleado_top = (
        DetalleServicio.objects
        .filter(
            fecha_creacion__month=mes_actual,
            fecha_creacion__year=anio_actual,
            proceso='terminado'
        )
        # Cambiamos 'empleado__first_name' por 'empleado__user__first_name'
        .values('empleado__user__first_name', 'empleado__user__last_name')
        .annotate(total=Count('id'))
        .order_by('-total')
        .first()
    )

    # ── LÓGICA DE INFORMES (Merge) ─────────────────────────────
    desde, hasta, periodo_activo = get_rango_fechas(request)
    estado_filtro = request.GET.get('estado', 'todos')

    # ── SERVICIOS DEL PERÍODO (Informes)
    qs_servicios = DetalleServicio.objects.filter(
        estado=True,
        fecha_creacion__date__gte=desde,
        fecha_creacion__date__lte=hasta,
    )
    if estado_filtro != 'todos':
        qs_servicios = qs_servicios.filter(proceso=estado_filtro)

    total_servicios_informe     = qs_servicios.count()
    servicios_terminados_informe = qs_servicios.filter(proceso='terminado').count()
    servicios_en_proceso_informe = qs_servicios.filter(proceso='proceso').count()
    ingresos_servicios_informe  = sum(float(s.subtotal) for s in qs_servicios.filter(proceso='terminado'))

    # Datos para gráfica servicios por día
    servicios_por_dia = []
    labels_servicios  = []
    delta = (hasta - desde).days
    if delta <= 62:
        for i in range(delta + 1):
            dia = desde + timedelta(days=i)
            cnt = qs_servicios.filter(fecha_creacion__date=dia).count()
            servicios_por_dia.append(cnt)
            labels_servicios.append(dia.strftime('%d/%m'))
    else:
        meses_data = (
            qs_servicios
            .annotate(mes=TruncMonth('fecha_creacion'))
            .values('mes')
            .annotate(total=Count('id'))
            .order_by('mes')
        )
        for m in meses_data:
            labels_servicios.append(m['mes'].strftime('%b %Y'))
            servicios_por_dia.append(m['total'])

    # ── PAGOS A PROVEEDORES
    qs_pagos = Pagos.objects.filter(
        estado=True,
        fecha__gte=desde,
        fecha__lte=hasta,
    )
    total_pagos   = qs_pagos.count()
    monto_pagos   = qs_pagos.aggregate(t=Sum('monto_total'))['t'] or 0

    pagos_por_dia  = []
    labels_pagos   = []
    if delta <= 62:
        for i in range(delta + 1):
            dia = desde + timedelta(days=i)
            monto = qs_pagos.filter(fecha=dia).aggregate(t=Sum('monto_total'))['t'] or 0
            pagos_por_dia.append(float(monto))
            labels_pagos.append(dia.strftime('%d/%m'))
    else:
        meses_pagos = (
            qs_pagos
            .annotate(mes=TruncMonth('fecha'))
            .values('mes')
            .annotate(total=Sum('monto_total'))
            .order_by('mes')
        )
        for m in meses_pagos:
            labels_pagos.append(m['mes'].strftime('%b %Y'))
            pagos_por_dia.append(float(m['total'] or 0))

    # ── NÓMINA
    qs_nomina = Nomina.objects.filter(
        fecha_pago__gte=desde,
        fecha_pago__lte=hasta,
    )
    total_nomina_registros = qs_nomina.count()
    monto_nomina           = qs_nomina.aggregate(t=Sum('monto'))['t'] or 0

    nomina_por_dia = []
    labels_nomina  = []
    if delta <= 62:
        for i in range(delta + 1):
            dia = desde + timedelta(days=i)
            monto = qs_nomina.filter(fecha_pago=dia).aggregate(t=Sum('monto'))['t'] or 0
            nomina_por_dia.append(float(monto))
            labels_nomina.append(dia.strftime('%d/%m'))
    else:
        meses_nomina = (
            qs_nomina
            .annotate(mes=TruncMonth('fecha_pago'))
            .values('mes')
            .annotate(total=Sum('monto'))
            .order_by('mes')
        )
        for m in meses_nomina:
            labels_nomina.append(m['mes'].strftime('%b %Y'))
            nomina_por_dia.append(float(m['total'] or 0))

    # ── TABLAS DE DETALLE
    servicios_tabla = qs_servicios.select_related(
        'id_vehiculo', 'empleado', 'cliente'
    ).order_by('-fecha_creacion')[:20]

    pagos_tabla = qs_pagos.select_related('proveedor').order_by('-fecha')[:20]

    nomina_tabla = qs_nomina.select_related(
        'empleado__user'
    ).order_by('-fecha_pago')[:20]

    # --- FINAL CONTEXT ---
    context = {
        # Contadores tarjetas (globales)
        'total_insumos':   total_insumos,
        'total_vehiculos': total_vehiculos,
        'total_clientes':  total_clientes,
        'total_gastos':    total_gastos,

        # Financiero (mes actual, solo gerente)
        'ingresos_mes':      round(ingresos_mes, 0),
        'gastos_mes':        round(gastos_mes, 0),
        'utilidad_mes':      round(utilidad_mes, 0),
        'variacion_ingresos': variacion_ingresos,
        'ticket_promedio':   round(ticket_promedio, 0),

        # Gráfico ingresos vs gastos principales (estadísticas 6 meses)
        'meses':           json.dumps(meses_labels),
        'totales':         json.dumps(datos_ingresos),
        'datos_ingresos':  json.dumps(datos_ingresos),
        'datos_gastos':    json.dumps(datos_gastos),

        # Métricas servicios (mes actual)
        'servicios_en_proceso':      servicios_en_proceso,
        'servicios_terminados_mes':  servicios_terminados_mes,

        # Tablas (Estadísticas recientes)
        'servicios_recientes': servicios_recientes,
        'top_repuestos':       top_repuestos,
        'top_insumos':         top_insumos,

        # Empleado top (mes actual)
        'empleado_top': empleado_top,

        # Flag de rol para el template
        'es_gerente': es_gerente(request.user),

        # ─── DATOS DE INFORMES ────────────────────────────────
        'periodo_activo': periodo_activo,
        'desde': desde.strftime('%Y-%m-%d'),
        'hasta': hasta.strftime('%Y-%m-%d'),
        'desde_display': desde.strftime('%d/%m/%Y'),
        'hasta_display': hasta.strftime('%d/%m/%Y'),
        'estado_filtro': estado_filtro,

        # Métricas servicios informes
        'total_servicios_informe':      total_servicios_informe,
        'servicios_terminados_informe': servicios_terminados_informe,
        'servicios_en_proceso_informe': servicios_en_proceso_informe,
        'ingresos_servicios_informe':   round(ingresos_servicios_informe, 0),

        # Métricas pagos
        'total_pagos':  total_pagos,
        'monto_pagos':  float(monto_pagos),

        # Métricas nómina
        'total_nomina_registros': total_nomina_registros,
        'monto_nomina':           float(monto_nomina),

        # Gráficas Informes (JSON safe)
        'labels_servicios':  json.dumps(labels_servicios),
        'datos_servicios':   json.dumps(servicios_por_dia),
        'labels_pagos':      json.dumps(labels_pagos),
        'datos_pagos':       json.dumps(pagos_por_dia),
        'labels_nomina':     json.dumps(labels_nomina),
        'datos_nomina':      json.dumps(nomina_por_dia),

        # Tablas Informes
        'servicios_tabla': servicios_tabla,
        'pagos_tabla':     pagos_tabla,
        'nomina_tabla':    nomina_tabla,
    }

    return render(request, 'estadisticas.html', context)


# ─────────────────────────────────────────────────────────────
# APIs JSON para los contadores en tiempo real (sin cambios)
# ─────────────────────────────────────────────────────────────
@login_required(login_url=reverse_lazy('login:login'))
def api_contador_insumos(request):
    return JsonResponse({'total_insumos': Insumos.objects.filter(estado=True).count()})

@login_required(login_url=reverse_lazy('login:login'))
def api_contador_vehiculos(request):
    return JsonResponse({'total_vehiculos': Vehiculo.objects.filter(estado=True).count()})

@login_required(login_url=reverse_lazy('login:login'))
def api_contador_clientes(request):
    return JsonResponse({'total_clientes': Cliente.objects.filter(estado=True).count()})

@login_required(login_url=reverse_lazy('login:login'))
def api_contador_gastos(request):
    return JsonResponse({'total_gastos': Gastos.objects.filter(estado=True).count()})



