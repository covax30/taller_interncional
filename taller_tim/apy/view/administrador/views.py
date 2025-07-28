from django.shortcuts import render
from apy.models import *
from apy.view.administrador.views import *
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.urls import reverse_lazy
from apy.forms import *

# --------------Vistas de administrador---------------

def administrador(request):
    data = {
        'administrador':'administrador',
        'titulo':'Lista de administradores',
        'administrador': Administrador.objects.all()
    }
    return render(request, 'Administrador/listar_administradores.html', data)

class AdministradorListView(ListView):
    model = Administrador
    template_name ='Administrador/listar_administrador.html'
    
    # @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
       return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        nombre = {'nombre' : 'Administrador'}
        return JsonResponse(nombre)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Administradores'
        context['crear_url'] = reverse_lazy('apy:administrador_crear')
        context['entidad'] = 'Administrador'  
        return context
    
class AdministradorCreateView(CreateView):
    model = Administrador
    form_class = AdministradorForm
    template_name = 'Administrador/crear_administrador.html'
    success_url = reverse_lazy('apy:administrador_lista')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context ['titulo'] = 'Crear Administrador'
        context ['entidad'] = 'Administradores'
        context ['listar_url'] = reverse_lazy('apy:administrador_lista')
        return context
    
class AdministradorUpdateView(UpdateView):
    model = Administrador
    form_class = AdministradorForm
    template_name = 'Administrador/crear_administrador.html'
    success_url = reverse_lazy('apy:administrador_lista')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Administrador'
        context['entidad'] = 'Administradores'
        context['listar_url'] = reverse_lazy('apy:administrador_lista')
        return context

class AdministradorDeleteView(DeleteView):
    model = Administrador
    template_name = 'Administrador/eliminar_administrador.html'
    success_url = reverse_lazy('apy:administrador_lista')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Administrador'
        context['entidad'] = 'Administradores'
        context['listar_url'] = reverse_lazy('apy:administrador_lista')
        return context