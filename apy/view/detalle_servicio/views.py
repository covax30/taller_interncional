from django.shortcuts import render
from apy.models import *
from apy.view.detalle_servicio.views import *
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.urls import reverse_lazy
from apy.forms import *
from django.contrib import messages

# Create your views here.
# --------------Vistas Yury---------------
def detalle_servicio(request):
    data = {
        'Detalle_Servicio':'Detalle_Servicio',
        'titulo':'Lista de Detalle de Servicios',
        'detalle_servicios': DetalleServicio.objects.all()
    }
    return render(request, 'detalle_servicio/cont_detalle_servicio.html', data)

class DetalleServicioListView(ListView):
    model = DetalleServicio
    template_name ='detalle_servicio/listar_detalle_servicio.html'
    
    # @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
       return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        nombre = {'nombre' : 'Yury'}
        return JsonResponse(nombre)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Detalle de Servicios'
        context['crear_url'] = reverse_lazy('apy:detalle_servicio_crear')
        context['entidad'] = 'Detalle de Servicio'  
        return context
    
class DetalleServicioCreateView(CreateView):
    model = DetalleServicio
    form_class = DetalleServicioForm
    template_name = 'detalle_servicio/crear_detalle_servicio.html'
    success_url = reverse_lazy('apy:detalle_servicio_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "Detalle de Servicio creado correctamente")
        return super().form_valid(form)
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context ['titulo'] = 'Crear Detalle de Servicio'
        context ['entidad'] = 'Detalle de Servicios'
        context ['listar_url'] = reverse_lazy('apy:detalle_servicio_lista')
        
        return context
    
class DetalleServicioUpdateView(UpdateView):
    model = DetalleServicio
    form_class = DetalleServicioForm    
    template_name = 'detalle_servicio/crear_detalle_servicio.html'
    success_url = reverse_lazy('apy:detalle_servicio_lista')
    def form_valid(self, form):
        messages.success(self.request, "detalle de servicio actualizado correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context ['titulo'] = 'Editar Detalle de Servicio'
        context ['entidad'] = 'Detalle de Servicios'
        context ['listar_url'] = reverse_lazy('apy:detalle_servicio_lista')
        
        return context
class DetalleServicioDeleteView(DeleteView):
    model = DetalleServicio
    template_name = 'detalle_servicio/eliminar_detalle_servicio.html'
    success_url = reverse_lazy('apy:detalle_servicio_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "Detalle de servicio eliminado correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context ['titulo'] = 'Eliminar Detalle de Servicio'
        context ['entidad'] = 'Detalle de Servicios'
        context ['listar_url'] = reverse_lazy('apy:detalle_servicio_lista')
        
        return context
    
    
