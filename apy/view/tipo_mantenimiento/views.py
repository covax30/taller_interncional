from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.urls import reverse_lazy
from apy.forms import *
from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin
# Importar modelos necesarios para el Mixin
from apy.models import TipoMantenimiento, Module, Permission 
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
        # Redirige a la lista de tipos de mantenimiento como fallback
        return reverse_lazy('apy:tipo_mantenimiento_lista') 

# --------------Vistas de Tipo de Mantenimiento---------------

# NOTA: La función 'def listar_tipo_mantenimiento(request)' se elimina

class TipoMantenimientoListView(PermisoRequeridoMixin, ListView):
    model = TipoMantenimiento
    template_name = 'tipo_mantenimiento/listar.html'
    
    # --- Configuración de Permisos ---
    module_name = 'TipoMantenimiento' 
    permission_required = 'view'
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Tipos de Mantenimiento'
        context['crear_url'] = reverse_lazy('apy:tipo_mantenimiento_crear')
        context['entidad'] = 'Tipo de Mantenimiento'
        return context

class TipoMantenimientoCreateView(PermisoRequeridoMixin, CreateView): # ORDEN CORREGIDO
    model = TipoMantenimiento
    form_class = TipoMantenimientoForm
    template_name = 'tipo_mantenimiento/crear.html'
    success_url = reverse_lazy('apy:tipo_mantenimiento_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'TipoMantenimiento'
    permission_required = 'add'
    
    def form_valid(self, form):
        messages.success(self.request, "tipo de mantnimiento creado correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Tipo de Mantenimiento'
        context['entidad'] = 'Tipo de Mantenimiento'
        context['listar_url'] = reverse_lazy('apy:tipo_mantenimiento_lista')
        return context

class TipoMantenimientoUpdateView(PermisoRequeridoMixin, UpdateView): 
    model = TipoMantenimiento
    form_class = TipoMantenimientoForm
    template_name = 'tipo_mantenimiento/crear.html'
    success_url = reverse_lazy('apy:tipo_mantenimiento_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'TipoMantenimiento'
    permission_required = 'change'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Tipo de Mantenimiento'
        context['entidad'] = 'Tipo de Mantenimiento'
        context['listar_url'] = reverse_lazy('apy:tipo_mantenimiento_lista')
        return context

class TipoMantenimientoDeleteView(PermisoRequeridoMixin, DeleteView):
    model = TipoMantenimiento
    template_name = 'tipo_mantenimiento/eliminar.html'
    success_url = reverse_lazy('apy:tipo_mantenimiento_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'TipoMantenimiento'
    permission_required = 'delete'
    
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

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            form = self.get_form()
            html = render_to_string(self.template_name, {"form": form}, request=request)
            return JsonResponse({"html": html})
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # Verificar si es una lista de mantenimientos múltiples
        if 'mantenimientos_multiples' in request.POST:
            return self.guardar_mantenimientos_multiples(request)
        else:
            # Comportamiento original para un solo mantenimiento
            return super().post(request, *args, **kwargs)

    def guardar_mantenimientos_multiples(self, request):
        try:
            mantenimientos_data = json.loads(request.POST['mantenimientos_multiples'])
            objetos_creados = []
            
            for mantenimiento in mantenimientos_data:
                # Crear instancia para cada mantenimiento
                detalle = DetalleTipoMantenimiento(
                    id_tipo_mantenimiento_id=mantenimiento['id_tipo_mantenimiento'],
                    cantidad=mantenimiento['cantidad'],
                    precio_unitario=mantenimiento['precio_unitario'],
                    descripcion=mantenimiento['descripcion']
                )
                detalle.full_clean()
                detalle.save()
                objetos_creados.append({
                    'id': detalle.id,
                    'text': str(detalle)
                })
            
            return JsonResponse({
                "success": True,
                "message": f"Se guardaron {len(objetos_creados)} mantenimientos correctamente ✅",
                "objetos_creados": objetos_creados,
                "total_mantenimientos": len(objetos_creados)
            })
            
        except Exception as e:
            return JsonResponse({
                "success": False,
                "message": f"Error al guardar los mantenimientos: {str(e)}"
            }, status=500)

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