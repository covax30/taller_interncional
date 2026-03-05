from builtins import Exception, print, super
from locale import str

from django.shortcuts import render, redirect
from apy.models import * # Asegúrate de que PagoServiciosPublicos, Module, y Permission sean importados
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect, JsonResponse
from django.utils.decorators import method_decorator
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.urls import reverse_lazy
from apy.forms import *
from django.contrib import messages
# Se elimina la importación de AccessMixin ya que no se usa localmente.

# Importar el Mixin Corregido (que lanza 403)
from apy.decorators import PermisoRequeridoMixin 

# --------------Vistas de pago servicios publicos---------------

class PagoServiciosListView(PermisoRequeridoMixin, ListView): 
    model = PagoServiciosPublicos
    template_name ='Pago_Servicios/listar_pagoservicios.html'
    
    # --- Configuración de Permisos ---
    module_name = 'PagoServicios'
    permission_required = 'view' 
    def get_queryset(self):
        return PagoServiciosPublicos.objects.filter(estado=True)
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        # Usa el Mixin importado de apy.decorators
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        nombre = {'nombre' : 'pago servicios'}
        return JsonResponse(nombre)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Pago Servicios Publicos'
        context['crear_url'] = reverse_lazy('apy:pago_servicios_crear')
        context['entidad'] = 'PagoServiciosPublicos'
        return context
    
#--- vista para liistar pago servicios inactivos ---
class PagoServiciosInactivosListView(PermisoRequeridoMixin, ListView): 
    model = PagoServiciosPublicos
    template_name ='Pago_Servicios/pagoservicios_inactivos.html'
    
    # --- Configuración de Permisos ---
    module_name = 'PagoServicios'
    permission_required = 'view' 
    
    def get_queryset(self):
        return PagoServiciosPublicos.objects.filter(estado=False)
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        # Usa el Mixin importado de apy.decorators
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        nombre = {'nombre' : 'pago servicios inactivos'}
        return JsonResponse(nombre)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Pago Servicios Públicos Inactivos'
        context['crear_url'] = reverse_lazy('apy:pago_servicios_lista')
        context['entidad'] = 'PagoServiciosPublicos'
        return context    
    
    
class PagoServiciosCreateView(PermisoRequeridoMixin, CreateView):
    model = PagoServiciosPublicos
    form_class = PagoServiciosForm
    template_name = 'pago_servicios/crear.html'
    success_url = reverse_lazy('apy:pago_servicios_lista')
    module_name = 'PagoServicios'
    permission_required = 'add'

    def form_valid(self, form):
        # 1. Marcamos el estado del pago
        form.instance.estado = True
        
        # 2. Guardamos el objeto PagoServicio y lo capturamos
        response = super().form_valid(form)
        self.object = form.save() 

        # 3. Creamos el Gasto asociado
        Gastos.objects.create(
            monto=self.object.monto,
            descripcion=f"Pago de servicio: {self.object.get_servicio_display()}",
            tipo_gastos='costo fijo', 
            id_pagos_servicios=self.object, # Relacionamos con el pago recién creado
            fecha=timezone.now().date()
        )

        messages.success(self.request, "Pago de servicio y gasto registrados correctamente ✅")
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Pago Servicios Públicos'
        context['entidad'] = 'PagoServiciosPublicos'
        context['listar_url'] = reverse_lazy('apy:pago_servicios_lista')
        return context
    
class PagoServiciosUpdateView(PermisoRequeridoMixin, UpdateView):
    model = PagoServiciosPublicos
    form_class = PagoServiciosForm
    template_name = 'Pago_Servicios/crear_pagoservicios.html'
    success_url = reverse_lazy('apy:pago_servicios_lista')
    
    module_name = 'PagoServicios'
    permission_required = 'change'
    
    def form_valid(self, form):
        # 1. Guardamos los cambios del Pago
        response = super().form_valid(form)
        pago = self.object

        # 2. Buscamos el Gasto asociado para actualizarlo
        # Usamos .filter().update() para ser más eficientes
        Gastos.objects.filter(id_pagos_servicios=pago).update(
            monto=pago.monto,
            descripcion=f"Pago de servicio (Editado): {pago.get_servicio_display()}",
            # Mantenemos la fecha original o la actualizamos según tu preferencia
        )

        messages.success(self.request, "Pago de servicio y gasto asociado actualizados correctamente ✅")
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Pago Servicios Públicos'
        context['entidad'] = 'PagoServiciosPublicos'
        context['listar_url'] = reverse_lazy('apy:pago_servicios_lista')
        return context
    
class PagoServiciosDeleteView(PermisoRequeridoMixin, DeleteView): 
    model = PagoServiciosPublicos
    template_name = 'Pago_Servicios/eliminar_pagoservicios.html'
    success_url = reverse_lazy('apy:pago_servicios_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'PagoServicios'
    permission_required = 'delete'
    
    def post(self, request, *args, **kwargs):
        
        self.object = self.get_object()
        success_url = self.get_success_url()
        
        self.object.estado = False
        self.object.save()
        
        messages.success(self.request, f"Servicio {self.object.servicio} desactivado correctamente")
        return HttpResponseRedirect(success_url)
    
    def form_valid(self, form):

        messages.success(self.request, "Pago de servicio eliminado correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Pago Servicios Publicos'
        context['entidad'] = 'PagoServiciosPublicos'
        context['listar_url'] = reverse_lazy('apy:pago_servicios_lista')
        return context
    
#--- vista para activar pago servicios ---
class PagoServiciosActivateView(PermisoRequeridoMixin, UpdateView): 
    model = PagoServiciosPublicos
    template_name = 'Pago_Servicios/activar_pagoservicios.html'
    success_url = reverse_lazy('apy:pago_servicios_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'PagoServicios'
    permission_required = 'delete'
    
    def form_valid(self, form):
        # Activar el pago de servicio estableciendo estado a True
        self.object.estado = True
        self.object.save()
        messages.success(self.request, f"Pago de servicio {self.object.servicio} activado correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Activar Pago Servicios Publicos'
        context['entidad'] = 'PagoServiciosPublicos'
        context['listar_url'] = reverse_lazy('apy:pago_servicios_lista')
        return context    
      
class PagoServiciosCreateModalView(PermisoRequeridoMixin, CreateView):
    model = PagoServiciosPublicos
    form_class = PagoServiciosForm
    template_name = "Pago_Servicios/modal_pago_servicios.html"
    success_url = reverse_lazy("apy:pago_servicios_lista")

    # --- Configuración de Permisos ---
    module_name = 'PagoServicios'
    permission_required = 'add'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        try:
            self.object = form.save()
            return JsonResponse({
                "success": True,
                "id": self.object.id_servicio,
                "text": f"{self.object.servicio} - {self.object.monto}",
                "message": "Pago de servicio registrado correctamente"
            })
        except Exception as e:
            import traceback
            print("ERROR EN PagoServiciosCreateModalView:", traceback.format_exc())  # imprime la traza completa en consola
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