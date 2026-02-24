from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from apy.forms import *
from django.contrib import messages
# Importar modelos necesarios para la vista
from apy.models import Caja 
# Importar el Mixin Corregido (que lanza 403)
from apy.decorators import PermisoRequeridoMixin 


# --------------Vistas de Caja---------------
class CajaListView(PermisoRequeridoMixin, ListView):
    model = Caja
    template_name = 'Caja/listar_caja.html'
    
    # --- Configuración de Permisos ---
    module_name = 'Caja' 
    permission_required = 'view'
    
    def get_queryset(self):
        return Caja.objects.filter(estado=True)
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        # El Mixin se ejecuta antes de super().dispatch
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        nombre = {'nombre' : 'Yury'}
        return JsonResponse(nombre)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista Caja'
        context['crear_url'] = reverse_lazy('apy:caja_crear')
        context['entidad'] = 'Caja'
        return context
    
class CajaInactivaListView(PermisoRequeridoMixin, ListView):
    model = Caja
    template_name = 'Caja/caja_inactiva.html'
    
    # --- Configuración de Permisos ---
    module_name = 'Caja' 
    permission_required = 'view'
    
    def get_queryset(self):
        return Caja.objects.filter(estado=False)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista Ingreso a Caja Inactivos'
        context['listar_url'] = reverse_lazy('apy:caja_lista')
        context['crear_url'] = reverse_lazy('apy:caja_crear')
        return context    
    
class CajaCreateView(PermisoRequeridoMixin, CreateView):
    model = Caja
    form_class = CajaForm
    template_name = 'Caja/crear_caja.html'
    success_url = reverse_lazy('apy:caja_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'Caja'
    permission_required = 'add'
    
    def form_valid(self, form):
        form.instance.estado = True 
        messages.success(self.request, "Caja creada correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Caja'
        context['entidad'] = 'Caja'
        context['listar_url'] = reverse_lazy('apy:caja_lista')
        return context
    
class CajaUpdateView(PermisoRequeridoMixin, UpdateView):
    model = Caja
    form_class = CajaForm
    template_name = 'Caja/crear_caja.html'
    success_url = reverse_lazy('apy:caja_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'Caja'
    permission_required = 'change'
    
    def form_valid(self, form):
        
        form.instance.estado = True 
        messages.success(self.request, "Caja actualizada correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Caja'
        context['entidad'] = 'Caja'
        context['listar_url'] = reverse_lazy('apy:caja_lista')
        return context

class CajaDeleteView(PermisoRequeridoMixin, DeleteView):
    model = Caja
    template_name = 'Caja/eliminar_caja.html'
    success_url = reverse_lazy('apy:caja_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'Caja'
    permission_required = 'delete'
    
    def post(self, request, *args, **kwargs):
        
        self.object = self.get_object()
        success_url = self.get_success_url()
        
        self.object.estado = False
        self.object.save()
        
        messages.success(self.request,     f"Ingreso a caja {Caja} desactivado correctamente")
        return HttpResponseRedirect(success_url)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Registro Caja'
        context['entidad'] = 'Caja'
        context['listar_url'] = reverse_lazy('apy:caja_lista')
        return context
    
# Activar Caja
class CajaActivateView(PermisoRequeridoMixin, DeleteView):
    model = Caja
    template_name = 'Caja/activar_caja.html'
    success_url = reverse_lazy('apy:caja_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'Caja'
    permission_required = 'change'
    
    def post(self, request, *args, **kwargs):
        
        self.object = self.get_object()
        success_url = self.get_success_url()
        
        self.object.estado = True
        self.object.save()
        
        messages.success(self.request,     f"Ingreso a caja {Caja} activado correctamente")
        return HttpResponseRedirect(success_url)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Activar Registro Caja'
        context['entidad'] = 'Caja'
        context['listar_url'] = reverse_lazy('apy:caja_lista')
        return context    