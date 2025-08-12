from django.shortcuts import render
from apy.models import *
from apy.view.salida_vehiculos.views import *
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.urls import reverse_lazy
from apy.forms import *


from apy.models import Cliente


def lista_salida_vehiculos(request):
    data = {
        'salida_vehiculos': 'salida_vehiculos',
        'titulo': 'Lista de Salida de Vehiculos',
        'salida_vehiculos': SalidaVehiculo.objects.all()
    }
    return render(request, 'salida_vehiculos/listar_salida_vehiculos.html', data)

# vistas basadas en clases
class SalidaVehiculoListView(ListView):
    model = SalidaVehiculo
    template_name = 'salida_vehiculos/listar_salida_vehiculos.html'

        # @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
       return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        nombre = {'nombre' : 'Salida de Vehiculos'}
        return JsonResponse(nombre)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Salida de Vehiculos'
        context['crear_url'] = reverse_lazy('apy:salida_vehiculo_crear')
        context['entidad'] = 'Salida de Vehiculos'  
        return context

class SalidaVehiculoCreateView(CreateView):
    model = SalidaVehiculo
    form_class = SalidaVehiculoForm
    template_name = 'salida_vehiculos/crear_salida_vehiculos.html'
    success_url = reverse_lazy('apy:salida_vehiculo_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "Salida de Vehiculo creada correctamente")
        return super().form_valid(form)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear de Salida de Vehiculos'
        context['entidad'] = 'Salida de Vehiculos'  
        context['listar_url'] = reverse_lazy('apy:salida_vehiculo_lista')
        return context

class SalidaVehiculoUpdateView(UpdateView):
    model = SalidaVehiculo
    form_class = SalidaVehiculoForm
    template_name = 'salida_vehiculos/crear_salida_vehiculos.html'
    success_url = reverse_lazy('apy:salida_vehiculo_lista')

    def form_valid(self, form):
        messages.success(self.request, "Salida de Vehiculo actualizada correctamente")
        return super().form_valid(form)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar de Salida de Vehiculos'
        context['entidad'] = 'Salida de Vehiculos'  
        context['listar_url'] = reverse_lazy('apy:salida_vehiculo_lista')
        return context

class SalidaVehiculoDeleteView(DeleteView):
    model = SalidaVehiculo
    template_name = 'salida_vehiculos/eliminar_salida_vehiculos.html'
    success_url = reverse_lazy('apy:salida_vehiculo_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "Salida de Vehiculo eliminada correctamente")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar de Salida de Vehiculos'
        context['entidad'] = 'Salida de Vehiculos'  
        context['listar_url'] = reverse_lazy('apy:salida_vehiculo_lista')
        return context