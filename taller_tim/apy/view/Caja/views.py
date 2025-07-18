from django.shortcuts import render
from apy.models import *
from apy.view.Caja.views import *
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.urls import reverse_lazy
from apy.forms import *

# Create your views here.
# --------------Vistas Karol---------------

def caja(request):
    data = {
        'Caja':'Caja',
        'titulo':'Lista de Caja',
        'caja': Caja.objects.all()
    }
    return render(request, 'Caja/cont_Caja.html', data)

class CajaListView(ListView):
    model = Caja
    template_name = 'Caja/listar_caja.html'
    
   
    
    # @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
       return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        nombre = {'nombre' : 'Yury'}
        return JsonResponse(nombre)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista Caja'
        context['crear_url'] = reverse_lazy('apy:caja_crear')
        context['entidad'] = '  Caja  '  
        return context
    
class CajaCreateView(CreateView):
    model = Caja
    form_class = CajaForm
    template_name = 'Caja/crear_caja.html'
    success_url = reverse_lazy('apy:caja_lista')
    
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Caja'
        context['entidad'] = 'Caja'
        context['listar_url'] = reverse_lazy('apy:caja_lista')
        return context
    
    
    
class CajaUpdateView(UpdateView):
    model = Caja
    form_class = CajaForm
    template_name = 'Caja/crear_caja.html'
    success_url = reverse_lazy('apy:caja_lista')

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Caja'
        context['entidad'] = 'Caja'
        context['listar_url'] = reverse_lazy('apy:caja_lista')
        return context

class CajaDeleteView(DeleteView):
    model = Nomina
    template_name = 'Caja/eliminar_caja.html'
    success_url = reverse_lazy('apy:caja_lista')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Registro Caja'
        context['entidad'] = 'Caja'
        context['listar_url'] = reverse_lazy('apy:caja_lista')
        return context
