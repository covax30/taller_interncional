from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.urls import reverse_lazy
from apy.forms import *

# Create your views here.
# --------------Vistas erick---------------

class RepuestoListView(ListView):
    model = Repuesto
    template_name = 'repuestos/listar.html'
    
    @method_decorator(csrf_exempt)
  
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Repuestos'
        context['crear_url'] = reverse_lazy('apy:repuesto_crear')
        context['entidad'] = 'Repuesto'
        return context
    
class RepuestoCreateView(CreateView):
    model = Repuesto
    form_class = RepuestoForm
    template_name = 'repuestos/crear.html'
    success_url = reverse_lazy('apy:repuesto_lista')
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Repuesto'
        context['entidad'] = 'Repuesto'
        context['listar_url'] = reverse_lazy('apy:repuesto_lista')
        return context
    
    def form_valid(self, form):
        self.object = form.save()

        #  forma de detectar 
        if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({
                "success": True,
                "id": self.object.id,
                "nombre": str(self.object.nombre)  # usa __str__ del modelo
            })

        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({
                "success": False,
                "errors": form.errors
            }, status=400)
        return super().form_invalid(form)

    
class RepuestoUpdateView(UpdateView):
    model = Repuesto
    form_class = RepuestoForm
    template_name = 'repuestos/crear.html'
    success_url = reverse_lazy('apy:repuesto_lista')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Repuesto'
        context['entidad'] = 'Repuesto'
        context['listar_url'] = reverse_lazy('apy:repuesto_lista')
        return context
    
class RepuestoDeleteView(DeleteView):
    model = Repuesto
    template_name = 'repuestos/eliminar.html'
    success_url = reverse_lazy('apy:repuesto_lista')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Repuesto'
        context['entidad'] = 'Repuesto'
        context['listar_url'] = reverse_lazy('apy:repuesto_lista')
        return context

class RepuestoCreateModalView(CreateView):
    model = Repuesto
    form_class = RepuestoForm
    template_name = "repuestos/modal_form.html"  # plantilla parcial
    success_url = reverse_lazy("apy:repuesto_lista")

    def form_valid(self, form):
        self.object = form.save()
        # Retornamos JSON para actualizar el select sin refrescar la página
        return JsonResponse({
            "success": True,
            "id": self.object.id,
            "text": str(self.object)
        })

    def form_invalid(self, form):
        return JsonResponse({
            "success": False,
            "html": render(self.request, self.template_name, {"form": form}).content.decode("utf-8")
        })
        
    def form_valid(self, form):
        self.object = form.save()
        return JsonResponse({
            "success": True,
            "id": self.object.id,
            "text": str(self.object),
            "message": "Repuesto registrado correctamente ✅"
        })
    
    def form_invalid(self, form):
        return JsonResponse({
            "success": False,
            "html": render(self.request, self.template_name, {"form": form}).content.decode("utf-8"),
            "message": "Error al registrar el repuesto ❌"
        })

