from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from apy.forms import *
from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin
# Importar modelos necesarios para el Mixin y la vista
from apy.models import Vehiculo, Module, Permission 
from apy.decorators import PermisoRequeridoMixin

# PERMISO REQUERIDO MIXIN 
class PermisoRequeridoMixin(AccessMixin):
    """
    Mixin para verificar los permisos del usuario actual.
    Requiere que se definan 'module_name' y 'permission_required'.
    """
    module_name = None      
    permission_required = None 

    def dispatch(self, request, *args, **kwargs):
        # 1. Verificar Autenticación
        if not request.user.is_authenticated:
            return self.handle_no_permission() 

        # 2. Permitir Superusuario
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)

        # 3. Verificar Configuración
        if self.module_name is None or self.permission_required is None:
            raise NotImplementedError(
                f'{self.__class__.__name__} debe definir module_name y permission_required.'
            )

        # 4. Lógica de Permisos Personalizados
        try:
            # Asumiendo que Module y Permission son los modelos correctos
            module = Module.objects.get(name=self.module_name)
            permission_obj = Permission.objects.filter(user=request.user, module=module).first()
            
            has_permission = False
            if permission_obj:
                # Usa getattr para verificar el permiso (ej: permission_obj.view)
                has_permission = getattr(permission_obj, self.permission_required, False)
                
            if has_permission:
                return super().dispatch(request, *args, **kwargs)
            else:
                messages.warning(request, f"Acceso denegado. No tienes permiso de {self.permission_required.upper()} para el módulo '{self.module_name}'.")
                return redirect(self.get_permission_denied_url())
                
        except Module.DoesNotExist:
            messages.error(request, f"Error de configuración: Módulo '{self.module_name}' no encontrado.")
            return redirect(self.get_permission_denied_url())

    def get_permission_denied_url(self):
        # Redirige a la lista de vehículos como fallback
        return reverse_lazy('apy:vehiculo_lista') 

# --------------Vistas de Vehículos---------------

class VehiculoListView(PermisoRequeridoMixin, ListView):
    model = Vehiculo
    template_name = 'vehiculos/listar_vehiculos.html'

    # --- Configuración de Permisos ---
    module_name = 'Vehiculos' 
    permission_required = 'view'
    
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

class VehiculoCreateView(PermisoRequeridoMixin, CreateView): 
    model = Vehiculo
    form_class = VehiculoForm
    template_name = 'vehiculos/crear_vehiculos.html'
    success_url = reverse_lazy('apy:vehiculo_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'Vehiculos'
    permission_required = 'add'
    
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

class VehiculoUpdateView(PermisoRequeridoMixin, UpdateView): # ORDEN CORREGIDO
    model = Vehiculo
    form_class = VehiculoForm
    template_name = 'vehiculos/crear_vehiculos.html'
    success_url = reverse_lazy('apy:vehiculo_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'Vehiculos'
    permission_required = 'change'
    
    def form_valid(self, form):
        messages.success(self.request, "Vehiculo actualizado correctamente")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar de Vehiculos'
        context['entidad'] = 'Vehiculo' 
        context['listar_url'] = reverse_lazy('apy:vehiculo_lista')
        return context

class VehiculoDeleteView(PermisoRequeridoMixin, DeleteView): 
    model = Vehiculo
    template_name = 'vehiculos/eliminar_vehiculos.html'
    success_url = reverse_lazy('apy:vehiculo_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'Vehiculos'
    permission_required = 'delete'
    
    def form_valid(self, form):
        messages.success(self.request, "Vehiculo eliminado correctamente")
        return super().form_valid(form)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar de Vehiculos'
        context['entidad'] = 'Vehiculo'
        context['listar_url'] = reverse_lazy('apy:vehiculo_lista')
        return context
  
def estadisticas_view(request):
    # Contar total de vehiculos
    total_vehiculos = Vehiculo.objects.count()

    # Puedes agregar más estadísticas aquí
    context = {
        'total_vehiculos': total_vehiculos,
    }
    return render(request, 'estadisticas.html', context)

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