from django.shortcuts import render
from apy.models import *
from apy.view.vehiculos.views import *
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.urls import reverse_lazy
from apy.forms import *


def lista_vehiculos(request):
    data = {
        'vehiculos': 'vehiculos',
        'titulo': 'Lista de Vehiculos',
        'vehiculos': Vehiculo.objects.all()
    }
    return render(request, 'vehiculos/listar_vehiculos.html', data)

# vistas basadas en clases
class VehiculoListView(ListView):
    model = Vehiculo
    template_name = 'vehiculos/listar_vehiculos.html'

        # @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
       return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        nombre = {'nombre' : 'Vehiculo'}
        return JsonResponse(nombre)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Vehiculos'
        context['crear_url'] = reverse_lazy('apy:vehiculo_crear')
        context['entidad'] = 'Vehiculo'  
        return context

class VehiculoCreateView(CreateView):
    model = Vehiculo
    form_class = VehiculoForm
    template_name = 'vehiculos/crear_vehiculos.html'
    success_url = reverse_lazy('apy:vehiculo_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "Vehiculo creado correctamente")
        response = super().form_valid(form)
        
        # Si la request es AJAX, devolver JSON con el nuevo contador
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            total_vehiculos = Vehiculo.objects.count()
            return JsonResponse({
                'success': True, 
                'total_vehiculos': total_vehiculos,
                'message': 'Vehiculo creado correctamente'
            })
        
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear de Vehiculos'
        context['entidad'] = 'Vehiculo'  
        context['listar_url'] = reverse_lazy('apy:vehiculo_lista')
        return context

class VehiculoUpdateView(UpdateView):
    model = Vehiculo
    form_class = VehiculoForm
    template_name = 'vehiculos/crear_vehiculos.html'
    success_url = reverse_lazy('apy:vehiculo_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "Vehiculo actualizado correctamente")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar de Vehiculos'
        context['entidad'] = 'Vehiculo'  
        context['listar_url'] = reverse_lazy('apy:vehiculo_lista')
        return context

class VehiculoDeleteView(DeleteView):
    model = Vehiculo
    template_name = 'vehiculos/eliminar_vehiculos.html'
    success_url = reverse_lazy('apy:vehiculo_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "Vehiculo eliminado correctamente")
        return super().form_valid(form)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar de Vehiculos'
        context['entidad'] = 'Vehiculo'  
        context['listar_url'] = reverse_lazy('apy:vehiculo_lista')
        return context
    
# Vista para mostrar estadísticas
def estadisticas_view(request):
    # Contar total de vehiculos
    total_vehiculos = Vehiculo.objects.count()

    # Puedes agregar más estadísticas aquí
    context = {
        'total_vehiculos': total_vehiculos,
    }
    return render(request, 'estadisticas.html', context)

# API para actualización dinámica del contador de vehiculos
def api_contador_vehiculos(request):
    total_vehiculos = Vehiculo.objects.count()
    return JsonResponse({'total_vehiculos': total_vehiculos})