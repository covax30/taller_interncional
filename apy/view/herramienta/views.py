from django.shortcuts import render
from apy.models import *
from apy.view.Contenidos.views import *
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from apy.forms import *

# Create your views here.
# --------------Vistas erick---------------

class HerramientaListView(ListView):
    model = Herramienta
    template_name = 'herramienta/listar.html'
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Herramientas'
        context['crear_url'] = reverse_lazy('apy:herramienta_crear')
        context['entidad'] = 'Herramienta'
        return context

class HerramientaCreateView(CreateView):
    model = Herramienta
    form_class = HerramientaForm
    template_name = 'herramienta/crear.html'
    success_url = reverse_lazy('apy:herramienta_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "herramienta creada correctamente")
        return super().form_valid(form)  
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Herramienta'
        context['entidad'] = 'Herramienta'
        context['listar_url'] = reverse_lazy('apy:herramienta_lista')
        return context

class HerramientaUpdateView(UpdateView):
    model = Herramienta
    form_class = HerramientaForm
    template_name = 'herramienta/crear.html'
    success_url = reverse_lazy('apy:herramienta_lista')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Herramienta'
        context['entidad'] = 'Herramienta'
        context['listar_url'] = reverse_lazy('apy:herramienta_lista')
        return context

class HerramientaDeleteView(DeleteView):
    model = Herramienta
    template_name = 'herramienta/eliminar.html'
    success_url = reverse_lazy('apy:herramienta_lista')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Herramienta'
        context['entidad'] = 'Herramienta'
        context['listar_url'] = reverse_lazy('apy:herramienta_lista')
        return context  
    
class HerramientaCreateModalView(CreateView):
    model = Herramienta
    form_class = HerramientaForm
    template_name = "herramienta/modal_herramienta.html"
    success_url = reverse_lazy("apy:herramienta_lista")

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
                "message": "Herramienta registrada correctamente ✅"
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