from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.urls import reverse_lazy
from apy.forms import *

# Create your views here.
# --------------Vistas erick---------------

def listar_tipo_mantenimiento(request):
    data = {
        'tipo_mantenimiento': 'tipo_mantenimiento',
        'titulo': 'Lista de Tipos de Mantenimiento',
        'tipos_mantenimiento': TipoMantenimiento.objects.all()
    }
    return render(request, 'tipo_mantenimiento/listar.html', data)

class TipoMantenimientoListView(ListView):
    model = TipoMantenimiento
    template_name = 'tipo_mantenimiento/listar.html'
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Tipos de Mantenimiento'
        context['crear_url'] = reverse_lazy('apy:tipo_mantenimiento_crear')
        context['entidad'] = 'Tipo de Mantenimiento'
        return context

class TipoMantenimientoCreateView(CreateView):
    model = TipoMantenimiento
    form_class = TipoMantenimientoForm
    template_name = 'tipo_mantenimiento/crear.html'
    success_url = reverse_lazy('apy:tipo_mantenimiento_lista')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Tipo de Mantenimiento'
        context['entidad'] = 'Tipo de Mantenimiento'
        context['listar_url'] = reverse_lazy('apy:tipo_mantenimiento_lista')
        return context

class TipoMantenimientoUpdateView(UpdateView):
    model = TipoMantenimiento
    form_class = TipoMantenimientoForm
    template_name = 'tipo_mantenimiento/crear.html'
    success_url = reverse_lazy('apy:tipo_mantenimiento_lista')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Tipo de Mantenimiento'
        context['entidad'] = 'Tipo de Mantenimiento'
        context['listar_url'] = reverse_lazy('apy:tipo_mantenimiento_lista')
        return context

class TipoMantenimientoDeleteView(DeleteView):
    model = TipoMantenimiento
    template_name = 'tipo_mantenimiento/eliminar.html'
    success_url = reverse_lazy('apy:tipo_mantenimiento_lista')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Tipo de Mantenimiento'
        context['entidad'] = 'Tipo de Mantenimiento'
        return context