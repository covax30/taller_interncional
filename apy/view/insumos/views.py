from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.urls import reverse_lazy
from apy.forms import *
from django.contrib import messages

# Create your views here.
# --------------Vistas erick---------------

class InsumoListView(ListView):
    model = Insumos
    template_name = 'insumos/listar.html'
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Insumos'
        context['crear_url'] = reverse_lazy('apy:insumo_crear')
        context['entidad'] = 'Insumo'
        return context
    
class InsumoCreateView(CreateView):
    model = Insumos
    form_class = InsumoForm
    template_name = 'insumos/crear.html'
    success_url = reverse_lazy('apy:insumo_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "Insumo creado correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Insumo'
        context['entidad'] = 'Insumo'
        context['listar_url'] = reverse_lazy('apy:insumo_lista')
        return context
    
class InsumoUpdateView(UpdateView):
    model = Insumos
    form_class = InsumoForm
    template_name = 'insumos/crear.html'
    success_url = reverse_lazy('apy:insumo_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "Insumo actualizado correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Insumo'
        context['entidad'] = 'Insumo'
        context['listar_url'] = reverse_lazy('apy:insumo_lista')
        return context
    
class InsumoDeleteView(DeleteView):
    model = Insumos
    template_name = 'insumos/eliminar.html'
    success_url = reverse_lazy('apy:insumo_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "Insumo eliminado correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Insumo'
        context['entidad'] = 'Insumo'
        context['listar_url'] = reverse_lazy('apy:insumo_lista')
        return context
    
# Vista para mostrar estadísticas
def estadisticas_view(request):
    # Contar total de insumos
    total_insumos = Insumos.objects.count()

    # Puedes agregar más estadísticas aquí
    context = {
        'total_insumos': total_insumos,
    }
    return render(request, 'estadisticas.html', context)

# API para actualización dinámica del contador de insumos
def api_contador_insumos(request):
    total_insumos = Insumos.objects.count()
    return JsonResponse({'total_insumos': total_insumos})