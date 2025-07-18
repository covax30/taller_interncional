from django.shortcuts import render
from apy.models import *
from apy.view.clientes.views import *
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.urls import reverse_lazy
from apy.forms import *


def lista_clientes(request):
    data = {
        'clientes': 'clientes',
        'titulo': 'Lista de Clientes',
        'clientes': Cliente.objects.all()
    }
    return render(request, 'clientes/listar_clientes.html', data)

# vistas basadas en clases
class ClienteListView(ListView):
    model = Cliente
    template_name = 'clientes/listar_clientes.html'

        # @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
       return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        nombre = {'nombre' : 'Cliente'}
        return JsonResponse(nombre)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Clientes'
        context['crear_url'] = reverse_lazy('apy:cliente_crear')
        context['entidad'] = 'Cliente'  
        return context
    
class ClienteCreateView(CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'clientes/crear_clientes.html'
    success_url = reverse_lazy('apy:cliente_lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear de Clientes'
        context['entidad'] = 'Cliente'  
        context['listar_url'] = reverse_lazy('apy:cliente_lista')
        return context
    
class ClienteUpdateView(UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'clientes/crear_clientes.html'
    success_url = reverse_lazy('apy:cliente_lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar de Clientes'
        context['entidad'] = 'Cliente'  
        context['listar_url'] = reverse_lazy('apy:cliente_lista')
        return context
    
class ClienteDeleteView(DeleteView):
    model = Cliente
    template_name = 'clientes/eliminar_clientes.html'
    success_url = reverse_lazy('apy:cliente_lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar de Clientes'
        context['entidad'] = 'Cliente'  
        context['listar_url'] = reverse_lazy('apy:cliente_lista')
        return context