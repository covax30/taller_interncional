from django.shortcuts import render
from apy.models import *
from apy.view.Contenidos.views import *
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.urls import reverse_lazy
from apy.forms import *

# Create your views here.
# --------------Vistas erick---------------

class MantenimientoListView(ListView):
    model = Mantenimiento
    template_name = 'gestion_mantenimiento/listar.html'
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Mantenimientos'
        context['crear_url'] = reverse_lazy('apy:mantenimiento_crear')
        context['entidad'] = 'Mantenimiento'
        return context

class MantenimientoCreateView(CreateView):
    model = Mantenimiento
    form_class = MantenimientoForm
    template_name = 'gestion_mantenimiento/crear.html'
    success_url = reverse_lazy('apy:mantenimiento_lista')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Mantenimiento'
        context['entidad'] = 'Mantenimiento'
        context['listar_url'] = reverse_lazy('apy:mantenimiento_lista')
        return context
    
class MantenimientoUpdateView(UpdateView):
    model = Mantenimiento
    form_class = MantenimientoForm
    template_name = 'gestion_mantenimiento/crear.html'
    success_url = reverse_lazy('apy:mantenimiento_lista')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Mantenimiento'
        context['entidad'] = 'Mantenimiento'
        context['listar_url'] = reverse_lazy('apy:mantenimiento_lista')
        return context

class MantenimientoDeleteView(DeleteView):
    model = Mantenimiento
    template_name = 'gestion_mantenimiento/eliminar.html'
    success_url = reverse_lazy('apy:mantenimiento_lista')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Mantenimiento'
        context['entidad'] = 'Mantenimiento'
        context['listar_url'] = reverse_lazy('apy:mantenimiento_lista')
        return context
