from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.urls import reverse_lazy
from apy.forms import *
from django.contrib import messages


# Create your views here.
# --------------Vistas erick---------------

def listar_tipo_mantenimiento(request):
    data = {
        'tipo_mantenimiento': 'tipo_mantenimiento',
        'titulo': 'Lista de Tipos de Mantenimiento',
        'tipos_mantenimiento': TipoMantenimiento.objects.all()
    }
    return render(request, 'tipo_mantenimiento/listar.html', data)

class TipoMantenimientoListView(ListView):
    model = TipoMantenimiento
    template_name = 'tipo_mantenimiento/listar.html'
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Tipos de Mantenimiento'
        context['crear_url'] = reverse_lazy('apy:tipo_mantenimiento_crear')
        context['entidad'] = 'Tipo de Mantenimiento'
        return context

class TipoMantenimientoCreateView(CreateView):
    model = TipoMantenimiento
    form_class = TipoMantenimientoForm
    template_name = 'tipo_mantenimiento/crear.html'
    success_url = reverse_lazy('apy:tipo_mantenimiento_lista')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Tipo de Mantenimiento'
        context['entidad'] = 'Tipo de Mantenimiento'
        context['listar_url'] = reverse_lazy('apy:tipo_mantenimiento_lista')
        return context

class TipoMantenimientoUpdateView(UpdateView):
    model = TipoMantenimiento
    form_class = TipoMantenimientoForm
    template_name = 'tipo_mantenimiento/crear.html'
    success_url = reverse_lazy('apy:tipo_mantenimiento_lista')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Tipo de Mantenimiento'
        context['entidad'] = 'Tipo de Mantenimiento'
        context['listar_url'] = reverse_lazy('apy:tipo_mantenimiento_lista')
        return context

class TipoMantenimientoDeleteView(DeleteView):
    model = TipoMantenimiento
    template_name = 'tipo_mantenimiento/eliminar.html'
    success_url = reverse_lazy('apy:tipo_mantenimiento_lista')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar tipo de mantenimiento'
        context['entidad'] = 'tipo de mantenimiento'
        context['listar_url'] = reverse_lazy('apy:tipo_mantenimiento_lista')
        return context

class TipoMantenimientoCreateModalView(CreateView):
    model = TipoMantenimiento
    form_class = TipoMantenimientoForm
    template_name = "tipo_mantenimiento/modal_tipo_mantenimiento.html"
    success_url = reverse_lazy("apy:tipo_mantenimiento_lista")

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
                "message": "Tipo de Mantenimiento registrado correctamente ✅"
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

class DetalleTipoMantenimientoCreateModalView(CreateView):
    model = DetalleTipoMantenimiento
    form_class = DetalleTipo_MantenimientoForm
    template_name = "tipo_mantenimiento/modal_detalletipo_mantenimiento.html"
    success_url = reverse_lazy("apy:detalletipo_mantenimiento_lista ")

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            form = self.get_form()
            html = render_to_string(self.template_name, {"form": form}, request=request)
            return JsonResponse({"html": html})
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        try:
            self.object = form.save()
            return JsonResponse({
                "success": True,
                "id": self.object.id,
                "text": str(self.object),
                "message": "Detalle de Tipo Mantenimiento registrado correctamente ✅"
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