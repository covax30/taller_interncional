from django.shortcuts import render
from apy.models import *
from apy.view.entrada_vehiculos.views import *
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.urls import reverse_lazy
from apy.forms import *


from apy.models import Cliente


def lista_entrada_vehiculos(request):
    data = {
        'entrada_vehiculos': 'entrada_vehiculos',
        'titulo': 'Lista de Entrada de Vehiculos',
        'entrada_vehiculos': EntradaVehiculo.objects.all()
    }
    return render(request, 'entrada_vehiculos/listar_entrada_vehiculos.html', data)

# vistas basadas en clases
class EntradaVehiculoListView(ListView):
    model = EntradaVehiculo
    template_name = 'entrada_vehiculos/listar_entrada_vehiculos.html'

        # @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
       return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        nombre = {'nombre' : 'Entrada de Vehiculos'}
        return JsonResponse(nombre)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Entrada de Vehiculos'
        context['crear_url'] = reverse_lazy('apy:entrada_vehiculo_crear')
        context['entidad'] = 'Entrada de Vehiculos'  
        return context

class EntradaVehiculoCreateView(CreateView):
    model = EntradaVehiculo
    form_class = EntradaVehiculoForm
    template_name = 'entrada_vehiculos/crear_entrada_vehiculos.html'
    success_url = reverse_lazy('apy:entrada_vehiculo_lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear de Entrada de Vehiculos'
        context['entidad'] = 'Entrada de Vehiculos'  
        context['listar_url'] = reverse_lazy('apy:entrada_vehiculo_lista')
        return context

class EntradaVehiculoUpdateView(UpdateView):
    model = EntradaVehiculo
    form_class = EntradaVehiculoForm
    template_name = 'entrada_vehiculos/crear_entrada_vehiculos.html'
    success_url = reverse_lazy('apy:entrada_vehiculo_lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar de Entrada de Vehiculos'
        context['entidad'] = 'Entrada de Vehiculos'  
        context['listar_url'] = reverse_lazy('apy:entrada_vehiculo_lista')
        return context

class EntradaVehiculoDeleteView(DeleteView):
    model = EntradaVehiculo
    template_name = 'entrada_vehiculos/eliminar_entrada_vehiculos.html'
    success_url = reverse_lazy('apy:entrada_vehiculo_lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar de Entrada de Vehiculos'
        context['entidad'] = 'Entrada de Vehiculos'  
        context['listar_url'] = reverse_lazy('apy:entrada_vehiculo_lista')
        return context