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
from apy.decorators import PermisoRequeridoMixin, permiso_requerido_fbv


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
    

class EmpresaInactivasListView(PermisoRequeridoMixin, ListView):
    model = Empresa
    template_name = 'empresa/empresa_inactivas.html'
    
    # --- Configuración de Permisos ---
    module_name = 'Empresa' 
    permission_required = 'view' 
    # --------------------------------
    
    def get_queryset(self):
        return Empresa.objects.filter(estado=False)

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
        
        form.instance.estado = True 
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
    
    # --- Configuración de Permisos ---
    module_name = 'Empresa'
    permission_required = 'delete'
    
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
        context['titulo'] = 'Eliminar Empresa'  
        context['entidad'] = 'Empresa'
        context['listar_url'] = reverse_lazy('apy:empresa_lista')  
        return context
    
 
class   EmpresaInactivaDeleteView(PermisoRequeridoMixin, DeleteView): 
    model = Empresa
    template_name = 'empresa/activar_empresa.html'
    success_url = reverse_lazy('apy:empresa_lista')
    
    def post(self, request, *args, **kwargs):
        
        self.object = self.get_object()
        success_url = self.get_success_url()
        
        self.object.estado = True
        self.object.save()
        
        messages.success(self.request, f"empresa {self.object.nombre} activada correctamente")
        return HttpResponseRedirect(success_url)
    

# Vista para mostrar estadísticas de empresas
@permiso_requerido_fbv(module_name='Estadísticas Generales', permission_required='view')
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

class EmpresaCreateModalView(PermisoRequeridoMixin, CreateView):
    model = Empresa
    form_class = EmpresaForm
    template_name = "empresa/modal_empresa.html"
    success_url = reverse_lazy("apy:empresa_lista")
    
    module_name = 'Empresa'
    permission_required = 'add'

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