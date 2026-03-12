from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from apy.forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Importar modelos necesarios
from apy.models import Gastos, Module, Permission 
from django.http import HttpResponse 

# Importar las herramientas de permisos centralizadas
from apy.decorators import PermisoRequeridoMixin, permiso_requerido_fbv 

# **VARIABLE DE CONFIGURACIÓN DEL MÓDULO**
# Definimos el nombre exacto de la DB en una variable para fácil mantenimiento
GASTOS_MODULE_NAME = 'Gastos'

# --------------Vistas de Gastos (CBVs)---------------

class GastosListView(PermisoRequeridoMixin, ListView):
    model = Gastos
    template_name ='Gastos/listar_gasto.html' 
    
    # --- Configuración de Permisos ---
    module_name = GASTOS_MODULE_NAME # <-- CORRECCIÓN APLICADA
    permission_required = 'view'
    
    def get_queryset(self):
        return Gastos.objects.filter(estado=True)
    
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
    
#-----------------Vistas de Gastos (CBVs) de Inactivos---------------
class GastosInactivosListView(PermisoRequeridoMixin, ListView):
    model = Gastos
    template_name = 'Gastos/gastos_inactivos.html'
    
    # --- Configuración de Permisos ---
    module_name = GASTOS_MODULE_NAME 
    permission_required = 'view'
    
    def get_queryset(self):
        return Gastos.objects.filter(estado=False)
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        nombre = {'nombre' : 'Gastos Inactivos'}
        return JsonResponse(nombre)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Gastos Inactivos'
        context['crear_url'] = reverse_lazy('apy:gasto_crear')
        context['entidad'] = 'Gastos'
        return context
    
        
class GastosCreateView(PermisoRequeridoMixin, CreateView):
    form_class = GastosForm
    template_name = 'Gastos/crear_gasto.html'
    success_url = reverse_lazy('apy:gasto_lista')
    
    # --- Configuración de Permisos ---
    module_name = GASTOS_MODULE_NAME 
    permission_required = 'add'
    
    def form_valid(self, form):
        form.instance.estado = True 
        response = super().form_valid(form)
        
        # 2. Lógica Financiera: Crear el movimiento en Caja
        Caja.objects.create(
            tipo_movimiento='Egreso',  # O el valor que uses en tu modelo
            monto=form.instance.monto,
            descripcion=f"Gasto: {form.instance.tipo_gastos} - {form.instance.descripcion}",
            fecha=form.instance.fecha,
            estado=True
        )
        
        messages.success(self.request, "Gasto creado y descontado de caja")
        return response
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
    module_name = GASTOS_MODULE_NAME # <-- CORRECCIÓN APLICADA
    permission_required = 'change'
    
    def form_valid(self, form):
        
        form.instance.estado = True 
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
    module_name = GASTOS_MODULE_NAME # <-- CORRECCIÓN APLICADA
    permission_required = 'delete'
    
    def post(self, request, *args, **kwargs):
        
        self.object = self.get_object()
        success_url = self.get_success_url()
        
        self.object.estado = False
        self.object.save()
        
        messages.success(self.request, f"Gasto {self.object.descripcion} desactivado ")
        return HttpResponseRedirect(success_url)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Gastos'
        context['entidad'] = 'Gastos'
        context['listar_url'] = reverse_lazy('apy:gasto_lista')
        return context
    
#----vista de activacion de gasto----
class GastosActivateView(PermisoRequeridoMixin, DeleteView):
    model = Gastos
    template_name = 'Gastos/activar_gastos.html'
    success_url = reverse_lazy('apy:gasto_lista')
    
    # --- Configuración de Permisos ---
    module_name = GASTOS_MODULE_NAME # <-- CORRECCIÓN APLICADA
    permission_required = 'delete'
    
    def post(self, request, *args, **kwargs):
        
        self.object = self.get_object()
        success_url = self.get_success_url()
        
        self.object.estado = True
        self.object.save()
        
        messages.success(self.request, f"Gasto {self.object.descripcion} activado ")
        return HttpResponseRedirect(success_url)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Activar Gastos'
        context['entidad'] = 'Gastos'
        context['listar_url'] = reverse_lazy('apy:gasto_lista')
        return context    
    
# --------------Vistas de Gastos (VBFs estandarizadas)---------------

# Sustituir la lógica manual de check_custom_permission por el decorador centralizado
@permiso_requerido_fbv(module_name=GASTOS_MODULE_NAME, permission_required='view') # <-- CORRECCIÓN APLICADA
def estadisticas_view(request):
    
    # Contar total de gastos
    total_gastos = Gastos.objects.count()

    # Puedes agregar más estadísticas aquí
    context = {
        'total_gastos': total_gastos,
    }
    return render(request, 'estadisticas.html', context)

# Sustituir la lógica manual por el decorador centralizado, usando api=True
@permiso_requerido_fbv(module_name=GASTOS_MODULE_NAME, permission_required='view', api=True) # <-- CORRECCIÓN APLICADA
def api_contador_gastos(request):
    total_gastos = Gastos.objects.count()
    return JsonResponse({'total_gastos': total_gastos})
