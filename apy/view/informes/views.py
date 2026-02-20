from django.shortcuts import render, redirect
from apy.models import Informes, Module, Permission 
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse, HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from apy.forms import *
from django.contrib import messages
# Se elimina la importación de AccessMixin ya que no se usa localmente.
from apy.decorators import PermisoRequeridoMixin
from openpyxl import Workbook
from django.http import HttpResponse
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side


# --------------Vistas de informes---------------

class InformesListView(PermisoRequeridoMixin, ListView): 
    model = Informes
    template_name ='Informes/listar_informe.html'
    
    # --- Configuración de Permisos ---
    module_name = 'Informes' 
    permission_required = 'view'
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        # Usa el Mixin importado de apy.decorators
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        nombre = {'nombre' : 'Informes'}
        return JsonResponse(nombre)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Informes'
        context['crear_url'] = reverse_lazy('apy:informes_crear')
        context['entidad'] = 'Informes'
        return context
    
class InformesCreateView(PermisoRequeridoMixin, CreateView): 
    model = Informes
    form_class = InformeForm
    template_name = 'Informes/crear_informe.html'
    success_url = reverse_lazy('apy:informes_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'Informes'
    permission_required = 'add'
    
    def form_valid(self, form):
        form.instance.estado = True 
        messages.success(self.request, "Informe creado correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context ['titulo'] = 'Crear Informe'
        context ['entidad'] = 'Informes'
        context ['listar_url'] = reverse_lazy('apy:informes_lista')
        return context
    
#--- vista para listar informes inactivos ---
class InformesInactivosListView(PermisoRequeridoMixin, ListView):       
    model = Informes
    template_name ='Informes/informes_inactivos.html'
    
    # --- Configuración de Permisos ---
    module_name = 'Informes' 
    permission_required = 'view' 
    
    def get_queryset(self):
        return Informes.objects.filter(estado=False)
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        # Usa el Mixin importado de apy.decorators
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        nombre = {'nombre' : 'informes inactivos'}
        return JsonResponse(nombre)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Informes Inactivos'
        context['listar_url'] = reverse_lazy('apy:informes_lista')
        context['entidad'] = 'Informes'
        return context    
    
class InformesUpdateView(PermisoRequeridoMixin, UpdateView): 
    model = Informes
    form_class = InformeForm
    template_name = 'Informes/crear_informe.html'
    success_url = reverse_lazy('apy:informes_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'Informes'
    permission_required = 'change'
    
    def form_valid(self, form):
        
        form.instance.estado = True 
        messages.success(self.request, "Informe actualizado correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Informe'
        context['entidad'] = 'Informes'
        context['listar_url'] = reverse_lazy('apy:informes_lista')
        return context

class InformesDeleteView(PermisoRequeridoMixin, DeleteView): 
    model = Informes
    template_name = 'Informes/eliminar_informe.html'
    success_url = reverse_lazy('apy:informes_lista')
    context_object_name = 'object'
    
    # --- Configuración de Permisos ---
    module_name = 'Informes'
    permission_required = 'delete'
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        
        self.object = self.get_object()
        success_url = self.get_success_url()
        
        self.object.estado = False
        self.object.save()
        
        messages.success(self.request,     f"Informe {Informes} desactivado correctamente")
        return HttpResponseRedirect(success_url)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Informe'
        context['entidad'] = 'Informes'
        context['listar_url'] = reverse_lazy('apy:informes_lista')
        return context
    
#- vista para activar  informe ---
class InformesActivateView(PermisoRequeridoMixin, DeleteView): 
    model = Informes
    template_name = 'Informes/activar_informes.html'
    success_url = reverse_lazy('apy:informes_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'Informes'
    permission_required = 'change'
    
    def form_valid(self, form):
        self.object.estado = True
        self.object.save()
        messages.success(self.request, "informe activado correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Activar Informe'
        context['entidad'] = 'Informes' 
        context['listar_url'] = reverse_lazy('apy:informes_lista')
        
        return context
    
from django.http import JsonResponse
from django.db.models import Sum

def obtener_costos_mantenimiento(request):
    if request.method == 'POST':
        form = InformeForm(request.POST)
        repuesto_formset = DetalleRepuestoFormSet(request.POST, prefix='repuestos')
        insumo_formset = DetalleInsumosFormSet(request.POST, prefix='insumos')

        if form.is_valid() and repuesto_formset.is_valid() and insumo_formset.is_valid():
            # 1. Guardamos el informe base (sin commit para calcular totales)
            informe = form.save(commit=False)
            
            # 2. Guardamos los formsets para que existan en la DB
            repuestos = repuesto_formset.save(commit=False)
            insumos = insumo_formset.save(commit=False)
            
            # 3. Calculamos totales antes de guardar definitivamente
            total_rep = sum(r.cantidad * r.precio_unitario for r in repuestos)
            total_ins = sum(i.cantidad * i.precio_unitario for i in insumos)
            
            informe.total_repuestos = total_rep
            informe.total_insumos = total_ins
            informe.total_final = total_rep + total_ins + informe.costo_mano_obra
            
            informe.save() # Guardar Informe
            
            # 4. Vincular y guardar los detalles
            for r in repuestos:
                r.id_informe = informe # O la relación que tengas definida
                r.save()
            for i in insumos:
                i.id_informe = informe
                i.save()
                
            return redirect('apy:informes_lista')
    else:
        form = InformeForm()
        repuesto_formset = DetalleRepuestoFormSet(prefix='repuestos')
        insumo_formset = DetalleInsumosFormSet(prefix='insumos')

    return render(request, 'informes/informe_form.html', {
        'form': form,
        'repuesto_formset': repuesto_formset,
        'insumo_formset': insumo_formset,
    })
    
def informe_excel(request, id):
    informe = Informes.objects.get(id_informe=id)

    wb = Workbook()
    ws = wb.active
    ws.title = "Informe"

    # ===== ESTILOS =====
    titulo_font = Font(size=14, bold=True)
    header_font = Font(bold=True, color="FFFFFF")
    header_fill = PatternFill("solid", fgColor="2C3E50")
    center = Alignment(horizontal="center", vertical="center")

    border = Border(
        left=Side(style="thin"),
        right=Side(style="thin"),
        top=Side(style="thin"),
        bottom=Side(style="thin")
    )

    # ===== TÍTULO =====
    ws.merge_cells("A1:B1")
    ws["A1"] = "INFORME DE MANTENIMIENTO"
    ws["A1"].font = titulo_font
    ws["A1"].alignment = center

    # ===== ENCABEZADOS =====
    headers = ["Campo", "Detalle"]
    ws.append(headers)

    for col in range(1, 3):
        cell = ws.cell(row=2, column=col)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = center
        cell.border = border

    # ===== DATOS =====
    data = [
    ]

    row = 3
    for campo, valor in data:
        ws.cell(row=row, column=1, value=campo)
        ws.cell(row=row, column=2, value=valor)

        for col in range(1, 3):
            ws.cell(row=row, column=col).border = border
            ws.cell(row=row, column=col).alignment = Alignment(vertical="center")

        row += 1

    # ===== FORMATO MONEDA =====
    ws["B5"].number_format = '"$"#,##0.00'

    # ===== AJUSTAR COLUMNAS =====
    ws.column_dimensions["A"].width = 25
    ws.column_dimensions["B"].width = 40

    # ===== RESPONSE =====
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = f'attachment; filename=Informe_{id}.xlsx'

    wb.save(response)
    return response