from django.shortcuts import render
from apy.models import *
from apy.view.Empleado.views import *
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from apy.forms import *
from django.contrib import messages

# Create your views here.
# --------------Vistas Karol---------------

def empleado(request):
    data = {
        'Empleado':'Empleado',
        'titulo':'Lista de Empleados',
        'empleados': Empleado.objects.all()
    }
    return render(request, 'Empleado/cont_Empleado.html', data)

class EmpleadoListView(ListView):
    model = Empleado
    template_name ='Empleado/listar_empleado.html'
    
    # @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
       return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        nombre = {'nombre' : 'Yury'}
        return JsonResponse(nombre)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Empleados'
        context['crear_url'] = reverse_lazy('apy:empleado_crear')
        context['entidad'] = 'Empleado'  
        return context
    
class EmpleadoCreateView(CreateView):
    model = Empleado
    form_class = EmpleadoForm
    template_name = 'Empleado/crear_empleado.html'
    success_url = reverse_lazy('apy:empleado_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "Empleado creado correctamente")
        return super().form_valid(form)
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context ['titulo'] = 'Crear Empleado'
        context ['entidad'] = 'Empleados'
        context ['listar_url'] = reverse_lazy('apy:empleado_lista')
        
        return context
    
class EmpleadoUpdateView(UpdateView):
    model = Empleado
    form_class = EmpleadoForm
    template_name = 'Empleado/crear_empleado.html'
    success_url = reverse_lazy('apy:empleado_lista')
    def form_valid(self, form):
        messages.success(self.request, "Empleado actualizado correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar empleado'
        context['entidad'] = 'Empleados'
        context['listar_url'] = reverse_lazy('apy:empleado_lista')
        return context

class EmpleadoDeleteView(DeleteView):
    model = Empleado
    template_name = 'Empleado/eliminar_empleado.html'
    success_url = reverse_lazy('apy:empleado_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "Empleado eliminado correctamente")
        return super().form_valid(form)
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Empleado'
        context['entidad'] = 'Empleados'
        context['listar_url'] = reverse_lazy('apy:empleado_lista')
        return context
    
class EmpleadoCreateModalView(CreateView):
    model = Empleado
    form_class = EmpleadoForm
    template_name = "Empleado/modal_empleado.html"
    success_url = reverse_lazy("apy:empleado_lista")

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
                "message": "Empleado registrado correctamente ✅"
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
