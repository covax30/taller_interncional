from django.shortcuts import render
from apy.models import *
from apy.view.Contenidos.views import *
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.urls import reverse_lazy
from apy.forms import *

# Create your views here.
# --------------Vistas erick---------------

class MantenimientoListView(ListView):
    model = Mantenimiento
    template_name = 'gestion_mantenimiento/listar.html'
    
    @method_decorator(csrf_exempt) 
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Mantenimientos'
        context['crear_url'] = reverse_lazy('apy:mantenimiento_crear')
        context['entidad'] = 'Mantenimiento'
        return context

class MantenimientoCreateView(CreateView):
    model = Mantenimiento
    form_class = MantenimientoForm
    template_name = 'gestion_mantenimiento/crear.html'
    success_url = reverse_lazy('apy:mantenimiento_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "Mantenimiento creado correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Mantenimiento'
        context['entidad'] = 'Mantenimiento'
        context['listar_url'] = reverse_lazy('apy:mantenimiento_lista')
        return context
    
class MantenimientoUpdateView(UpdateView):
    model = Mantenimiento
    form_class = MantenimientoForm
    template_name = 'gestion_mantenimiento/crear.html'
    success_url = reverse_lazy('apy:mantenimiento_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "Mantenimiento editado correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Mantenimiento'
        context['entidad'] = 'Mantenimiento'
        context['listar_url'] = reverse_lazy('apy:mantenimiento_lista')
        return context

class MantenimientoDeleteView(DeleteView):
    model = Mantenimiento
    template_name = 'gestion_mantenimiento/eliminar.html'
    success_url = reverse_lazy('apy:mantenimiento_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "Mantenimiento eliminado correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Mantenimiento'
        context['entidad'] = 'Mantenimiento'
        context['listar_url'] = reverse_lazy('apy:mantenimiento_lista')
        return context
    
class MantenimientoCreateModalView(CreateView):
    model = Mantenimiento
    form_class = MantenimientoForm
    template_name = "gestion_mantenimiento/modal_mantenimiento.html"
    success_url = reverse_lazy("apy:mantenimiento_lista")

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        try:
            self.object = form.save()
            return JsonResponse({
                "success": True,
                "id": self.object.id,
                "text": str(self.object),
                "message": "Mantenimiento registrado correctamente ✅"
            })
        except Exception as e:
            return JsonResponse({
                "success": False,
                "message": f"Error al guardar: {str(e)}"
            }, status=500)
    
    def form_invalid(self, form):
        html = render_to_string(self.template_name, {"form": form}, request=self.request)
        return JsonResponse({
            "success": False,
            "html": html,
            "message": "Por favor, corrige los errores en el formulario ❌"
        })
