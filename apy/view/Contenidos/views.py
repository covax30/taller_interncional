from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from urllib3 import request
from apy.forms import *
from django.contrib import messages
# Importar modelos necesarios
from apy.models import Factura, DetalleRepuesto, DetalleTipoMantenimiento, DetalleInsumos 
# Importar el Mixin Corregido (que lanza 403)
from apy.decorators import PermisoRequeridoMixin 


from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView

# --------------Vistas de Facturas---------------
class FacturaListView(PermisoRequeridoMixin, ListView):
    model = Factura
    template_name ='Contenido/listar_factura.html'
    
    # --- Configuración de Permisos ---
    module_name = 'Facturas' 
    permission_required = 'view'
    
    def get_queryset(self):
        return Factura.objects.filter(estado=True)
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        # El Mixin se ejecuta antes de super().dispatch (lanzará 403)
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        nombre = {'nombre' : 'Karol'}
        return JsonResponse(nombre)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Facturas'
        context['crear_url'] = reverse_lazy('apy:factura_crear')
        context['entidad'] = 'Factura'
        return context
    
#-----------------Vistas de Facturas (CBVs) de Inactivos---------------
class FacturaInactivosListView(PermisoRequeridoMixin, ListView):
    model = Factura
    template_name = 'Contenido/facturas_inactivas.html'
    
    # --- Configuración de Permisos ---
    module_name = 'Facturas' 
    permission_required = 'view'
    
    def get_queryset(self):
        return Factura.objects.filter(estado=False)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        nombre = {'nombre' : 'Factura Inactiva'}
        return JsonResponse(nombre)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Facturas Inactivos'
        context['crear_url'] = reverse_lazy('apy:factura_crear')
        context['entidad'] = 'Factura'
        return context
    
class FacturaCreateView(PermisoRequeridoMixin, CreateView): 
    model = Factura
    form_class = FacturaForm
    template_name = 'Contenido/crear_factura.html'
    success_url = reverse_lazy('apy:factura_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'Facturas'
    permission_required = 'add'
    
    def form_valid(self, form):
        form.instance.estado = True 
        messages.success(self.request, "Factura creada correctamente")
        return super().form_valid(form)
 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context ['titulo'] = 'Crear Factura'
        context ['entidad'] = 'Facturas'
        context ['listar_url'] = reverse_lazy('apy:factura_lista')
        return context
    
def agregar_fila_repuesto(request):
    # Asegúrate de usar el nombre correcto de tu formulario de detalles
    # Si no lo tienes creado, puedes usar FacturaForm o el específico de repuestos
    form = RepuestoscantidadForm()
    return render(request, 'Contenido/parcial_fila_repuesto.html', {'form': form})    

def filtrar_items(request):
    tipo = request.GET.get('tipo_seleccion')
    
    if tipo == 'repuestos':
        # Usamos tu formulario existente RepuestoscantidadForm
        form = RepuestoscantidadForm()
        campo = form['id_repuesto']
    elif tipo == 'mantenimiento':
        form = DetalleTipo_MantenimientoForm()
        campo = form['id_tipo_mantenimiento']
    elif tipo == 'insumos':
        form = DetalleInsumoForm()
        campo = form['id_insumos']
    else:
        return HttpResponse('<select class="form-control"><option>---------</option></select>')

    return render(request, 'Contenido/parcial_select_filtrado.html', {'campo': campo})
class FacturaUpdateView(PermisoRequeridoMixin, UpdateView): 
    model = Factura
    form_class = FacturaForm
    template_name = 'Contenido/crear_factura.html'
    success_url = reverse_lazy('apy:factura_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'Facturas'
    permission_required = 'change'
    
    def form_valid(self, form):
        messages.success(self.request, "Factura actualizada correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Factura'
        context['entidad'] = 'Facturas'
        context['listar_url'] = reverse_lazy('apy:factura_lista')
        return context

class FacturaDeleteView(PermisoRequeridoMixin, DeleteView):
    model = Factura
    template_name = 'Contenido/eliminar_factura.html'
    success_url = reverse_lazy('apy:factura_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'Facturas'
    permission_required = 'delete'
    
    def post(self, request, *args, **kwargs):
        
        self.object = self.get_object()
        success_url = self.get_success_url()
        
        self.object.estado = False
        self.object.save()

        messages.success(self.request, f"Factura {Factura} desactivada ")
        return HttpResponseRedirect(success_url)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Factura'
        context['entidad'] = 'Facturas'
        context['listar_url'] = reverse_lazy('apy:factura_lista')
        return context
    
#---------------Vistas de Facturas (CBVs) de Inactivos---------------
class FacturaActivarView(PermisoRequeridoMixin, DeleteView):
    model = Factura
    template_name = 'Contenido/activar_factura.html'
    success_url = reverse_lazy('apy:factura_inactivos')
    
    # --- Configuración de Permisos ---
    module_name = 'Facturas'
    permission_required = 'change'
    
    def post(self, request, *args, **kwargs):
        
        self.object = self.get_object()
        success_url = self.get_success_url()
        
        self.object.estado = True
        self.object.save()
        
        messages.success(self.request, f"Factura {Factura} activado ")
        return HttpResponseRedirect(success_url)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Activar Factura'
        context['entidad'] = 'Facturas'
        context['listar_url'] = reverse_lazy('apy:factura_inactivos')
        return context    
    
def factura_detalle_json(request, pk):
    # Traemos la factura por su ID (pk)
    factura = get_object_or_404(Factura, pk=pk)
    
    # Obtenemos el servicio relacionado
    # NOTA: Asegúrate que el campo en 'Factura' se llame 'detalles_servicios'
    servicio = factura.detalle_servicio
    
    # 1. Repuestos (usando el related_name por defecto '_set')
    repuestos = [
        {
            'categoria': f"REPUESTO",
            'descripcion': f" {r.id_repuesto.nombre}",
            'cantidad': r.cantidad,
            'precio': float(r.precio_unitario),
            'subtotal': float(r.subtotal)
        } for r in servicio.detallerepuesto_set.all().select_related('id_repuesto')
    ]
    
    # 2. Mantenimientos
    mantenimientos = [
        {
            'categoria': f"MANTENIMIENTO ",
            'descripcion': f" {m.id_tipo_mantenimiento.nombre}",
            'cantidad': m.cantidad,
            'precio': float(m.precio_unitario),
            'subtotal': float(m.subtotal)
        } for m in servicio.detalletipomantenimiento_set.all().select_related('id_tipo_mantenimiento')
    ]

    # 3. Insumos
    insumos = [
        {
            'categoria': f"INSUMO",
            'descripcion': f" {i.id_insumos.id_marca.nombre}",
            'cantidad': i.cantidad,
            'precio': float(i.precio_unitario),
            'subtotal': float(i.subtotal)
        } for i in servicio.detalleinsumos_set.all().select_related('id_insumos')
    ]

    # Unimos todos los items para la tabla del PDF
    todos_los_items = repuestos + mantenimientos + insumos

    # Estructura final del JSON
    data = {
        'factura_nro': factura.id,
        'fecha': factura.fecha.strftime('%d/%m/%Y'),
        'empresa': {
            'nombre': factura.empresa.nombre,
            'nit': factura.empresa.nit,
            'direccion': factura.empresa.direccion,
            'telefono': factura.empresa.telefono,
        },
        'cliente': {
            'nombre': factura.cliente.nombre,
            'documento': factura.cliente.identificacion,
            'telefono': factura.cliente.telefono,
            'direccion': factura.cliente.direccion,
            
        },
        'vehiculo': {
            'placa': servicio.id_vehiculo.placa,
            'info': f"{servicio.id_vehiculo.marca_vehiculo} {servicio.id_vehiculo.modelo_vehiculo} ",
            
        },
        'items': todos_los_items,
        'subtotal_factura': float(factura.subtotal),
    }
    
    return JsonResponse(data)

class DetalleFacturaView(DetailView):
    model = Factura
    template_name = 'Contenido/detalle_factura.html'
    context_object_name = 'factura'

    def get_queryset(self):
        # 1. select_related: Solo para lo que Django te permite (relaciones directas)
        return Factura.objects.select_related(
            'empresa', 
            'cliente', 
            'empleado',  
            'detalle_servicio'
        ).prefetch_related(
            # 2. prefetch_related: Para los detalles que quieres SEPARAR
            'detalle_servicio__id_vehiculo',
            'detalle_servicio__detallerepuesto_set',
            'detalle_servicio__detalleinsumos_set',
            'detalle_servicio__detalletipomantenimiento_set'
        )
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        factura = self.get_object()
        servicio = factura.detalle_servicio

        context.update({
            'servicio': servicio,
            'repuestos': servicio.detallerepuesto_set.all(),
            'mantenimientos': servicio.detalletipomantenimiento_set.all(),
            'insumos': servicio.detalleinsumos_set.all(),
            'subtotal_factura': servicio.subtotal,
        })

        return context
    
