from django.shortcuts import render
from django.http import HttpResponse,JsonResponse

# Create your views here.
# --------------Vistas Karol---------------

def vista_administrador(request):
    return render(request, 'vista_admin.html')

def vista_informes(request):
    return render(request, 'vista_informes.html')

def vista_pago_servicios(request):
    return render(request, 'vista_pago_servicios.html')

def vista_proveedores(request):
    return render(request, 'vista_proveedores.html')

def vista_pagos(request):
    return render(request, 'vista_pagos.html')

# --------------Vistas erick---------------

def vista_gestion_mantenimiento(request):
    return render(request, 'vista_gestion_mantenimiento.html')

def vista_tipo_mantenimiento(request):
    return render(request, 'vista_tipo_mantenimiento.html')

def vista_herramientas(request):
    return render(request, 'vista_herramienta.html')

def vista_repuestos(request):
    return render(request, 'vista_repuestos.html')

def vista_insumos(request):
    return render(request, 'vista_insumos.html')

# --------------Vistas Steven --------------
def vista_entrada_vehiculos(request):
    return render(request, 'vista_entrada_vehiculos.html')

def vista_salida_vehiculos(request):
    return render(request, 'vista_salida_vehiculos.html')

def vista_vehiculos(request):
    return render(request, 'vista_vehiculos.html')

def vista_clientes(request):
    return render(request, 'vista_clientes.html')

def vista_compras(request):
    return render(request, 'vista_compras.html')
