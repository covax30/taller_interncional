from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from apy.models import Empresa, Cliente  # Importa explícitamente
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.urls import reverse_lazy
from apy.forms import EmpresaForm  # Importa explícitamente
from django.contrib.auth.mixins import AccessMixin
from apy.decorators import PermisoRequeridoMixin

## MIXIN DE PERMISOS (sin cambios)
class PermisoRequeridoMixin(AccessMixin):
    """
    Mixin para verificar los permisos del usuario actual.
    Requiere que se definan 'module_name' y 'permission_required'.
    """
    module_name = None      
    permission_required = None 

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission() 

        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)

        if self.module_name is None or self.permission_required is None:
            raise NotImplementedError(
                f'{self.__class__.__name__} debe definir module_name y permission_required.'
            )

        try:
            # Asegúrate de importar Module y Permission
            from apy.models import Module, Permission
            module = Module.objects.get(name=self.module_name)
            permission_obj = Permission.objects.filter(user=request.user, module=module).first()
            
            has_permission = False
            if permission_obj:
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
        return reverse_lazy('apy:empresa_lista')  # Cambié de cliente_lista a empresa_lista
    

## VISTAS BASADAS EN CLASES (CBVs)

class EmpresaListView(PermisoRequeridoMixin, ListView):
    model = Empresa
    template_name = 'empresa/listar_empresas.html'
    
    # --- Configuración de Permisos ---
    module_name = 'Empresa' 
    permission_required = 'view' 
    # --------------------------------
    
    def get_queryset(self):
        return Empresa.objects.filter(estado=True)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        nombre = {'nombre' : 'Empresa'}
        return JsonResponse(nombre)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Empresas'
        context['crear_url'] = reverse_lazy('apy:empresa_crear')
        context['entidad'] = 'Empresa'
        
        return context
    
class EmpresaCreateView(PermisoRequeridoMixin, CreateView):
    model = Empresa
    form_class = EmpresaForm
    template_name = 'empresa/crear_empresa.html'
    success_url = reverse_lazy('apy:empresa_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'Empresa'
    permission_required = 'add'
    
    def form_valid(self, form):
        form.instance.estado = True 
        messages.success(self.request, "Empresa agregada correctamente")
        response = super().form_valid(form)
        
        # CORRECCIÓN: Devuelve total de empresas, no clientes
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            total_empresas = Empresa.objects.count()
            return JsonResponse({
                'success': True, 
                'total_empresas': total_empresas,  
                'message': 'Empresa creada correctamente'  
            })
        
        return response
    
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Empresa'  # Corregido texto
        context['entidad'] = 'Empresa'
        context['listar_url'] = reverse_lazy('apy:empresa_lista')  # minúsculas
        return context
    
class EmpresaUpdateView(PermisoRequeridoMixin, UpdateView):
    model = Empresa
    form_class = EmpresaForm
    template_name = 'empresa/crear_empresa.html'
    success_url = reverse_lazy('apy:empresa_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'Empresa'
    permission_required = 'change'
    
    def form_valid(self, form):
        messages.success(self.request, "Empresa actualizada correctamente")
        return super().form_valid(form)
    
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Empresa'  # Corregido texto
        context['entidad'] = 'Empresa'
        context['listar_url'] = reverse_lazy('apy:empresa_lista')
        return context
    
class EmpresaDeleteView(PermisoRequeridoMixin, DeleteView): 
    model = Empresa
    template_name = 'empresa/eliminar_empresa.html'
    success_url = reverse_lazy('apy:empresa_lista')
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        
        # En lugar de eliminar, cambiar estado a inactivo
        self.object.estado = False
        self.object.save()
        
        messages.success(self.request, f"Empresa {self.object.nombre} desactivada")  # Corregido
        return HttpResponseRedirect(success_url)
   
    # --- Configuración de Permisos ---
    module_name = 'Empresa'
    permission_required = 'delete'
    
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Empresa'  # Corregido texto
        context['entidad'] = 'Empresa'
        context['listar_url'] = reverse_lazy('apy:empresa_lista')  # minúsculas
        return context
    
class EmpresaInactivosListView(View):
    def get(self, request):
        # CORRECCIÓN: Usa 'id' no 'id_empresa'
        inactivos = Empresa.objects.filter(estado=False).values("id", "nombre")
        return JsonResponse(list(inactivos), safe=False)
    
    
def activar_empresa(request):
    if request.method == "POST":
        # CORRECCIÓN: Usa 'id' no 'id_empresa'
        id = request.POST.get("id")
        empresa = Empresa.objects.filter(id=id).first()

        if empresa:
            empresa.estado = True
            empresa.save()
            return JsonResponse({"success": True, "message": "Empresa activada correctamente"})  # Cambiado

        return JsonResponse({"success": False, "message": "Empresa no encontrada"})  # Cambiado

    return JsonResponse({"success": False, "message": "Método inválido"})

# Vista para mostrar estadísticas de empresas
def estadisticas_empresas_view(request):
    # Contar total de empresas
    total_empresas = Empresa.objects.count()
    activas = Empresa.objects.filter(estado=True).count()
    inactivas = Empresa.objects.filter(estado=False).count()
    
    context = {
        'total_empresas': total_empresas,
        'activas': activas,
        'inactivas': inactivas,
    }
    return render(request, 'empresa/estadisticas.html', context)

# API para actualización dinámica del contador de empresas
def api_contador_empresas(request):
    total_empresas = Empresa.objects.count()
    return JsonResponse({'total_empresas': total_empresas})

class EmpresaCreateModalView(CreateView):
    model = Empresa
    form_class = EmpresaForm
    template_name = "empresa/modal_empresa.html"
    success_url = reverse_lazy("apy:empresa_lista")

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        try:
            self.object = form.save()
            # CORRECCIÓN: Usa self.object.id, no self.object.id_cliente
            return JsonResponse({
                "success": True,
                "id": self.object.id,  # Cambiado
                "text": str(self.object),
                "message": "Empresa registrada correctamente"
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
            "message": "Por favor, corrige los errores en el formulario"
        })