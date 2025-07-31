from django.shortcuts import render
from apy.models import *
from apy.view.compras.views import *
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.urls import reverse_lazy
from apy.forms import *


def lista_compras(request):
    data = {
        'compras': 'compras',
        'titulo': 'Lista de Compras',
        'compras': Compras.objects.all()
    }
    return render(request, 'compras/listar_compras.html', data)

# vistas basadas en clases
class CompraListView(ListView):
    model = Compra
    template_name = 'compras/listar_compras.html'

        # @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
       return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        nombre = {'nombre' : 'Compra'}
        return JsonResponse(nombre)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Compras'
        context['crear_url'] = reverse_lazy('apy:compra_crear')
        context['entidad'] = 'Compra'  
        return context

class CompraCreateView(CreateView):
    model = Compra
    form_class = CompraForm
    template_name = 'compras/crear_compras.html'
    success_url = reverse_lazy('apy:compra_lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear de Compras'
        context['entidad'] = 'Compra'  
        context['listar_url'] = reverse_lazy('apy:compra_lista')
        return context

class CompraUpdateView(UpdateView):
    model = Compra
    form_class = CompraForm
    template_name = 'compras/crear_compras.html'
    success_url = reverse_lazy('apy:compra_lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar de Compras'
        context['entidad'] = 'Compra'  
        context['listar_url'] = reverse_lazy('apy:compra_lista')
        return context

class CompraDeleteView(DeleteView):
    model = Compra
    template_name = 'compras/eliminar_compras.html'
    success_url = reverse_lazy('apy:compra_lista')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar de Compras'
        context['entidad'] = 'Compra'  
        context['listar_url'] = reverse_lazy('apy:compra_lista')
        return context