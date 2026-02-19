from django.shortcuts import render, redirect
from apy.models import * # Importa Proveedores, Module, Permission
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from apy.forms import *
from django.contrib import messages
# Se elimina la importación local de AccessMixin
# Se mantiene la importación del Mixin centralizado (aunque estaba duplicada, ahora solo se usa la importada)
from apy.decorators import PermisoRequeridoMixin 

# --------------Vistas Proveedor---------------
class ProveedorListView(PermisoRequeridoMixin, ListView): 
    model = Proveedores
    template_name ='Proveedores/listar_proveedores.html'
    
    # --- Configuración de Permisos ---
    module_name = 'Proveedores' 
    permission_required = 'view' 
    # --------------------------------
    def get_queryset(self):
        return Proveedores.objects.filter(estado=True)
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        nombre = {'nombre' : 'Proveedor'}
        return JsonResponse(nombre)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Proveedores'
        context['crear_url'] = reverse_lazy('apy:proveedor_crear')
        context['entidad'] = 'Proveedor'
        return context
    
    #-- Vista para Proveedores Inactivos --
class ProveedorInactivaListView(PermisoRequeridoMixin, ListView):
    model = Proveedores
    template_name = 'Proveedores/proveedores_inactivos.html'
    
    # --- Configuración de Permisos ---
    module_name = 'Proveedores' 
    permission_required = 'view'
    
    def get_queryset(self):
        return Proveedores.objects.filter(estado=False)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Proveedores Inactivos'
        context['listar_url'] = reverse_lazy('apy:proveedor_lista')
        return context
    
class ProveedorCreateView(PermisoRequeridoMixin, CreateView): 
    model = Proveedores
    form_class = ProveedorForm
    template_name = 'Proveedores/crear_proveedor.html'
    success_url = reverse_lazy('apy:proveedor_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'Proveedores'
    permission_required = 'add'
        
    
    def form_valid(self, form):
        form.instance.estado = True 
        messages.success(self.request, "Proveedor creado correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context ['titulo'] = 'Crear Proveedor'
        context ['entidad'] = 'Proveedores'
        context ['listar_url'] = reverse_lazy('apy:proveedor_lista')
        return context
    
class ProveedorUpdateView(PermisoRequeridoMixin, UpdateView):
    model = Proveedores
    form_class = ProveedorForm
    template_name = 'Proveedores/crear_proveedor.html'
    success_url = reverse_lazy('apy:proveedor_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'Proveedores'
    permission_required = 'change'
    
    def form_valid(self, form):
        
        form.instance.estado = True 
        messages.success(self.request, "Proveedor actualizado correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Proveedor'
        context['entidad'] = 'Proveedores'
        context['listar_url'] = reverse_lazy('apy:proveedor_lista')
        return context

class ProveedorDeleteView(PermisoRequeridoMixin, DeleteView): 
    model = Proveedores
    template_name = 'Proveedores/eliminar_proveedor.html'
    success_url = reverse_lazy('apy:proveedor_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'Proveedores'
    permission_required = 'delete'
    
    def post(self, request, *args, **kwargs):
        
        self.object = self.get_object()
        success_url = self.get_success_url()
        
        self.object.estado = False
        self.object.save()
        
        messages.success(self.request,f"Proveedor {Proveedores} desactivado correctamente")
        return HttpResponseRedirect(success_url)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Proveedor'
        context['entidad'] = 'Proveedores'
        context['listar_url'] = reverse_lazy('apy:proveedor_lista')
        return context
    
#--- Vista para activar Proveedor ---
class ProveedorActivateView(PermisoRequeridoMixin, DeleteView):
    model = Proveedores
    template_name = 'Proveedores/activar_proveedores.html'
    success_url = reverse_lazy('apy:proveedor_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'Proveedores'
    permission_required = 'change'
    
    def post(self, request, *args, **kwargs):
        
        self.object = self.get_object()
        success_url = self.get_success_url()
        
        self.object.estado = True
        self.object.save()
        
        messages.success(self.request,f"Proveedor {Proveedores} activado correctamente")
        return HttpResponseRedirect(success_url)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Activar Proveedor'
        context['entidad'] = 'Proveedores'
        context['listar_url'] = reverse_lazy('apy:proveedor_lista')
        return context    
    
class ProveedorCreateModalView(CreateView):
    model = Proveedores
    form_class = ProveedorForm
    template_name = "Proveedores/modal_proveedores.html"
    success_url = reverse_lazy("apy:proveedor_lista")

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.estado = True 
        try:
            self.object = form.save()
            return JsonResponse({
                "success": True,
                "id": self.object.id_proveedor,
                "text": str(self.object),
                "message": "Proveedor registrado correctamente ✅"
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
