from django.db.models import Q
from django.shortcuts import render
from apy.models import *
from django.db.models import Q, TextField
from django.db.models.functions import Cast

def buscador_global(request):
    query = request.GET.get('q', '').strip()
    context = {'query': query}
    
    if query:
        context['clientes'] = Cliente.objects.filter(
            Q(nombre__icontains=query) | Q(correo__icontains=query) | Q(identificacion__icontains=query)
        )
        context['vehiculos'] = Vehiculo.objects.filter(
            Q(placa__icontains=query) | Q(modelo_vehiculo__icontains=query)
        )
        context['informes'] = Informes.objects.filter(
            Q(diagnostico_final__icontains=query) | Q(tipo_informe__icontains=query)
        )
        
        context['factura'] = Factura.objects.filter(
            Q(cliente__nombre__icontains=query) | 
            Q(empleado__nombre__icontains=query) | 
            Q(metodo_pago__icontains=query)
        ).select_related('cliente', 'empleado').distinct()
        
        context['marca'] = Marca.objects.filter(
            Q(tipo__icontains=query) | 
            Q(nombre__icontains=query)
        )
        
        context['repuestos'] = Repuesto.objects.filter(
            Q(id_marca__nombre__icontains=query) | 
            Q(nombre__icontains=query) | 
            Q(categoria__icontains=query) |
            Q(stock__icontains=query)
        ).select_related('id_marca').distinct()
        
        context['herramienta'] = Herramienta.objects.filter(
            Q(id_marca__nombre__icontains=query) | 
            Q(nombre__icontains=query) | 
            Q(tipo__icontains=query) |
            Q(stock__icontains=query)
        ).select_related('id_marca').distinct()
        
        context['insumos'] = Insumos.objects.filter(
            Q(id_marca__nombre__icontains=query) | 
            Q(cantidad__icontains=query) | 
            Q(stock__icontains=query)
        ).select_related('id_marca').distinct()
        
        context['entrada_vehiculo'] = EntradaVehiculo.objects.annotate(
            fecha_str=Cast('fecha_ingreso', TextField()),
            hora_str=Cast('hora_ingreso', TextField()),
        ).filter(
            Q(id_vehiculo__placa__icontains=query) | 
            Q(id_cliente__nombre__icontains=query) | 
            Q(fecha_str__icontains=query) |
            Q(hora_str__icontains=query)
        ).select_related('id_vehiculo', 'id_cliente').distinct()
        
        context['salida_vehiculo'] = SalidaVehiculo.objects.annotate(
            fecha_str=Cast('fecha_salida', TextField()),
            hora_str=Cast('hora_salida', TextField()),
        ).filter(
            Q(id_vehiculo__placa__icontains=query) | 
            Q(id_cliente__nombre__icontains=query) | 
            Q(fecha_str__icontains=query) |
            Q(hora_str__icontains=query)
        ).select_related('id_vehiculo', 'id_cliente').distinct()
        
        context['pago_servicios'] = PagoServiciosPublicos.objects.filter(
            Q(id_servicio__icontains=query) | 
            Q(servicio__icontains=query) | 
            Q(monto__icontains=query)
        )
        
        context['proveedores'] = Proveedores.objects.filter(
            Q(nombre__icontains=query) | 
            Q(telefono__icontains=query) | 
            Q(correo__icontains=query)
        )
        
        context['mantenimiento'] = Mantenimiento.objects.filter(
            Q(id_vehiculo__placa__icontains=query) | 
            Q(id_empleado__nombre__icontains=query) | 
            Q(fallas__icontains=query) |
            Q(id_tipo_mantenimiento__nombre__icontains=query) 
        ).select_related('id_vehiculo', 'id_empleado', 'id_tipo_mantenimiento').distinct()
        
        context['caja'] = Caja.objects.filter(
            Q(tipo_movimiento__icontains=query) | 
            Q(monto__icontains=query) | 
            Q(fecha__icontains=query)
        )
        
    return render(request, 'buscador_global.html', context)