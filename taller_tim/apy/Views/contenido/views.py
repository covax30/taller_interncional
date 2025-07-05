from django.shortcuts import render
from apy.models import *
from apy.Views.contenido.views import *

# Create your views here.
# --------------Vistas Karol---------------

def factura(request):
    data = {
        'factura':'factura',
        'titulo':'Lista de facturas',
        'facturas': Factura.objects.all()
    }
    return render(request, 'Contenido/cont_factura.html', data)

def contacto(request):
    data = {
        'contacto':'contacto',
        'titulo':'Contactanos'
    }
    return render(request, 'Contenido/cont_contacto.html', data)
