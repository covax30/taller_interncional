from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from apy.forms import *
from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin
# Importar modelos necesarios para el Mixin y la vista
from apy.models import Herramienta, Module, Permission 
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
        # Redirige a la lista de herramientas como fallback
        return reverse_lazy('apy:herramienta_lista') 

# --------------Vistas de Herramientas---------------

class HerramientaListView(PermisoRequeridoMixin, ListView): 
    model = Herramienta
    template_name = 'herramienta/listar.html'
    
    # --- Configuración de Permisos ---
    module_name = 'Herramientas' 
    permission_required = 'view'
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        # El dispatch del Mixin se ejecuta primero para la verificación de permisos
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Herramientas'
        context['crear_url'] = reverse_lazy('apy:herramienta_crear')
        context['entidad'] = 'Herramienta'
        return context

class HerramientaCreateView(PermisoRequeridoMixin, CreateView): 
    model = Herramienta
    form_class = HerramientaForm
    template_name = 'herramienta/crear.html'
    success_url = reverse_lazy('apy:herramienta_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'Herramientas'
    permission_required = 'add'
    
    def form_valid(self, form):
        messages.success(self.request, "herramienta creada correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Herramienta'
        context['entidad'] = 'Herramienta'
        context['listar_url'] = reverse_lazy('apy:herramienta_lista')
        return context

class HerramientaUpdateView(PermisoRequeridoMixin, UpdateView): # ORDEN CORREGIDO
    model = Herramienta
    form_class = HerramientaForm
    template_name = 'herramienta/crear.html'
    success_url = reverse_lazy('apy:herramienta_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'Herramientas'
    permission_required = 'change'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Herramienta'
        context['entidad'] = 'Herramienta'
        context['listar_url'] = reverse_lazy('apy:herramienta_lista')
        return context

class HerramientaDeleteView(PermisoRequeridoMixin, DeleteView): # ORDEN CORREGIDO
    model = Herramienta
    template_name = 'herramienta/eliminar.html'
    success_url = reverse_lazy('apy:herramienta_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'Herramientas'
    permission_required = 'delete'
    
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