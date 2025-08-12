from django.shortcuts import render
from apy.models import *
from apy.view.Marca.views import *
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.urls import reverse_lazy
from apy.forms import *
from django.contrib import messages

# Create your views here.
# --------------Vistas Karol---------------

def marca(request):
    data = {
        'Marca':'Marca',
        'titulo':'Lista de Marcas',
        'marcas': Empleado.objects.all()
    }
    return render(request, 'Marca/cont_Marca.html', data)

class MarcaListView(ListView):
    model = Marca
    template_name ='Marca/listar_marca.html'
    
    # @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
       return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        nombre = {'nombre' : 'Yury'}
        return JsonResponse(nombre)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Marcas'
        context['crear_url'] = reverse_lazy('apy:marca_crear')
        context['entidad'] = 'Marcas'  
        return context
    
class MarcaCreateView(CreateView):
    model = Marca
    form_class = MarcaForm
    template_name = 'Marca/crear_marca.html'
    success_url = reverse_lazy('apy:marca_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "Marca creada correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context ['titulo'] = 'Crear Marca'
        context ['entidad'] = 'Marca'
        context ['listar_url'] = reverse_lazy('apy:marca_lista')
        return context
    
class MarcaUpdateView(UpdateView):
    model = Marca
    form_class = MarcaForm
    template_name = 'Marca/crear_marca.html'
    success_url = reverse_lazy('apy:marca_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "Marca actualizada correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar marca'
        context['entidad'] = '  Marcas'
        context['listar_url'] = reverse_lazy('apy:marca_lista')
        return context

class MarcaDeleteView(DeleteView):
    model = Marca
    template_name = 'Marca/eliminar_marca.html'
    success_url = reverse_lazy('apy:marca_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "Marca eliminada correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Marca'
        context['entidad'] = ' Marcas'
        context['listar_url'] = reverse_lazy('apy:marca_lista')
        return context
