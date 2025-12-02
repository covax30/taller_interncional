from django.shortcuts import render, redirect
from apy.models import * # Necesitas importar los modelos, incluyendo 'Insumos', 'Module', y 'Permission'
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from apy.forms import *
from django.contrib import messages
# Se elimina la importación local de AccessMixin

# Importar las herramientas de permisos centralizadas
from apy.decorators import PermisoRequeridoMixin, permiso_requerido_fbv 

# --------------Vistas de Insumos (CBVs)---------------

class InsumoListView(PermisoRequeridoMixin, ListView): 
    model = Insumos
    template_name = 'insumos/listar.html'
    
    # --- Configuración de Permisos ---
    module_name = 'Insumos' 
    permission_required = 'view'
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Insumos'
        context['crear_url'] = reverse_lazy('apy:insumo_crear')
        context['entidad'] = 'Insumo'
        return context
    
class InsumoCreateView(PermisoRequeridoMixin, CreateView): 
    model = Insumos
    form_class = InsumoForm
    template_name = 'insumos/crear.html'
    success_url = reverse_lazy('apy:insumo_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'Insumos' 
    permission_required = 'add'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Insumo'
        context['entidad'] = 'Insumo'
        context['listar_url'] = reverse_lazy('apy:insumo_lista')
        return context
    
class InsumoUpdateView(PermisoRequeridoMixin, UpdateView):
    model = Insumos
    form_class = InsumoForm
    template_name = 'insumos/crear.html'
    success_url = reverse_lazy('apy:insumo_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'Insumos' 
    permission_required = 'change'
    
    def form_valid(self, form):
        messages.success(self.request, "Insumo actualizado correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Insumo'
        context['entidad'] = 'Insumo'
        context['listar_url'] = reverse_lazy('apy:insumo_lista')
        return context
    
class InsumoDeleteView(PermisoRequeridoMixin, DeleteView): 
    model = Insumos
    template_name = 'insumos/eliminar.html'
    success_url = reverse_lazy('apy:insumo_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'Insumos' 
    permission_required = 'delete'
    
    def form_valid(self, form):
        messages.success(self.request, "Insumo eliminado correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Insumo'
        context['entidad'] = 'Insumo'
        context['listar_url'] = reverse_lazy('apy:insumo_lista')
        return context
    
# --------------Vistas de Insumos (VBFs estandarizadas)---------------

# Proteger la vista de estadísticas
@permiso_requerido_fbv(module_name='Insumos', permission_required='view') 
def estadisticas_view(request):
    # Contar total de insumos
    total_insumos = Insumos.objects.count()

    # Puedes agregar más estadísticas aquí
    context = {
        'total_insumos': total_insumos,
    }
    return render(request, 'estadisticas.html', context)

# API para actualización dinámica del contador de insumos (Proteger la API)
@permiso_requerido_fbv(module_name='Insumos', permission_required='view', api=True)
def api_contador_insumos(request):
    total_insumos = Insumos.objects.count()
    return JsonResponse({'total_insumos': total_insumos})

class InsumoCreateModalView(CreateView):
    model = Insumos
    form_class = InsumoForm
    template_name = "insumos/modal_insumos.html"
    success_url = reverse_lazy("apy:insumo_lista")

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
                "message": "Insumo registrado correctamente ✅"
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
        
class DetalleInsumoCreateModalView(CreateView):
    model = Insumos
    form_class = InsumoForm
    template_name = "insumos/modal_detalleinsumos.html"
    success_url = reverse_lazy("apy:detalleinsumo_lista")

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
                "message": "Insumo registrado correctamente ✅"
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