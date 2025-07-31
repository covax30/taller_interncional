from django.shortcuts import render
from apy.models import *
from apy.view.Gastos.views import *
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.urls import reverse_lazy
from apy.forms import *

# Create your views here.
# --------------Vistas Karol---------------

def gasto(request):
    data = {
        'Gastos':'Gastos',
        'titulo':'Lista de Gastos',
        'Gastos': Gastos.objects.all()
    }
    return render(request, 'Gastos/cont_gastos.html', data)

class GastosListView(ListView):
    model = Gastos
    template_name ='Gastos/listar_gasto.html'
    
    # @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
       return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        nombre = {'nombre' : 'Yury'}
        return JsonResponse(nombre)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Gastos'
        context['crear_url'] = reverse_lazy('apy:gasto_crear')
        context['entidad'] = 'Gastos'  
        return context
    
class GastosCreateView(CreateView):
    model = Gastos
    form_class = GastosForm
    template_name = 'Gastos/crear_gasto.html'
    success_url = reverse_lazy('apy:gasto_lista')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context ['titulo'] = 'Crear Gasto'
        context ['entidad'] = 'Gastos'
        context ['listar_url'] = reverse_lazy('apy:gasto_lista')
        return context
    
class GastosUpdateView(UpdateView):
    model = Gastos
    form_class = GastosForm
    template_name = 'Gastos/crear_gasto.html'
    success_url = reverse_lazy('apy:gasto_lista')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Gasto'
        context['entidad'] = 'Gastos'
        context['listar_url'] = reverse_lazy('apy:gasto_lista')
        return context

class GastosDeleteView(DeleteView):
    model = Gastos
    template_name = 'Gastos/eliminar_gasto.html'
    success_url = reverse_lazy('apy:gasto_lista')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Gastos'
        context['entidad'] = 'Gastos'
        context['listar_url'] = reverse_lazy('apy:gasto_lista')
        return context
