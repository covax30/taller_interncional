from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.urls import reverse_lazy
from apy.forms import *
import json
from django.db import transaction

# Create your views here.
# --------------Vistas erick---------------

class RepuestoListView(ListView):
    model = Repuesto
    template_name = 'repuestos/listar.html'
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Lista de Repuestos'
        context['crear_url'] = reverse_lazy('apy:repuesto_crear')
        context['entidad'] = 'Repuesto'
        return context
    
class RepuestoCreateView(CreateView):
    model = Repuesto
    form_class = RepuestoForm
    template_name = 'repuestos/crear.html'
    success_url = reverse_lazy('apy:repuesto_lista')
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Repuesto'
        context['entidad'] = 'Repuesto'
        context['listar_url'] = reverse_lazy('apy:repuesto_lista')
        return context
    
    def form_valid(self, form):
        self.object = form.save()

        if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({
                "success": True,
                "id": self.object.id,
                "nombre": str(self.object.nombre)
            })

        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({
                "success": False,
                "errors": form.errors
            }, status=400)
        return super().form_invalid(form)

    
class RepuestoUpdateView(UpdateView):
    model = Repuesto
    form_class = RepuestoForm
    template_name = 'repuestos/crear.html'
    success_url = reverse_lazy('apy:repuesto_lista')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Repuesto'
        context['entidad'] = 'Repuesto'
        context['listar_url'] = reverse_lazy('apy:repuesto_lista')
        return context
    
class RepuestoDeleteView(DeleteView):
    model = Repuesto
    template_name = 'repuestos/eliminar.html'
    success_url = reverse_lazy('apy:repuesto_lista')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Repuesto'
        context['entidad'] = 'Repuesto'
        context['listar_url'] = reverse_lazy('apy:repuesto_lista')
        return context



class RepuestoCreateModalView(CreateView):
    model = Repuesto
    form_class = RepuestoForm
    template_name = "repuestos/modal_form.html"
    success_url = reverse_lazy("apy:repuesto_lista")

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
                "message": "Repuesto registrado correctamente ✅"
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
class DetalleRepuestoCreateModalView(CreateView):
    model = DetalleRepuesto
    form_class = RepuestoscantidadForm
    template_name = "repuestos/modal_detallerepuesto.html"

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['repuestos'] = Repuesto.objects.all()
            print("✅ Repuestos cargados correctamente")
        except Exception as e:
            print(f"❌ Error cargando repuestos: {e}")
            context['repuestos'] = []
        return context

    def get(self, request, *args, **kwargs):
        print("🔍 GET request recibido para modal")
        try:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                print("✅ Es una petición AJAX")
                form = self.get_form()
                print("✅ Formulario creado")
                context = self.get_context_data(form=form)
                print("✅ Contexto creado")
                html = render_to_string(self.template_name, context, request=request)
                print("✅ Template renderizado")
                return JsonResponse({'html': html})
            print("❌ No es AJAX, usando comportamiento normal")
            return super().get(request, *args, **kwargs)
        except Exception as e:
            print(f"❌ ERROR en GET: {str(e)}")
            import traceback
            print("TRACEBACK COMPLETO:")
            print(traceback.format_exc())
            return JsonResponse({
                'success': False,
                'message': f'Error al cargar el formulario: {str(e)}'
            }, status=500)

    # Temporalmente comenta el método post para probar solo el GET
    # def post(self, request, *args, **kwargs):
    #     pass