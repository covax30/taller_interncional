import openpyxl
from django.http import HttpResponse
from django.views.generic import ListView, TemplateView, CreateView
from django.db.models import Sum
from django.utils import timezone
from django.urls import reverse_lazy
from django.contrib import messages

from apy.models import Informes, DetalleServicio, Cliente
from apy.forms import InformeForm

class InformeDashboardView(TemplateView):
    template_name = 'informes/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hoy = timezone.now()
        context['total_ventas_mes'] = Informes.objects.filter(fecha__month=hoy.month).aggregate(total=Sum('total_final'))['total'] or 0
        context['servicios_pendientes'] = DetalleServicio.objects.filter(proceso='proceso', estado=True).count()
        context['ultimos_informes'] = Informes.objects.all().select_related('detalle_servicio__id_vehiculo').order_by('-fecha')[:5]
        context['servicios_preventivos'] = Informes.objects.filter(tipo_informe='Preventivo').count()
        context['servicios_correctivos'] = Informes.objects.filter(tipo_informe='Correctivo').count()
        return context

class CreateInformeView(CreateView):
    model = Informes
    form_class = InformeForm
    template_name = 'informes/crear_informe.html'
    success_url = reverse_lazy('apy:informe_lista')

    def get_initial(self):
        initial = super().get_initial()
        # Capturamos el ID del servicio que viene por la URL (?servicio_id=X)
        servicio_id = self.request.GET.get('servicio_id')
        if servicio_id:
            initial['detalle_servicio'] = servicio_id
        return initial

    def form_valid(self, form):
        # Aquí puedes agregar lógica extra antes de guardar si lo necesitas
        messages.success(self.request, "Informe técnico guardado y costos cerrados.")
        return super().form_valid(form)

class InformeListView(ListView):
    model = Informes
    template_name = 'informes/listar_informe.html'
    context_object_name = 'informes'

def exportar_informe_excel(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(['ID', 'Fecha', 'Placa', 'Mano Obra', 'Total'])
    informes = Informes.objects.all().select_related('detalle_servicio__id_vehiculo')
    for i in informes:
        ws.append([i.id_informe, i.fecha.strftime('%d/%m/%Y'), i.detalle_servicio.id_vehiculo.placa, i.costo_mano_obra, i.total_final])
    
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="Reporte_Productividad.xlsx"'
    wb.save(response)
    return response