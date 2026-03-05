# ═══════════════════════════════════════════════════════════════
# ACTUALIZACIÓN en apy/view/entrada_vehiculos/views.py
# Agrega vehiculo_cliente_map al context de Create y Update
# para que el template pueda autocompletar el cliente.
# ═══════════════════════════════════════════════════════════════

from builtins import Exception, str, super
import html
import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from apy.models import EntradaVehiculo, Vehiculo, Cliente
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from apy.forms import EntradaVehiculoForm
from django.contrib import messages
from django.template.loader import render_to_string
from apy.decorators import PermisoRequeridoMixin


# ─────────────────────────────────────────────────────────────
# API — datos de una entrada (para autocompletar Crear Servicio)
# ─────────────────────────────────────────────────────────────
def api_entrada_datos(request, pk):
    try:
        # Optimizamos la consulta con select_related para traer los datos del vehículo y cliente de un solo golpe
        entrada = EntradaVehiculo.objects.select_related(
            'id_vehiculo', 
            'id_id_cliente'
        ).get(pk=pk)

        vehiculo = entrada.id_vehiculo
        # Lógica: Usamos el cliente de la entrada, y si no hay, el que tiene registrado el vehículo
        cliente = entrada.id_id_cliente or (vehiculo.id_id_cliente if vehiculo else None)

        return JsonResponse({
            'ok': True,
            'vehiculo_id': vehiculo.pk if vehiculo else None,
            # Formateamos un texto descriptivo para que se vea bien en el Select2
            'vehiculo_texto': f"{vehiculo.placa} — {vehiculo.marca_vehiculo} {vehiculo.modelo_vehiculo}" if vehiculo else 'Sin vehículo',
            'cliente_id': cliente.pk if cliente else None,
            'cliente_texto': str(cliente) if cliente else 'Sin cliente',
        })
    except EntradaVehiculo.DoesNotExist:
        return JsonResponse({'ok': False, 'error': 'Entrada no encontrada'}, status=404)
    except Exception as e:
        return JsonResponse({'ok': False, 'error': str(e)}, status=500)
@login_required 
def obtener_cliente_por_vehiculo(request):
    vehiculo_id = request.GET.get('id')
    
    if not vehiculo_id:
        return JsonResponse({'error': 'No se proporcionó ID'}, status=400)

    try:
        # Buscamos el vehículo y obtenemos su cliente relacionado
        vehiculo = Vehiculo.objects.select_related('cliente').get(id=vehiculo_id)
        return JsonResponse({
            'cliente_id': vehiculo.cliente.id,
            'nombre_cliente': str(vehiculo.cliente) # Útil si quieres mostrar el nombre en consola
        })
    except Vehiculo.DoesNotExist:
        return JsonResponse({'error': 'Vehículo no encontrado'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)    


def _vehiculo_cliente_map():
    """Devuelve dict {vehiculo_id: cliente_id} para autocompletar en el form."""
    return {
        str(v.pk): v.id_cliente_id
        for v in Vehiculo.objects.filter(estado=True).only('pk', 'id_cliente_id')
    }


# ─────────────────────────────────────────────────────────────
# LISTAR
# ─────────────────────────────────────────────────────────────
class EntradaVehiculoListView(PermisoRequeridoMixin, ListView):
    model = EntradaVehiculo
    template_name = 'entrada_vehiculos/listar_entrada_vehiculos.html'
    module_name = 'EntradaVehiculos'
    permission_required = 'view'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return JsonResponse({'nombre': 'Entrada de Vehiculos'})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo']    = 'Lista de Entrada de Vehículos'
        context['crear_url'] = reverse_lazy('apy:entrada_vehiculo_crear')
        context['entidad']   = 'Entrada de Vehículos'
        return context


# ─────────────────────────────────────────────────────────────
# CREAR
# ─────────────────────────────────────────────────────────────
class EntradaVehiculoCreateView(PermisoRequeridoMixin, CreateView):
    model = EntradaVehiculo
    form_class = EntradaVehiculoForm
    template_name = 'entrada_vehiculos/crear_entrada_vehiculos.html'
    success_url = reverse_lazy('apy:entrada_vehiculo_lista')
    module_name = 'EntradaVehiculos'
    permission_required = 'add'

    def form_valid(self, form):
        messages.success(self.request, "Entrada de Vehículo registrada correctamente.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo']              = 'Registrar Entrada de Vehículo'
        context['entidad']             = 'Entrada de Vehículos'
        context['listar_url']          = reverse_lazy('apy:entrada_vehiculo_lista')
        # Mapa JSON para autocompletar cliente al elegir vehículo
        context['vehiculo_cliente_map'] = json.dumps(_vehiculo_cliente_map())
        return context
    
    def get_initial(self):
        initial = super().get_initial()
        # Leemos '?entrada=X' de la URL
        entrada_id = self.request.GET.get('entrada')
        
        if entrada_id:
            # Buscamos la entrada en la base de datos MySQL
            entrada = get_object_or_404(EntradaVehiculo, id_entrada=entrada_id)
            
            # Asignamos los valores iniciales al formulario
            initial['id_vehiculo'] = entrada.id_vehiculo
            initial['id_cliente'] = entrada.id_id_cliente
            
        return initial


# ─────────────────────────────────────────────────────────────
# EDITAR
# ─────────────────────────────────────────────────────────────
class EntradaVehiculoUpdateView(PermisoRequeridoMixin, UpdateView):
    model = EntradaVehiculo
    form_class = EntradaVehiculoForm
    template_name = 'entrada_vehiculos/crear_entrada_vehiculos.html'
    success_url = reverse_lazy('apy:entrada_vehiculo_lista')
    module_name = 'EntradaVehiculos'
    permission_required = 'change'

    def form_valid(self, form):
        messages.success(self.request, "Entrada de Vehículo actualizada correctamente.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo']              = 'Editar Entrada de Vehículo'
        context['entidad']             = 'Entrada de Vehículos'
        context['listar_url']          = reverse_lazy('apy:entrada_vehiculo_lista')
        context['vehiculo_cliente_map'] = json.dumps(_vehiculo_cliente_map())
        return context


# ─────────────────────────────────────────────────────────────
# ELIMINAR
# ─────────────────────────────────────────────────────────────
class EntradaVehiculoDeleteView(PermisoRequeridoMixin, DeleteView):
    model = EntradaVehiculo
    template_name = 'entrada_vehiculos/eliminar_entrada_vehiculos.html'
    success_url = reverse_lazy('apy:entrada_vehiculo_lista')
    module_name = 'EntradaVehiculos'
    permission_required = 'delete'

    def form_valid(self, form):
        messages.success(self.request, "Entrada de Vehículo eliminada correctamente.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo']    = 'Eliminar Entrada de Vehículo'
        context['entidad']   = 'Entrada de Vehículos'
        context['listar_url'] = reverse_lazy('apy:entrada_vehiculo_lista')
        return context


# ─────────────────────────────────────────────────────────────
# MODAL CREAR
# ─────────────────────────────────────────────────────────────
class EntradaCreateModalView(CreateView):
    model = EntradaVehiculo
    form_class = EntradaVehiculoForm
    template_name = "entrada_vehiculos/modal_entrada.html"
    success_url = reverse_lazy("apy:entrada_vehiculo_lista")

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vehiculo_cliente_map'] = json.dumps(_vehiculo_cliente_map())
        return context
    def get(self, request, *args, **kwargs):
        form = self.get_form()
        context = self.get_context_data(form=form)
        html = render_to_string(
            'entrada_vehiculos/modal_entrada.html',
            context,
            request=request
        )
        return JsonResponse({'html': html, 'success': True})

    def form_valid(self, form):
        try:
            self.object = form.save()
            return JsonResponse({
                "success": True,
                "id":      self.object.id_entrada,
                "text":    str(self.object),
                "message": "Entrada registrada correctamente ✅"
            })
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=500)

    def form_invalid(self, form):
        html = render_to_string(self.template_name, {"form": form}, request=self.request)
        return JsonResponse({
            "success": False,
            "html":    html,
            "message": "Corrige los errores en el formulario ❌"
        })
        
        