from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
# Se asume que apy.models, apy.view.clientes.views, y apy.forms contienen las clases necesarias
from apy.models import *
# from apy.view.clientes.views import * # Si este archivo contiene estas vistas, esta importación puede ser redundante o generar un conflicto circular. Se recomienda revisar su necesidad.
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.urls import reverse_lazy
from django.contrib.auth.mixins import AccessMixin # Solo necesaria si defines mixins locales
# Importaciones de modelos, formularios y Mixin corregido
from apy.models import *
from apy.forms import *
from apy.decorators import PermisoRequeridoMixin, permiso_requerido_fbv # <-- Asumo que 'permiso_requerido_fbv' es tu decorador de función 

# --- VISTAS BASADAS EN CLASES (CBVs) - PROTEGIDAS ---

class ClienteListView(PermisoRequeridoMixin, ListView):
    model = Cliente
    template_name = 'clientes/listar_clientes.html'
    
    # --- Configuración de Permisos ---
    module_name = 'Clientes' 
    permission_required = 'view' 
    # --------------------------------
    
    def get_queryset(self):
        return Cliente.objects.filter(estado=True)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        nombre = {'nombre' : 'Cliente'}
        return JsonResponse(nombre)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Clientes'
        context['crear_url'] = reverse_lazy('apy:cliente_crear')
        context['entidad'] = 'Cliente'
        
        return context
    
class ClienteCreateView(PermisoRequeridoMixin, CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'clientes/crear_clientes.html'
    success_url = reverse_lazy('apy:cliente_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'Clientes'
    permission_required = 'add'
    
    def form_valid(self, form):
        form.instance.estado = True 
        messages.success(self.request, "Cliente creado correctamente")
        response = super().form_valid(form)
        messages.success(self.request, "Cliente creado correctamente")
        
        # Si la request es AJAX, devolver JSON con el nuevo contador
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            total_clientes = Cliente.objects.count()
            return JsonResponse({
                'success': True, 
                'total_clientes': total_clientes,
                'message': 'Cliente creado correctamente'
            })
        
        return response
    
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear de Clientes'
        context['entidad'] = 'Cliente'
        context['listar_url'] = reverse_lazy('apy:cliente_lista')
        return context
    
class ClienteUpdateView(PermisoRequeridoMixin, UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'clientes/crear_clientes.html'
    success_url = reverse_lazy('apy:cliente_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'Clientes'
    permission_required = 'change'
    
    def form_valid(self, form):
        messages.success(self.request, "Cliente actualizado correctamente")
        return super().form_valid(form)
    
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar de Clientes'
        context['entidad'] = 'Cliente'
        context['listar_url'] = reverse_lazy('apy:cliente_lista')
        return context
    
class ClienteDeleteView(PermisoRequeridoMixin, DeleteView): 
    model = Cliente
    template_name = 'clientes/eliminar_clientes.html'
    success_url = reverse_lazy('apy:cliente_lista')
    
    def post(self, request, *args, **kwargs):
        
        self.object = self.get_object()
        success_url = self.get_success_url()
        
        # En lugar de eliminar, cambiar estado a inactivo
        self.object.estado = False
        self.object.save()
        
        messages.success(self.request, f"Cliente {self.object.nombre} desactivado ")
        return HttpResponseRedirect(success_url)
   
    
    # --- Configuración de Permisos ---
    module_name = 'Clientes'
    permission_required = 'delete'
    
    def form_valid(self, form):
        messages.success(self.request, "Cliente eliminado correctamente")
        return super().form_valid(form)
    
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar de Clientes'
        context['entidad'] = 'Cliente'
        context['listar_url'] = reverse_lazy('apy:cliente_lista')
        return context
    
class ClienteInactivosListView(View):
    def get(self, request):
        inactivos = Cliente.objects.filter(estado=False).values("id_cliente", "nombre")
        return JsonResponse(list(inactivos), safe=False)
    
    
def activar_cliente(request):
    if request.method == "POST":
        id_cliente = request.POST.get("id_cliente")
        cliente = Cliente.objects.filter(id_cliente=id_cliente).first()

        if cliente:
            cliente.estado = True
            cliente.save()
            return JsonResponse({"success": True, "message": "Cliente activado correctamente"})

        return JsonResponse({"success": False, "message": "Cliente no encontrado"})

    return JsonResponse({"success": False, "message": "Método inválido"})
# Vista para mostrar estadísticas
def estadisticas_view(request):
    """Muestra estadísticas, requiere permiso 'view' de Clientes."""
    # Contar total de clientes
    total_clientes = Cliente.objects.count()
    
    context = {
        'total_clientes': total_clientes,
        'titulo': 'Estadísticas de Clientes'
    }
    return render(request, 'clientes/estadisticas.html', context)

# API para actualización dinámica del contador de clientes (No protegida con 403, solo autenticación si es necesario)
def api_contador_clientes(request):
    """Retorna el total de clientes para actualización AJAX."""
    total_clientes = Cliente.objects.count()
    return JsonResponse({'total_clientes': total_clientes})

class ClienteCreateModalView(CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = "clientes/modal_cliente.html"
    success_url = reverse_lazy("apy:cliente_lista")

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        try:
            self.object = form.save()
            return JsonResponse({
                "success": True,
                "id": self.object.id_cliente,
                "text": str(self.object),
                "message": "Cliente registrado correctamente ✅"
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