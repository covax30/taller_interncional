from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from apy.forms import *
from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin
from django.contrib.auth.decorators import login_required
# Importar modelos necesarios para el Mixin y la vista
from apy.models import Gastos, Module, Permission 
from django.http import HttpResponse # Importado para la función check_custom_permission
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
        # Redirige a la lista de gastos como fallback
        return reverse_lazy('apy:gasto_lista') 


# Lógica de permisos para Vistas Basadas en Función (duplicada para fines de archivo)
def check_custom_permission(user, module_name, permission_required, redirect_url_name='apy:gasto_lista'):
    if user.is_superuser:
        return None 
    try:
        module = Module.objects.get(name=module_name)
        permission_obj = Permission.objects.filter(user=user, module=module).first()
        has_permission = False
        if permission_obj:
            has_permission = getattr(permission_obj, permission_required, False)
        if has_permission:
            return None 
        else:
            messages.warning(user, f"Acceso denegado. No tienes permiso de {permission_required.upper()} para el módulo '{module_name}'.")
            return redirect(reverse_lazy(redirect_url_name)) 
    except Module.DoesNotExist:
        messages.error(user, f"Error de configuración: Módulo '{module_name}' no encontrado.")
        return redirect(reverse_lazy(redirect_url_name))

# URL de redirección en caso de denegación de permisos para VBFs
REDIRECT_ON_DENIAL = 'apy:gasto_lista' 


# --------------Vistas de Gastos (CBVs)---------------

# NOTA: La función 'def gasto(request)' se elimina

class GastosListView(PermisoRequeridoMixin, ListView):
    model = Gastos
    template_name ='Gastos/listar_gasto.html' 
    
    # --- Configuración de Permisos ---
    module_name = 'Gastos' 
    permission_required = 'view'
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        nombre = {'nombre' : 'Yury'}
        return JsonResponse(nombre)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Gastos'
        context['crear_url'] = reverse_lazy('apy:gasto_crear')
        context['entidad'] = 'Gastos'
        return context
    
class GastosCreateView(PermisoRequeridoMixin, CreateView):
    form_class = GastosForm
    template_name = 'Gastos/crear_gasto.html'
    success_url = reverse_lazy('apy:gasto_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'Gastos'
    permission_required = 'add'
    
    def form_valid(self, form):
        messages.success(self.request, "Gasto  creado correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context ['titulo'] = 'Crear Gasto'
        context ['entidad'] = 'Gastos'
        context ['listar_url'] = reverse_lazy('apy:gasto_lista')
        return context
    
class GastosUpdateView(PermisoRequeridoMixin, UpdateView):
    model = Gastos
    form_class = GastosForm
    template_name = 'Gastos/crear_gasto.html'
    success_url = reverse_lazy('apy:gasto_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'Gastos'
    permission_required = 'change'
    
    def form_valid(self, form):
        messages.success(self.request, "Gasto editado correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Gasto'
        context['entidad'] = 'Gastos'
        context['listar_url'] = reverse_lazy('apy:gasto_lista')
        return context

class GastosDeleteView(PermisoRequeridoMixin, DeleteView):
    model = Gastos
    template_name = 'Gastos/eliminar_gasto.html'
    success_url = reverse_lazy('apy:gasto_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'Gastos'
    permission_required = 'delete'
    
    def form_valid(self, form):
        messages.success(self.request, "Gasto eliminado correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Gastos'
        context['entidad'] = 'Gastos'
        context['listar_url'] = reverse_lazy('apy:gasto_lista')
        return context
    
    
# --------------Vistas de Gastos (VBFs con Permisos)---------------

@login_required(login_url='/login/')
def estadisticas_view(request):
    # --- 1. VERIFICACIÓN DE PERMISOS PERSONALIZADOS ---
    permission_denied_response = check_custom_permission(
        request.user, 
        module_name='Gastos', 
        permission_required='view', # Se asume 'view' para estadísticas
        redirect_url_name=REDIRECT_ON_DENIAL
    )
    if permission_denied_response:
        return permission_denied_response
    # --------------------------------------------------
    
    # Contar total de gastos
    total_gastos = Gastos.objects.count()

    # Puedes agregar más estadísticas aquí
    context = {
        'total_gastos': total_gastos,
    }
    return render(request, 'estadisticas.html', context)

@login_required(login_url='/login/')
def api_contador_gastos(request):
    # --- 1. VERIFICACIÓN DE PERMISOS PERSONALIZADOS ---
    # Nota: Es común permitir acceso a APIs de conteo si el usuario tiene permiso de 'view'
    permission_denied_response = check_custom_permission(
        request.user, 
        module_name='Gastos', 
        permission_required='view', 
        redirect_url_name=REDIRECT_ON_DENIAL
    )
    # Para APIs, generalmente devolvemos un error 403 o un JsonResponse con error.
    # Aquí, por simplicidad, devolveremos un error si la redirección ocurre.
    if permission_denied_response:
         return JsonResponse({'error': 'Permiso denegado'}, status=403)
    # --------------------------------------------------
    
    total_gastos = Gastos.objects.count()
    return JsonResponse({'total_gastos': total_gastos})