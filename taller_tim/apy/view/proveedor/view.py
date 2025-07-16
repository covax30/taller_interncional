from django.shortcuts import render
from apy.models import *
from apy.view.proveedor.view import *
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.urls import reverse_lazy
from apy.forms import *

# Create your views here.
# --------------Vistas Karol---------------

def proveedor(request):
    data = {
        'proveedor':'proveedor',
        'titulo':'Lista de proveedores',
        'proveedor': Proveedores.objects.all()
    }
    return render(request, 'Proveedores/listar_proveedores.html', data)

class ProveedorListView(ListView):
    model = Proveedores
    template_name ='Proveedores/listar_proveedores.html'
    
    # @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
       return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        nombre = {'nombre' : 'Proveedor'}
        return JsonResponse(nombre)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Proveedores'
        context['crear_url'] = reverse_lazy('apy:proveedor_crear')
        context['entidad'] = 'Proveedor'  
        return context
    
class ProveedorCreateView(CreateView):
    model = Proveedores
    form_class = ProveedorForm
    template_name = 'Proveedores/crear_proveedor.html'
    success_url = reverse_lazy('apy:proveedor_lista')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context ['titulo'] = 'Crear Proveedor'
        context ['entidad'] = 'Proveedores'
        context ['listar_url'] = reverse_lazy('apy:proveedor_lista')
        return context
    
class ProveedorUpdateView(UpdateView):
    model = Proveedores
    form_class = ProveedorForm
    template_name = 'Proveedores/crear_proveedor.html'
    success_url = reverse_lazy('apy:proveedor_lista')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Proveedor'
        context['entidad'] = 'Proveedores'
        context['listar_url'] = reverse_lazy('apy:proveedor_lista')
        return context

class ProveedorDeleteView(DeleteView):
    model = Proveedores
    template_name = 'Proveedores/eliminar_proveedor.html'
    success_url = reverse_lazy('apy:proveedor_lista')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Proveedor'
        context['entidad'] = 'Proveedores'
        context['listar_url'] = reverse_lazy('apy:proveedor_lista')
        return context
