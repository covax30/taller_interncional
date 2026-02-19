from django.shortcuts import render, redirect
from apy.models import * # Asegúrate de que Nomina, Module, y Permission sean importados
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from apy.forms import *
from django.contrib import messages
# Se elimina la importación de AccessMixin ya que no se usa localmente.
from apy.decorators import PermisoRequeridoMixin # <-- Se mantiene solo la importación


# --------------Vistas de Nómina---------------

class NominaListView(PermisoRequeridoMixin, ListView): 
    model = Nomina
    template_name = 'Nomina/listar_nomina.html'
    
    # --- Configuración de Permisos ---
    module_name = 'Nomina'
    permission_required = 'view'
    
    def get_queryset(self):
        return Nomina.objects.filter(estado=True)
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        # Usa el Mixin importado de apy.decorators
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        nombre = {'nombre' : 'Yury'}
        return JsonResponse(nombre)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista pago de Nomina'
        context['crear_url'] = reverse_lazy('apy:nomina_crear')
        context['entidad'] = 'Nomina'
        return context
    
#---- vista para listar nomina inactiva -----
class NominaInactivosListView(PermisoRequeridoMixin, ListView): 
    model = Nomina
    template_name = 'Nomina/nomina_inactiva.html'
    
    # --- Configuración de Permisos ---
    module_name = 'Nomina'
    permission_required = 'view'
    # --------------------------------
    
    def get_queryset(self):
        return Nomina.objects.filter(estado=False) 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_nominas'] = Nomina.objects.count() 
        context['nominas_activas'] = Nomina.objects.filter(estado=True).count()

        return context    
    
class NominaCreateView(PermisoRequeridoMixin, CreateView): 
    model = Nomina
    form_class = NominaForm
    template_name = 'Nomina/crear_nomina.html'
    success_url = reverse_lazy('apy:nomina_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'Nomina'
    permission_required = 'add'
    
    def form_valid(self, form):
        form.instance.estado = True 
        messages.success(self.request, "Nomina creada correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Nomina'
        context['entidad'] = 'Nomina'
        context['listar_url'] = reverse_lazy('apy:nomina_lista')
        return context
    
class NominaUpdateView(PermisoRequeridoMixin, UpdateView): 
    model = Nomina
    form_class = NominaForm
    template_name = 'Nomina/crear_nomina.html'
    success_url = reverse_lazy('apy:nomina_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'Nomina'
    permission_required = 'change'
    
    def form_valid(self, form):
        messages.success(self.request, "Nomina actualizada correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar empleado'
        context['entidad'] = 'Nomina'
        context['listar_url'] = reverse_lazy('apy:nomina_lista')
        return context

class NominaDeleteView(PermisoRequeridoMixin, DeleteView): 
    model = Nomina
    template_name = 'Nomina/eliminar_nomina.html'
    success_url = reverse_lazy('apy:nomina_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'Nomina'
    permission_required = 'delete'
    
    def post(self, request, *args, **kwargs):
        
        self.object = self.get_object()
        success_url = self.get_success_url()
        
        self.object.estado = False
        self.object.save()
        
        messages.success(self.request, f"Nomina {Nomina} desactivado ")
        return HttpResponseRedirect(success_url)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar pago de Nomina'
        context['entidad'] = 'Nomina'
        context['listar_url'] = reverse_lazy('apy:nomina_lista')
        return context
#---- vista para activar nomina -----
class NominaActivateView(DeleteView):
    model = Nomina
    template_name = 'Nomina/activar_nomina.html'
    success_url = reverse_lazy('apy:nomina_lista') 
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.estado = True
        self.object.save()
        messages.success(self.request, f"Nómina {self.object.id} activada correctamente")

        return HttpResponseRedirect(self.get_success_url())
    
    
class NominaCreateModalView(CreateView):
    model = Nomina
    form_class = NominaForm
    template_name = "Nomina/modal_nomina.html"
    success_url = reverse_lazy("apy:nomina_lista")

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.estado = True 
        try:
            self.object = form.save()
            return JsonResponse({
                "success": True,
                "id": self.object.id,
                "text": str(self.object),
                "message": "Nomina registrada correctamente ✅"
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