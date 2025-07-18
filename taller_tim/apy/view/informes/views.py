from django.shortcuts import render
from apy.models import *
from apy.view.informes.views import *
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.urls import reverse_lazy
from apy.forms import *

# --------------Vistas de informes---------------

def informes(request):
    data = {
        'informe':'informe',
        'titulo':'Lista de informes',
        'informe': Administrador.objects.all()
    }
    return render(request, 'Informes/listar_administradores.html', data)

class InformesListView(ListView):
    model = Informes
    template_name ='Informes/listar_informe.html'
    
    # @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
       return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        nombre = {'nombre' : 'Informes'}
        return JsonResponse(nombre)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Informes'
        context['crear_url'] = reverse_lazy('apy:informes_crear')
        context['entidad'] = 'Informes'  
        return context
    
class InformesCreateView(CreateView):
    model = Informes
    form_class = InformeForm
    template_name = 'Informes/crear_informe.html'
    success_url = reverse_lazy('apy:informes_lista')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context ['titulo'] = 'Crear Informe'
        context ['entidad'] = 'Informes'
        context ['listar_url'] = reverse_lazy('apy:informes_lista')
        return context
    
class InformesUpdateView(UpdateView):
    model = Informes
    form_class = InformeForm
    template_name = 'Informes/crear_informe.html'
    success_url = reverse_lazy('apy:informes_lista')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Informe'
        context['entidad'] = 'Informes'
        context['listar_url'] = reverse_lazy('apy:informes_lista')
        return context

class InformesDeleteView(DeleteView):
    model = Informes
    template_name = 'Informes/eliminar_informe.html'
    success_url = reverse_lazy('apy:informes_lista')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Informe'
        context['entidad'] = 'Informes'
        context['listar_url'] = reverse_lazy('apy:informes_lista')
        return context