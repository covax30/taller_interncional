# Importaciones necesarias (basado en tus imports)
from apy.tasks import ejecutar_respaldo_asincrono
from django.shortcuts import render, redirect, get_object_or_404
from apy.models import * # Asume que aquí tienes tus modelos de BackupLog y ConfiguracionRespaldo
from django.views import View
from django.http import JsonResponse
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin
from django.utils import timezone
from django.http import FileResponse, Http404
from django.conf import settings, os

# ------------------------------------------------------------------------------
# MIXIN DE RESTRICCIÓN (Asegura que solo Superusuarios accedan)
# ------------------------------------------------------------------------------

class SuperuserRequiredMixin(UserPassesTestMixin):
    """
    Mixin que asegura que solo los superusuarios (admin) puedan acceder.
    """
    def test_func(self):
        # Asegura que el usuario esté autenticado y sea superusuario
        return self.request.user.is_authenticated and self.request.user.is_superuser
    
    def handle_no_permission(self):
        # Redirige a una página de error o a la principal si no tiene permisos
        messages.error(self.request, '⛔ No tienes permisos de administrador para acceder a esta sección.')
        return redirect(reverse_lazy('apy:index')) # Asume que 'apy:index' existe

# ------------------------------------------------------------------------------
# 1. VIEW PRINCIPAL (Muestra el estado y los formularios)
# ------------------------------------------------------------------------------

class RespaldoView(SuperuserRequiredMixin, View):
    template_name = 'respaldo/configuracion_respaldo.html'
    
    # Aplicar csrf_exempt a la vista completa para simplificar el manejo de POSTs en el mismo template
    # Aunque es mejor usar csrf_protect y csrf_token
    # @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        # Se mantiene la misma convención de tus vistas
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = {}
        context['entidad'] = 'Módulo de Respaldo'
        context['titulo'] = 'Configuración de Respaldo y Mantenimiento'
        
        # 1. Información de Último Respaldo
        try:
            # Asume que BackupLog existe en apy.models
            context['ultimo_backup_fecha'] = BackupLog.objects.filter(estado='Éxito').latest('fecha_inicio').fecha_fin
        except:
            context['ultimo_backup_fecha'] = None

        # 2. Configuración Programada
        try:
             # Asume que ConfiguracionRespaldo existe en apy.models
            configuracion = ConfiguracionRespaldo.objects.get(pk=1) 
            context['frecuencia_actual'] = configuracion.frecuencia
            context['hora_actual'] = configuracion.hora_ejecucion
        except:
            context['frecuencia_actual'] = 'inactivo'
            context['hora_actual'] = '03:00'
        
        # 3. Métricas (Estos valores deberían ser calculados por el modelo)
        # Reemplaza estos valores estáticos con cálculos reales si es necesario
        context['cantidad_programados'] = BackupLog.objects.filter(tipo='Automático', estado='Éxito').count()
        context['espacio_ocupado'] = "1.2 GB" 

        # 4. Logs del historial (Para llenar la tabla en la parte inferior)
        context['historial_respaldos'] = BackupLog.objects.all().order_by('-fecha_inicio')[:10]
        
        # URLs necesarias para los POSTs
        context['ejecutar_url'] = reverse_lazy('apy:backup_ejecutar')
        context['configurar_url'] = reverse_lazy('apy:backup_configurar')
        
        return context

    def get(self, request, *args, **kwargs):
        """Maneja la solicitud GET para mostrar la página."""
        context = self.get_context_data()
        return render(request, self.template_name, context)

# ------------------------------------------------------------------------------
# 2. VIEW PARA EJECUTAR RESPALDO MANUAL (Maneja el POST del Bloque Manual)
# ------------------------------------------------------------------------------

# apy/view/respaldo/views.py

# ... otras clases y funciones ...

class EjecutarRespaldoManualView(SuperuserRequiredMixin, View):
    
    def post(self, request, *args, **kwargs):
        # 1. Obtener datos del formulario (debería ser similar a lo que ya tienes)
        incluir_db = request.POST.get('incluir_base_datos') == 'on'
        incluir_archivos = request.POST.get('incluir_archivos_media') == 'on'
        ubicacion = request.POST.get('ubicacion_destino', 'local') # O el nombre real de tu campo

        try:
            # 2. Crear el registro de Log con estado 'En Proceso'
            log = BackupLog.objects.create(
                tipo='Manual',
                estado='En Proceso',
                usuario=request.user # Asume que el usuario que ejecuta la petición es request.user
            )

            # 3. ⚠️ LLAMADA REAL A LA TAREA DE CELERY
            # El método .delay() ejecuta la función en un proceso Worker en segundo plano.
            ejecutar_respaldo_asincrono.delay(
                log.pk, 
                incluir_db, 
                incluir_archivos, 
                ubicacion
            )

            messages.success(request, f'✅ Respaldo manual iniciado (ID: {log.pk}). Será completado en segundo plano.')
            
        except Exception as e:
            messages.error(request, f'❌ Error al iniciar el respaldo: {e}')
        
        return redirect(reverse_lazy('apy:configuracion_respaldo'))
# ------------------------------------------------------------------------------
# 3. VIEW PARA CONFIGURAR RESPALDO AUTOMÁTICO (Maneja el POST del Bloque Programación)
# ------------------------------------------------------------------------------

class ConfigurarRespaldoAutomaticoView(SuperuserRequiredMixin, View):
    
    @method_decorator(csrf_exempt) # Si tu proyecto requiere csrf_exempt en POSTs
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
        
    def post(self, request, *args, **kwargs):
        frecuencia = request.POST.get('frecuencia')
        hora = request.POST.get('hora')
        
        try:
            # Asume que solo hay un objeto de configuración (pk=1)
            configuracion, created = ConfiguracionRespaldo.objects.get_or_create(pk=1)
            configuracion.frecuencia = frecuencia
            configuracion.hora_ejecucion = hora 
            configuracion.save()

            # (Opcional) Aquí iría la lógica para configurar/actualizar el scheduler (ej. Celery Beat)
            
            messages.success(request, f'💾 Configuración de respaldo automático guardada: {frecuencia} a las {hora}.')
        except Exception as e:
            messages.error(request, f'❌ Error al guardar la configuración: {e}')
            
        return redirect(reverse_lazy('apy:configuracion_respaldo'))


# ------------------------------------------------------------------------------
# 4. VIEW PARA DESCARGAR UN ARCHIVO DE RESPALDO
# ------------------------------------------------------------------------------

# apy/view/respaldo/views.py

# ... otras clases y funciones ...

class DescargarRespaldoView(SuperuserRequiredMixin, View):
    
    def get(self, request, pk, *args, **kwargs):
        try:
            log = get_object_or_404(BackupLog, pk=pk)
            
            # 1. Verificar el estado del Log antes de intentar la descarga
            if log.estado != 'Éxito' or not log.ruta_archivo:
                messages.warning(request, f'⚠️ El respaldo #{pk} no está disponible para descarga (Estado: {log.estado}).')
                return redirect(reverse_lazy('apy:configuracion_respaldo'))
            
            # 2. Construir la ruta segura del archivo
            backup_base_dir = os.path.join(settings.MEDIA_ROOT, 'backups')
            file_path = os.path.join(backup_base_dir, log.ruta_archivo)
            
            # 3. ⚠️ Seguridad: Verificar que el archivo exista y esté dentro de la ruta de backups
            if not os.path.exists(file_path) or not file_path.startswith(backup_base_dir):
                 # Si la ruta no existe o intenta acceder a otra carpeta (seguridad)
                raise Http404 
            
            # 4. Entrega el archivo usando FileResponse
            return FileResponse(
                open(file_path, 'rb'), 
                as_attachment=True, 
                filename=log.ruta_archivo # Usa el nombre que guardó la tarea
            )
            
        except Http404:
            messages.error(request, '❌ Error: El archivo de respaldo no se encuentra o la ruta es inválida.')
            return redirect(reverse_lazy('apy:configuracion_respaldo')) 
        except Exception as e:
            messages.error(request, f'❌ Error al intentar descargar el respaldo: {e}')
            return redirect(reverse_lazy('apy:configuracion_respaldo'))
    
    def get(self, request, pk, *args, **kwargs):
        try:
            log = get_object_or_404(BackupLog, pk=pk)
            
            # **LÓGICA DE DESCARGA DE ARCHIVOS**
            # Si el archivo está en el servidor local:
            # from django.http import FileResponse
            # return FileResponse(log.obtener_ruta_archivo(), as_attachment=True, filename=log.nombre_archivo)
            
            # Si el archivo está en la nube, se redirige o se usa la lógica del storage backend
            
            messages.success(request, f'Preparando descarga del respaldo #{pk}...')
            # En un caso real, esto sería reemplazado por la lógica de FileResponse o StreamingHttpResponse
            return redirect(reverse_lazy('apy:configuracion_respaldo')) 
            
        except Exception:
            messages.error(request, '❌ Error: El respaldo solicitado no está disponible o la ruta es incorrecta.')
            return redirect(reverse_lazy('apy:configuracion_respaldo'))