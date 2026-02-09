from django.shortcuts import render, redirect
from apy.models import *
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from apy.forms import *
from django.contrib import messages
# Se elimina la importación de AccessMixin ya que no se usa localmente.
from apy.decorators import PermisoRequeridoMixin 

# --------------Vistas de pagos---------------

class PagosListView(PermisoRequeridoMixin, ListView): 
    model = Pagos
    template_name ='Pagos/listar_pago.html'
    
    # --- Configuración de Permisos ---
    module_name = 'Pagos' 
    permission_required = 'view' 
    
    def get_queryset(self):
        return Pagos.objects.filter(estado=True)
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        nombre = {'nombre' : 'pago'}
        return JsonResponse(nombre)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Pagos'
        context['crear_url'] = reverse_lazy('apy:pagos_crear')
        context['entidad'] = 'Pagos'
        return context
    
#---- vista para listar pagos inactivos -----
class PagosInactivosListView(PermisoRequeridoMixin, ListView): 
    model = Pagos
    template_name = 'Pagos/pago_inactivos.html'
    
    # --- Configuración de Permisos ---
    module_name = 'Pagos' 
    permission_required = 'view' 
    # --------------------------------
    
    def get_queryset(self):
        return Pagos.objects.filter(estado=False) 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_pagos'] = Pagos.objects.count() 
        context['pagos_activos'] = Pagos.objects.filter(estado=True).count()

        return context    
    
class PagosCreateView(PermisoRequeridoMixin, CreateView): 
    model = Pagos
    form_class = PagosForm
    template_name = 'Pagos/crear_pago.html'
    success_url = reverse_lazy('apy:pagos_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'Pagos'
    permission_required = 'add'
    
    def form_valid(self, form):
        form.instance.estado = True 
        messages.success(self.request, "Pago creado correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context ['titulo'] = 'Crear Pagos'
        context ['entidad'] = 'Pagos'
        context ['listar_url'] = reverse_lazy('apy:pagos_lista')
        return context
    
class PagosUpdateView(PermisoRequeridoMixin, UpdateView): 
    model = Pagos
    form_class = PagosForm
    template_name = 'Pagos/crear_pago.html'
    success_url = reverse_lazy('apy:pagos_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'Pagos'
    permission_required = 'change'
    
    def form_valid(self, form):
        messages.success(self.request, "Pago actualizado correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Pagos'
        context['entidad'] = 'Pagos'
        context['listar_url'] = reverse_lazy('apy:pagos_lista')
        return context

class PagosDeleteView(PermisoRequeridoMixin, DeleteView): 
    model = Pagos 
    template_name = 'Pagos/eliminar_pago.html'
    success_url = reverse_lazy('apy:pagos_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'Pagos'
    permission_required = 'delete'
    
    def post(self, request, *args, **kwargs):
        
        self.object = self.get_object()
        success_url = self.get_success_url()
        
        self.object.estado = False
        self.object.save()
        
        messages.success(self.request, f"Cliente {self.object.nombre} desactivado ")
        return HttpResponseRedirect(success_url)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Pagos'
        context['entidad'] = 'Pagos'
        context['listar_url'] = reverse_lazy('apy:pagos_lista')
        return context
    
    #---- vista para activar pagos -----
class PagosActivateView(PermisoRequeridoMixin, DeleteView):
    model = Pagos
    template_name = 'Pagos/activar_gastos.html'
    success_url = reverse_lazy('apy:pagos_lista')  # cambia por tu URL real

    # --- Configuración de Permisos ---
    module_name = 'Pagos'
    permission_required = 'change'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.estado = True
        self.object.save()
        messages.success(self.request, f"Pago {self.object.id} activado correctamente")

        return HttpResponseRedirect(self.get_success_url())