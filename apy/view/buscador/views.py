from django.db.models import Q
from django.shortcuts import render
from apy.models import *
from django.db.models import Q, TextField
from django.db.models.functions import Cast

def buscador_global(request):
    query = request.GET.get('q', '').strip()
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    
    # Pasamos los valores de vuelta al contexto para que se mantengan en los inputs
    context = {
        'query': query,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
    }
    
    # Solo ejecutamos la búsqueda si hay texto O si hay fechas
    if query or (fecha_inicio and fecha_fin):
        
        # --- 1. Modelos que se filtran por TEXTO (Clientes, Vehículos, etc.) ---
        context['clientes'] = Cliente.objects.filter(
            Q(nombre__icontains=query) | Q(correo__icontains=query) | Q(identificacion__icontains=query)
        ) if query else []

        context['vehiculos'] = Vehiculo.objects.filter(
            Q(placa__icontains=query) | Q(modelo_vehiculo__icontains=query)
        ) if query else []
        
        context['tipo_mantenimiento'] = TipoMantenimiento.objects.filter(
            Q(nombre__icontains=query) | Q(descripcion__icontains=query)
        ) if query else []
        
        context['marca'] = Marca.objects.filter(
            Q(nombre__icontains=query) | Q(tipo__icontains=query)
        ) if query else []

        # --- 2. Modelos que se filtran por TEXTO Y FECHAS (Los más importantes) ---
        
        def filtrar_por_fecha(queryset, campo_fecha):
            if fecha_inicio and fecha_fin:
                return queryset.filter(**{f"{campo_fecha}__range": [fecha_inicio, fecha_fin]})
            return queryset

        # Informes 
        informes_qs = Informes.objects.filter(
            Q(diagnostico_final__icontains=query) | 
            Q(tipo_informe__icontains=query) 
        ).distinct() if query else Informes.objects.all()
        # El "colador" de fecha se aplica después, sin importar qué encontró arriba
        context['informes'] = filtrar_por_fecha(informes_qs, 'fecha')

        # Entrada Vehículo 
        entrada_vehiculo_qs = EntradaVehiculo.objects.filter(
            Q(id_entrada__icontains=query) 
        ).distinct() if query else EntradaVehiculo.objects.all()
        # El "colador" de fecha se aplica después, sin importar qué encontró arriba
        context['entrada_vehiculo'] = filtrar_por_fecha(entrada_vehiculo_qs, 'fecha_ingreso')
        
        # Salida Vehículo 
        salida_vehiculo_qs = SalidaVehiculo.objects.filter(
            Q(id_salida__icontains=query) 
        ).distinct() if query else SalidaVehiculo.objects.all()
        # El "colador" de fecha se aplica después, sin importar qué encontró arriba
        context['salida_vehiculo'] = filtrar_por_fecha(salida_vehiculo_qs, 'fecha_salida')
        
        # Caja
        caja_qs = Caja.objects.filter(
            Q(tipo_movimiento__icontains=query) | Q(monto__icontains=query)
        ) if query else Caja.objects.all()
        context['caja'] = filtrar_por_fecha(caja_qs, 'fecha')
        
        # Pagos
        pago_qs = Pagos.objects.filter(
            Q(tipo_pago__icontains=query) | 
            Q(id_proveedor__nombre__icontains=query) | 
            Q(id_herramienta__nombre__icontains=query) | 
            Q(id_insumos__nombre__icontains=query) | 
            Q(id_repuesto__nombre__icontains=query)
        ).select_related('id_proveedor',  'id_herramienta', 'id_insumos', 'id_repuesto').distinct() if query else Pagos.objects.all()
        context['pago'] = filtrar_por_fecha(pago_qs, 'fecha')
        
        # Detalle Servicio
        detalle_qs = DetalleServicio.objects.filter(
            Q(proceso__icontains=query) | 
            Q(id_vehiculo__placa__icontains=query) | 
            Q(cliente__nombre__icontains=query) | 
            Q(id_entrada__id_entrada__icontains=query) | 
            Q(id_salida__id_salida__icontains=query) 
        ).select_related('id_vehiculo',  'cliente', 'id_entrada', 'id_salida', 'empleado').distinct() if query else DetalleServicio.objects.all()
        context['detalle'] = filtrar_por_fecha(detalle_qs, 'fecha_creacion')
        
        # --- 3. Otros modelos (Solo texto) ---
        if query:
            context['repuestos'] = Repuesto.objects.filter(
                Q(id_marca__nombre__icontains=query) | Q(nombre__icontains=query) | Q(categoria__icontains=query)
            ).select_related('id_marca').distinct()
            
            context['proveedores'] = Proveedores.objects.filter(
                Q(nombre__icontains=query) | Q(telefono__icontains=query) | Q(correo__icontains=query)
            )
            # ... agrega los demás (herramientas, insumos, marcas) siguiendo este patrón
        
    return render(request, 'buscador_global.html', context)