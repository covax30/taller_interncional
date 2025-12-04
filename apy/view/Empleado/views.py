from django.shortcuts import render, redirect
from apy.models import Empleado, Module, Permission # <-- Asegúrate de importar Module y Permission
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from apy.forms import *
from django.contrib import messages
# Importar el Mixin centralizado que lanza el 403
from apy.decorators import PermisoRequeridoMixin # <-- Importación Crítica
# from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin # <-- Ya no es necesario


# Create your views here.
# --------------Vistas Karol---------------

def empleado(request):
    data = {
        'Empleado':'Empleado',
        'titulo':'Lista de Empleados',
        'empleados': Empleado.objects.all()
    }
    return render(request, 'Empleado/cont_Empleado.html', data)

# -------------------------------------------------------------------------
# APLICACIÓN DEL MIXIN DE PERMISOS (LANZA 403)
# -------------------------------------------------------------------------

class EmpleadoListView(PermisoRequeridoMixin, ListView):
    model = Empleado
    template_name ='Empleado/listar_empleado.html'
    
    # --- Configuración de Permisos ---
    module_name = 'Empleados' 
    permission_required = 'view'
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        # El Mixin PermisoRequeridoMixin se ejecuta primero
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        nombre = {'nombre' : 'Yury'}
        return JsonResponse(nombre)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Empleados'
        context['crear_url'] = reverse_lazy('apy:empleado_crear')
        context['entidad'] = 'Empleado'
        return context
    
class EmpleadoCreateView(PermisoRequeridoMixin, CreateView):
    model = Empleado
    form_class = EmpleadoForm
    template_name = 'Empleado/crear_empleado.html'
    success_url = reverse_lazy('apy:empleado_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'Empleados'
    permission_required = 'add'
    
    def form_valid(self, form):
        messages.success(self.request, "Empleado creado correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context ['titulo'] = 'Crear Empleado'
        context ['entidad'] = 'Empleados'
        context ['listar_url'] = reverse_lazy('apy:empleado_lista')
        return context
    
class EmpleadoUpdateView(PermisoRequeridoMixin, UpdateView):
    model = Empleado
    form_class = EmpleadoForm
    template_name = 'Empleado/crear_empleado.html'
    success_url = reverse_lazy('apy:empleado_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'Empleados'
    permission_required = 'change'
    
    def form_valid(self, form):
        messages.success(self.request, "Empleado actualizado correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar empleado'
        context['entidad'] = 'Empleados'
        context['listar_url'] = reverse_lazy('apy:empleado_lista')
        return context

class EmpleadoDeleteView(PermisoRequeridoMixin, DeleteView):
    model = Empleado
    template_name = 'Empleado/eliminar_empleado.html'
    success_url = reverse_lazy('apy:empleado_lista')
    
    # --- Configuración de Permisos ---
    module_name = 'Empleados'
    permission_required = 'delete'
    
    def form_valid(self, form):
        messages.success(self.request, "Empleado eliminado correctamente")
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Empleado'
        context['entidad'] = 'Empleados'
        context['listar_url'] = reverse_lazy('apy:empleado_lista')
        return context
    
class EmpleadoCreateModalView(CreateView):
    model = Empleado
    form_class = EmpleadoForm
    template_name = "Empleado/modal_empleado.html"
    success_url = reverse_lazy("apy:empleado_lista")

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
                "message": "Empleado registrado correctamente ✅"
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

class EmpleadoCreateModalMantenimientoView(CreateView):
    model = Empleado_Mantenimiento
    form_class = Empleado_Mantenimiento_Form
    template_name = "Empleado/empleado_mantenimiento_form.html"

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save()
        return JsonResponse({
            "success": True,
            "id": self.object.id_empleado_mantenimiento,
            "text": str(self.object),
            "message": "Empleado registrado correctamente"
        })

    def form_invalid(self, form):
        html = render_to_string(self.template_name, {"form": form}, request=self.request)
        return JsonResponse({
            "success": False,
            "html": html,
            "message": "Por favor corrige los errores"
        })
