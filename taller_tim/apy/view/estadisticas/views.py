from django.shortcuts import render
from apy.models import *
from django.urls import reverse_lazy
from apy.forms import *

def estadisticas(request):
    data = {
        'estadisticas': 'estadisticas',
        'titulo': 'Estadisticas',
    }
    return render(request, 'estadisticas.html', data)