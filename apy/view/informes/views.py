# apy/view/informes/views.py — MÓDULO INFORMES COMPLETO

from django.utils import timezone
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.views import View
from django.db.models import Sum, Count, Q
from django.db.models.functions import TruncMonth, TruncWeek
from django.urls import reverse_lazy
from django.http import HttpResponse
from datetime import date, timedelta, datetime
import json

from apy.models import (
    DetalleServicio, Pagos, Nomina, Profile,
    Module, Permission
)
from apy.decorators import PermisoRequeridoMixin


# ─────────────────────────────────────────────────────────────
# HELPERS DE FECHA
# ─────────────────────────────────────────────────────────────
def get_rango_fechas(request):
    """
    Lee los parámetros GET y devuelve (fecha_inicio, fecha_fin, periodo_activo).
    Prioridad: rango personalizado > periodo rápido > mes actual por defecto.
    """
    hoy = timezone.now().date()

    # Rango personalizado
    desde_str = request.GET.get('desde', '')
    hasta_str = request.GET.get('hasta', '')
    if desde_str and hasta_str:
        try:
            desde = date.fromisoformat(desde_str)
            hasta = date.fromisoformat(hasta_str)
            return desde, hasta, 'personalizado'
        except ValueError:
            pass

    # Periodo rápido
    periodo = request.GET.get('periodo', 'mes')
    if periodo == 'semana':
        desde = hoy - timedelta(days=hoy.weekday())   # lunes de esta semana
        hasta = desde + timedelta(days=6)
        return desde, hasta, 'semana'
    elif periodo == 'anio':
        desde = date(hoy.year, 1, 1)
        hasta = date(hoy.year, 12, 31)
        return desde, hasta, 'anio'
    else:  # mes (default)
        desde = date(hoy.year, hoy.month, 1)
        # último día del mes
        if hoy.month == 12:
            hasta = date(hoy.year, 12, 31)
        else:
            hasta = date(hoy.year, hoy.month + 1, 1) - timedelta(days=1)
        return desde, hasta, 'mes'


def labels_para_grafica(desde, hasta, qs_fecha_field):
    """Genera labels de días para gráficas pequeñas (máx 31 días)."""
    delta = (hasta - desde).days
    if delta <= 31:
        return [(desde + timedelta(days=i)).strftime('%d/%m') for i in range(delta + 1)]
    return None



# ─────────────────────────────────────────────────────────────
# VISTAS EXISTENTES (mantener compatibilidad con urls.py)
# ─────────────────────────────────────────────────────────────
class InformeListView(PermisoRequeridoMixin, View):
    module_name = 'Informes'
    permission_required = 'view'

    def get(self, request):
        from apy.models import Informes
        informes = Informes.objects.filter(estado=True).select_related(
            'detalle_servicio__id_vehiculo', 'id_empleado__user'
        ).order_by('-fecha')
        return render(request, 'informes/lista_informes.html', {'informes': informes})


class CreateInformeView(PermisoRequeridoMixin, View):
    module_name = 'Informes'
    permission_required = 'add'

    def get(self, request):
        from apy.forms import InformeForm
        form = InformeForm()
        servicios = DetalleServicio.objects.filter(
            estado=True, proceso='terminado'
        ).exclude(informes__isnull=False)
        return render(request, 'informes/crear_informe.html', {
            'form': form,
            'servicios': servicios,
        })

    def post(self, request):
        from apy.forms import InformeForm
        from apy.models import Informes
        form = InformeForm(request.POST)
        if form.is_valid():
            informe = form.save(commit=False)
            servicio_id = request.POST.get('detalle_servicio')
            try:
                informe.detalle_servicio = DetalleServicio.objects.get(pk=servicio_id)
                informe.id_empleado = request.user.profile
                informe.save()
                from django.contrib import messages
                messages.success(request, 'Informe creado correctamente.')
                return __import__('django.shortcuts', fromlist=['redirect']).redirect('apy:informe_lista')
            except Exception as e:
                form.add_error(None, str(e))
        servicios = DetalleServicio.objects.filter(estado=True, proceso='terminado')
        return render(request, 'informes/crear_informe.html', {'form': form, 'servicios': servicios})


class InformeDetailView(PermisoRequeridoMixin, View):
    module_name = 'Informes'
    permission_required = 'view'

    def get(self, request, pk):
        from apy.models import Informes
        from django.shortcuts import get_object_or_404
        informe = get_object_or_404(Informes, pk=pk)
        return render(request, 'informes/detalle_informe.html', {'informe': informe})


class InformeGerencialView(PermisoRequeridoMixin, View):
    module_name = 'Informes'
    permission_required = 'view'

    def get(self, request):
        return render(request, 'informes/informe_gerencial.html', {})


def exportar_informe_excel(request):
    """Exporta el informe filtrado a Excel."""
    import openpyxl
    from openpyxl.styles import Font, PatternFill, Alignment
    from openpyxl.utils import get_column_letter

    desde, hasta, periodo = get_rango_fechas(request)
    estado_filtro = request.GET.get('estado', 'todos')
    modulo = request.GET.get('modulo', 'servicios')

    wb = openpyxl.Workbook()
    ws = wb.active

    header_fill = PatternFill(start_color='1F4E79', end_color='1F4E79', fill_type='solid')
    header_font = Font(color='FFFFFF', bold=True)

    if modulo == 'servicios':
        ws.title = 'Servicios'
        qs = DetalleServicio.objects.filter(
            estado=True,
            fecha_creacion__date__gte=desde,
            fecha_creacion__date__lte=hasta,
        )
        if estado_filtro != 'todos':
            qs = qs.filter(proceso=estado_filtro)

        headers = ['ID', 'Vehículo', 'Cliente', 'Empleado', 'Fecha', 'Estado', 'Total']
        ws.append(headers)
        for cell in ws[1]:
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = Alignment(horizontal='center')

        for s in qs.select_related('id_vehiculo', 'cliente', 'empleado').order_by('-fecha_creacion'):
            ws.append([
                s.id,
                str(s.id_vehiculo.placa),
                str(s.cliente.nombre),
                str(s.empleado.user.get_full_name() if s.empleado else '—'),
                s.fecha_creacion.strftime('%d/%m/%Y'),
                s.get_proceso_display(),
                float(s.subtotal),
            ])

    elif modulo == 'pagos':
        ws.title = 'Pagos'
        qs = Pagos.objects.filter(estado=True, fecha__gte=desde, fecha__lte=hasta)
        headers = ['ID', 'Proveedor', 'Fecha', 'Tipo Pago', 'Monto Total']
        ws.append(headers)
        for cell in ws[1]:
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = Alignment(horizontal='center')
        for p in qs.select_related('proveedor').order_by('-fecha'):
            ws.append([p.id_pago, p.proveedor.nombre, p.fecha.strftime('%d/%m/%Y'), p.tipo_pago, float(p.monto_total)])

    elif modulo == 'nomina':
        ws.title = 'Nómina'
        qs = Nomina.objects.filter(fecha_pago__gte=desde, fecha_pago__lte=hasta)
        headers = ['ID', 'Empleado', 'Fecha Pago', 'Monto']
        ws.append(headers)
        for cell in ws[1]:
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = Alignment(horizontal='center')
        for n in qs.select_related('empleado__user').order_by('-fecha_pago'):
            ws.append([
                n.id,
                n.empleado.user.get_full_name() or n.empleado.user.username,
                n.fecha_pago.strftime('%d/%m/%Y'),
                float(n.monto),
            ])

    # Ajustar anchos
    for col in ws.columns:
        max_len = max(len(str(cell.value or '')) for cell in col)
        ws.column_dimensions[get_column_letter(col[0].column)].width = min(max_len + 4, 40)

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="informe_{modulo}_{desde}_{hasta}.xlsx"'
    wb.save(response)
    return response