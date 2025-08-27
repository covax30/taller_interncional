from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.urls import reverse_lazy
from apy.forms import *
from django.db.models import F
from apy.models import Repuesto
from apy.forms import RepuestoForm

# Create your views here.
# --------------Vistas erick---------------

class RepuestoListView(ListView):
    model = Repuesto
    template_name = 'repuestos/listar.html'
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Repuestos'
        context['crear_url'] = reverse_lazy('apy:repuesto_crear')
        context['entidad'] = 'Repuesto'
        return context
    
class RepuestoCreateView(CreateView):
    model = Repuesto
    form_class = RepuestoForm
    template_name = 'repuestos/crear.html'
    success_url = reverse_lazy('apy:repuesto_lista')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Repuesto'
        context['entidad'] = 'Repuesto'
        context['listar_url'] = reverse_lazy('apy:repuesto_lista')
        return context
    
class RepuestoUpdateView(UpdateView):
    model = Repuesto
    form_class = RepuestoForm
    template_name = 'repuestos/crear.html'
    success_url = reverse_lazy('apy:repuesto_lista')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Repuesto'
        context['entidad'] = 'Repuesto'
        context['listar_url'] = reverse_lazy('apy:repuesto_lista')
        return context
    
class RepuestoDeleteView(DeleteView):
    model = Repuesto
    template_name = 'repuestos/eliminar.html'
    success_url = reverse_lazy('apy:repuesto_lista')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Repuesto'
        context['entidad'] = 'Repuesto'
        context['listar_url'] = reverse_lazy('apy:repuesto_lista')
        return context


@csrf_exempt
def repuestos_bajo_stock_api(request):
    repuestos = Repuesto.objects.filter(stock__lt=F('stock_minimo'))
    data = [
        {
            'id': r.id,
            'nombre': r.nombre,
            'stock': r.stock,
            'stock_minimo': r.stock_minimo
        }
        for r in repuestos
    ]
    return JsonResponse(data, safe=False)