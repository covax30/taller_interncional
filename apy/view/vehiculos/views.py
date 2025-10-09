from django.shortcuts import render
from apy.models import *
from apy.view.vehiculos.views import *
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.urls import reverse_lazy
from apy.forms import *


def lista_vehiculos(request):
    data = {
        'vehiculos': 'vehiculos',
        'titulo': 'Lista de Vehiculos',
        'vehiculos': Vehiculo.objects.all()
    }
    return render(request, 'vehiculos/listar_vehiculos.html', data)

# vistas basadas en clases
class VehiculoListView(ListView):
    model = Vehiculo
    template_name = 'vehiculos/listar_vehiculos.html'

        # @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
       return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        nombre = {'nombre' : 'Vehiculo'}
        return JsonResponse(nombre)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Vehiculos'
        context['crear_url'] = reverse_lazy('apy:vehiculo_crear')
        context['entidad'] = 'Vehiculo'  
        return context

class VehiculoCreateView(CreateView):
    model = Vehiculo
    form_class = VehiculoForm
    template_name = 'vehiculos/crear_vehiculos.html'
    success_url = reverse_lazy('apy:vehiculo_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "Vehiculo creado correctamente")
        response = super().form_valid(form)
        
        # Si la request es AJAX, devolver JSON con el nuevo contador
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            total_vehiculos = Vehiculo.objects.count()
            return JsonResponse({
                'success': True, 
                'total_vehiculos': total_vehiculos,
                'message': 'Vehiculo creado correctamente'
            })
        
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear de Vehiculos'
        context['entidad'] = 'Vehiculo'  
        context['listar_url'] = reverse_lazy('apy:vehiculo_lista')
        return context

class VehiculoUpdateView(UpdateView):
    model = Vehiculo
    form_class = VehiculoForm
    template_name = 'vehiculos/crear_vehiculos.html'
    success_url = reverse_lazy('apy:vehiculo_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "Vehiculo actualizado correctamente")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar de Vehiculos'
        context['entidad'] = 'Vehiculo'  
        context['listar_url'] = reverse_lazy('apy:vehiculo_lista')
        return context

class VehiculoDeleteView(DeleteView):
    model = Vehiculo
    template_name = 'vehiculos/eliminar_vehiculos.html'
    success_url = reverse_lazy('apy:vehiculo_lista')
    
    def form_valid(self, form):
        messages.success(self.request, "Vehiculo eliminado correctamente")
        return super().form_valid(form)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar de Vehiculos'
        context['entidad'] = 'Vehiculo'  
        context['listar_url'] = reverse_lazy('apy:vehiculo_lista')
        return context
    
# Vista para mostrar estadísticas
def estadisticas_view(request):
    # Contar total de vehiculos
    total_vehiculos = Vehiculo.objects.count()

    # Puedes agregar más estadísticas aquí
    context = {
        'total_vehiculos': total_vehiculos,
    }
    return render(request, 'estadisticas.html', context)

# API para actualización dinámica del contador de vehiculos
def api_contador_vehiculos(request):
    total_vehiculos = Vehiculo.objects.count()
    return JsonResponse({'total_vehiculos': total_vehiculos})

class VehiculoCreateModalView(CreateView):
    model = Vehiculo
    form_class = VehiculoForm
    template_name = "vehiculos/modal_vehiculo.html"
    success_url = reverse_lazy("apy:vehiculo_lista")

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Override post para manejar peticiones AJAX"""
        # Verificar si es petición AJAX
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        if not is_ajax:
            return JsonResponse({
                "success": False,
                "message": "Esta vista solo acepta peticiones AJAX"
            }, status=400)
        
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        """Manejar formulario válido"""
        try:
            self.object = form.save()

            # ✅ construir texto para el select (usando __str__)
            vehiculo_text = str(self.object)
            
            return JsonResponse({
                "success": True,
                "id": self.object.id_vehiculo,
                "text": vehiculo_text,
                "message": "Vehículo registrado correctamente ✅"
            })
        except Exception as e:
            # Log del error para debugging
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error al guardar vehículo: {str(e)}", exc_info=True)
            
            return JsonResponse({
                "success": False,
                "message": f"Error al guardar: {str(e)}"
            }, status=500)
    
    def form_invalid(self, form):
        """Manejar formulario inválido"""
        # Renderizar el template con los errores
        html = render_to_string(
            self.template_name, 
            {"form": form}, 
            request=self.request
        )
        
        # También puedes enviar los errores en formato JSON
        errors_dict = {}
        for field, errors in form.errors.items():
            errors_dict[field] = [{"message": str(error)} for error in errors]
        
        return JsonResponse({
            "success": False,
            "html": html,
            "errors": errors_dict,
            "message": "Por favor, corrige los errores en el formulario ❌"
        }, status=400)