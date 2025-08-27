from django.shortcuts import render
from apy.models import *
from apy.view.Nomina.views import *
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.urls import reverse_lazy
from apy.forms import *
from django.contrib import messages

# Create your views here.
# --------------Vistas Karol---------------

def nomina(request):
    data = {
        'Nomina':'Nomina',
        'titulo':'Lista de Pago de Nomina',
        'nominas': Nomina.objects.all()
    }
    return render(request, 'Nomina/cont_Nomina.html', data)

class NominaListView(ListView):
    model = Nomina
    template_name = 'Nomina/listar_nomina.html'
   
    
    # @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
       return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        nombre = {'nombre' : 'Yury'}
        return JsonResponse(nombre)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista pago de Nomina'
        context['crear_url'] = reverse_lazy('apy:nomina_crear')
        context['entidad'] = 'Nomina'  
        return context
    
class NominaCreateView(CreateView):
    model = Nomina
    form_class = NominaForm
    template_name = 'Nomina/crear_nomina.html'
    success_url = reverse_lazy('apy:nomina_lista')
    def form_valid(self, form):
        messages.success(self.request, "Nomina creada correctamente")
        return super().form_valid(form)
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Nomina'
        context['entidad'] = 'Nomina'
        context['listar_url'] = reverse_lazy('apy:nomina_lista')
        return context
    
    
    
class NominaUpdateView(UpdateView):
    model = Nomina
    form_class = NominaForm
    
    template_name = 'Nomina/crear_nomina.html'
    success_url = reverse_lazy('apy:nomina_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "Nomina actualizada correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar empleado'
        context['entidad'] = 'Nomina'
        context['listar_url'] = reverse_lazy('apy:nomina_lista')
        return context

class NominaDeleteView(DeleteView):
    model = Nomina
    template_name = 'Nomina/eliminar_nomina.html'
    success_url = reverse_lazy('apy:nomina_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "Nomina eliminado correctamente")
        return super().form_valid(form)

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar pago de Nomina'
        context['entidad'] = 'Nomina'
        context['listar_url'] = reverse_lazy('apy:nomina_lista')
        return context
