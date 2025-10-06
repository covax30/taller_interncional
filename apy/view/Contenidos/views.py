from django.shortcuts import render
from apy.models import *
from apy.view.Contenidos.views import *
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.urls import reverse_lazy
from apy.forms import *

# Create your views here.
# --------------Vistas Karol---------------

def factura(request):
    data = {
        'factura':'factura',
        'titulo':'Lista de facturas',
        'facturas': Factura.objects.all()
    }
    return render(request, 'Contenido/cont_factura.html', data)

class FacturaListView(ListView):
    model = Factura
    template_name ='Contenido/listar_factura.html'
    
    # @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
       return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        nombre = {'nombre' : 'Karol'}
        return JsonResponse(nombre)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Facturas'
        context['crear_url'] = reverse_lazy('apy:factura_crear')
        context['entidad'] = 'Factura'  
        return context
    
class FacturaCreateView(CreateView):
    model = Factura
    form_class = FacturaForm
    template_name = 'Contenido/crear_factura.html'
    success_url = reverse_lazy('apy:factura_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "Factura creada correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context ['titulo'] = 'Crear Factura'
        context ['entidad'] = 'Facturas'
        context ['listar_url'] = reverse_lazy('apy:factura_lista')
        return context
    
class FacturaUpdateView(UpdateView):
    model = Factura
    form_class = FacturaForm
    template_name = 'Contenido/crear_factura.html'
    success_url = reverse_lazy('apy:factura_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "Factura actualizada correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Factura'
        context['entidad'] = 'Facturas'
        context['listar_url'] = reverse_lazy('apy:factura_lista')
        return context

class FacturaDeleteView(DeleteView):
    model = Factura
    template_name = 'Contenido/eliminar_factura.html'
    success_url = reverse_lazy('apy:factura_lista')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Factura eliminada correctamente")
        return super().delete(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Factura'
        context['entidad'] = 'Facturas'
        context['listar_url'] = reverse_lazy('apy:factura_lista')
        return context
