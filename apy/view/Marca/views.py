from django.shortcuts import render, redirect
from apy.models import *
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from apy.forms import *
from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin
from apy.decorators import PermisoRequeridoMixin
from apy.decorators import PermisoRequeridoMixin

# PERMISO REQUERIDO MIXIN - Definición Completa

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
        # Redirige a la lista de marcas como fallback
        return reverse_lazy('apy:marca_lista') 

# --------------Vistas de Marca---------------

# NOTA: La función 'def marca(request)' se elimina

class MarcaListView(PermisoRequeridoMixin, ListView): # ORDEN CORREGIDO
    model = Marca
    template_name ='Marca/listar_marca.html'
    
    # --- Configuración de Permisos ---
    module_name = 'Marca' 
    permission_required = 'view'
    
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
    
class MarcaCreateView(PermisoRequeridoMixin, CreateView): # ORDEN CORREGIDO
    model = Marca
    form_class = MarcaForm
    template_name = 'Marca/crear_marca.html'
    success_url = reverse_lazy('apy:marca_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'Marca'
    permission_required = 'add'
    
    # --- Configuración de Permisos ---
    module_name = 'Marca'
    permission_required = 'add'
    
    def form_valid(self, form):
        messages.success(self.request, "Marca creada correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context ['titulo'] = 'Crear Marca'
        context ['entidad'] = 'Marca'
        context ['listar_url'] = reverse_lazy('apy:marca_lista')
        return context
    
class MarcaUpdateView(PermisoRequeridoMixin, UpdateView): # ORDEN CORREGIDO
    model = Marca
    form_class = MarcaForm
    template_name = 'Marca/crear_marca.html'
    success_url = reverse_lazy('apy:marca_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'Marca'
    permission_required = 'change'
    
    def form_valid(self, form):
        messages.success(self.request, "Marca actualizada correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar marca'
        context['entidad'] = 'Marcas' # Se eliminó el espacio inicial
        context['listar_url'] = reverse_lazy('apy:marca_lista')
        return context

class MarcaDeleteView(PermisoRequeridoMixin, DeleteView): # ORDEN CORREGIDO
    model = Marca
    template_name = 'Marca/eliminar_marca.html'
    success_url = reverse_lazy('apy:marca_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'Marca'
    permission_required = 'delete'
    
    def form_valid(self, form):
        messages.success(self.request, "Marca eliminada correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Marca'
        context['entidad'] = 'Marcas' # Se eliminó el espacio inicial
        context['listar_url'] = reverse_lazy('apy:marca_lista')
        return context

class MarcaCreateModalView(CreateView):
    model = Marca
    form_class = MarcaForm
    template_name = "Marca/modal_marca.html"
    success_url = reverse_lazy("apy:marca_lista")

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
                "message": "Marca registrada correctamente ✅"
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