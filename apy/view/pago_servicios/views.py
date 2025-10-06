from django.shortcuts import render
from apy.models import *
from apy.view.pago_servicios.views import *
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.urls import reverse_lazy
from apy.forms import *
from django.contrib import messages

# --------------Vistas de pago servicios publicos---------------

def pago_servicios(request):
    data = {
        'pago servicios':'pago servicios',
        'titulo':'Lista de pago servicios',
        'pago servicios': PagoServiciosPublicos.objects.all()
    }
    return render(request, 'Pago_Servicios/listar_pagoservicios.html', data)

class PagoServiciosListView(ListView):
    model = PagoServiciosPublicos
    template_name ='Pago_Servicios/listar_pagoservicios.html'
    
    # @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
       return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        nombre = {'nombre' : 'pago servicios'}
        return JsonResponse(nombre)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Pago Servicios Publicos'
        context['crear_url'] = reverse_lazy('apy:pago_servicios_crear')
        context['entidad'] = 'PagoServiciosPublicos'  
        return context
    
class PagoServiciosCreateView(CreateView):
    model = PagoServiciosPublicos
    form_class = PagoServiciosForm
    template_name = 'Pago_Servicios/crear_pagoservicios.html'
    success_url = reverse_lazy('apy:pago_servicios_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "Pago de servicio creado correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context ['titulo'] = 'Crear Pago Servicios Publicos'
        context ['entidad'] = 'PagoServiciosPublicos'
        context ['listar_url'] = reverse_lazy('apy:pago_servicios_lista')
        return context
    
class PagoServiciosUpdateView(UpdateView):
    model = PagoServiciosPublicos
    form_class = PagoServiciosForm
    template_name = 'Pago_Servicios/crear_pagoservicios.html'
    success_url = reverse_lazy('apy:pago_servicios_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "Pago de servicio actualizado correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Pago Servicios Publicos'
        context['entidad'] = 'PagoServiciosPublicos'
        context['listar_url'] = reverse_lazy('apy:pago_servicios_lista')
        return context

class PagoServiciosDeleteView(DeleteView):
    model = PagoServiciosPublicos
    template_name = 'Pago_Servicios/eliminar_pagoservicios.html'
    success_url = reverse_lazy('apy:pago_servicios_lista')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Pago de servicio eliminado correctamente")
        return super().delete(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Pago Servicios Publicos'
        context['entidad'] = 'PagoServiciosPublicos'
        context['listar_url'] = reverse_lazy('apy:pago_servicios_lista')
        return context