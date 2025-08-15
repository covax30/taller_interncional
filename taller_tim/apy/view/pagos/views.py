from django.shortcuts import render
from apy.models import *
from apy.view.pagos.views import *
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.urls import reverse_lazy
from apy.forms import *
from django.contrib import messages

# --------------Vistas de pagos---------------

def pagos(request):
    data = {
        'pagos':'pagos',
        'titulo':'Lista de pagos',
        'pagos': Pagos.objects.all()
    }
    return render(request, 'Pagos/listar_pago.html', data)

class PagosListView(ListView):
    model = Pagos
    template_name ='Pagos/listar_pago.html'
    
    # @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
       return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        nombre = {'nombre' : 'pago'}
        return JsonResponse(nombre)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Pagos'
        context['crear_url'] = reverse_lazy('apy:pagos_crear')
        context['entidad'] = 'Pagos'  
        return context
    
class PagosCreateView(CreateView):
    model = Pagos
    form_class = PagosForm
    template_name = 'Pagos/crear_pago.html'
    success_url = reverse_lazy('apy:pagos_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "Pago creado correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context ['titulo'] = 'Crear Pagos'
        context ['entidad'] = 'Pagos'
        context ['listar_url'] = reverse_lazy('apy:pagos_lista')
        return context
    
class PagosUpdateView(UpdateView):
    model = Pagos
    form_class = PagosForm
    template_name = 'Pagos/crear_pago.html'
    success_url = reverse_lazy('apy:pagos_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "Pago actualizado correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Pagos'
        context['entidad'] = 'Pagos'
        context['listar_url'] = reverse_lazy('apy:pagos_lista')
        return context

class PagosDeleteView(DeleteView):
    model = PagoServiciosPublicos
    template_name = 'Pagos/eliminar_pago.html'
    success_url = reverse_lazy('apy:pagos_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "Pago actualizado correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Pagos'
        context['entidad'] = 'Pagos'
        context['listar_url'] = reverse_lazy('apy:pagos_lista')
        return context