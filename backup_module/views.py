# views.py - ARCHIVO CORREGIDO Y MODIFICADO

# Importaciones necesarias (basado en tus imports)
# from apy.tasks import ejecutar_respaldo_asincrono # ❌ ELIMINADO/COMENTADO: Ya no usamos Celery
from django.shortcuts import render, redirect, get_object_or_404
from .models import BackupLog # Asume que aquí tienes tus modelos de BackupLog y ConfiguracionRespaldo
from django.views import View
from django.http import JsonResponse, FileResponse, Http404
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin
from django.utils import timezone

# ------------------------------------------------------------------------------
# ✅ NUEVAS IMPORTACIONES REQUERIDAS PARA EJECUCIÓN ASÍNCRONA NATIVA
# ------------------------------------------------------------------------------
from django.conf import settings
import os
import sys         # Para obtener la ruta del intérprete Python
import subprocess  # Para lanzar el proceso en segundo plano
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# ✅ FUNCIÓN DE EJECUCIÓN ASÍNCRONA (Reemplaza a Celery.delay())
# ------------------------------------------------------------------------------

# views.py

def iniciar_respaldo_en_segundo_plano(user_id):
    """
    Lanza el Comando de Gestión 'backup_db' de Django como un proceso secundario,
    capturando la salida y el error en un archivo de log temporal.
    """
    # 1. Rutas críticas
    manage_py_path = os.path.join(settings.BASE_DIR, 'manage.py')
    
    # 2. Comando a ejecutar (usando el intérprete Python activo)
    command = [
        sys.executable,     # Ruta al intérprete Python activo (del entorno virtual)
        manage_py_path,
        'backup_db',        # Llama a 'python manage.py backup_db'
        f'--user_id={user_id}', # Pasa el ID del usuario para el log
    ]
    
    # Define la ruta para el archivo de log de errores/salida
    log_file_path = os.path.join(settings.BASE_DIR, 'backup_error.log')

    # Abre el archivo de log para la salida del proceso secundario (modo 'a' para añadir)
    with open(log_file_path, 'a') as log_file:
        
        # 3. Lanzar el proceso (CLAVE EN WINDOWS)
        if sys.platform == "win32":
            subprocess.Popen(command, 
                             creationflags=subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS,
                             stdout=log_file, # Redirige la salida estándar al archivo
                             stderr=log_file) # Redirige el error al archivo
        else:
            # Fallback para sistemas Unix (Linux/Mac)
            subprocess.Popen(command, start_new_session=True, 
                             stdout=log_file, 
                             stderr=log_file)
    
# ------------------------------------------------------------------------------
# MIXIN DE RESTRICCIÓN (Asegura que solo Superusuarios accedan)
# ... (el resto del código sigue igual)
    """
    Lanza el Comando de Gestión 'backup_db' de Django como un proceso secundario,
    independiente de la conexión del usuario (Fire-and-forget).
    """
    # 1. Rutas críticas
    manage_py_path = os.path.join(settings.BASE_DIR, 'manage.py')
    
    # 2. Comando a ejecutar (usando el intérprete Python activo)
    command = [
        sys.executable,  # Ruta al intérprete Python activo (del entorno virtual)
        manage_py_path,
        'backup_db',     # Llama a 'python manage.py backup_db'
        f'--user_id={user_id}', # Pasa el ID del usuario para el log
    ]
    
    # 3. Lanzar el proceso (CLAVE EN WINDOWS)
    # Las flags aseguran que el proceso no bloquee el servidor web y no muestre una ventana de consola.
    if sys.platform == "win32":
        subprocess.Popen(command, 
                         creationflags=subprocess.CREATE_NEW_PROCESS_GROUP | subprocess.DETACHED_PROCESS,
                         stdout=subprocess.DEVNULL,  
                         stderr=subprocess.DEVNULL)
    else:
        # Fallback para sistemas Unix (Linux/Mac)
        subprocess.Popen(command, start_new_session=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

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
        return redirect(reverse_lazy('backup_module:index')) # Asume que 'apy:index' existe

# ------------------------------------------------------------------------------
# 1. VIEW PRINCIPAL (Muestra el estado y los formularios)
# ------------------------------------------------------------------------------

# views.py

class RespaldoView(SuperuserRequiredMixin, View):
    template_name = 'apy/configuracion_respaldo.html' # Ajusta la ruta a tu aplicación ('apy' o 'backup_module')

    def get(self, request, *args, **kwargs):
        
        # 1. Obtener todos los logs de respaldo (ordenados por el más reciente)
        # Importante: Asegúrate de que BackupLog esté importado.
        logs = BackupLog.objects.all().order_by('-fecha_inicio') 
        
        # 2. Obtener el último respaldo exitoso para el panel lateral
        ultimo_backup = logs.filter(estado='Éxito').order_by('-fecha_fin').first()
        
        # 3. Preparar el contexto
        context = {
            # Se usa en la tabla de Historial (lo que vamos a recorrer)
            'logs': logs, 
            
            # Variables del panel izquierdo
            'ultimo_backup_fecha': ultimo_backup.fecha_fin if ultimo_backup else None,
            
            # Otras métricas (puedes agregar lógica para calcular la cantidad/espacio real)
            'cantidad_programados': ConfiguracionRespaldo.objects.count(), # Ejemplo
            'espacio_ocupado': '10.5 GB', # Esto requiere cálculo, lo dejamos estático por ahora
        }
        
        return render(request, self.template_name, context)

    template_name = 'backup_module\configuracion_respaldo.html'
    
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
        context['ejecutar_url'] = reverse_lazy('backup_module:backup_ejecutar')
        context['configurar_url'] = reverse_lazy('backup_module:backup_configurar')
        
        return context

    def get(self, request, *args, **kwargs):
        """Maneja la solicitud GET para mostrar la página."""
        context = self.get_context_data()
        return render(request, self.template_name, context)

# ------------------------------------------------------------------------------
# 2. VIEW PARA EJECUTAR RESPALDO MANUAL (Maneja el POST del Bloque Manual)
# ------------------------------------------------------------------------------

class EjecutarRespaldoManualView(SuperuserRequiredMixin, View):
    
    @method_decorator(csrf_exempt) # Si tu proyecto requiere csrf_exempt en POSTs
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # 1. Recoger datos del formulario (aunque el Comando de Gestión solo haga la DB)
        incluir_db = 'incluirDB' in request.POST
        # incluir_archivos = 'incluirArchivos' in request.POST
        # ubicacion = request.POST.get('ubicacion', 'local')

        if not incluir_db:
            messages.error(request, '❌ La opción de Base de Datos debe estar marcada para ejecutar el respaldo manual.')
            return redirect(reverse_lazy('backup_module:configuracion_respaldo'))

        try:
            # 💡 CLAVE: REEMPLAZO DE LA LÓGICA ASÍNCRONA DE CELERY 💡
            # Llamamos a la función que lanza el Comando de Gestión de forma asíncrona
            iniciar_respaldo_en_segundo_plano(request.user.pk)
            
            # NOTA: El registro del log 'En Proceso' ahora lo hace el comando backup_db.py

            messages.success(request, '✅ Respaldo manual **iniciado** correctamente. La tarea se está ejecutando en segundo plano, revisa el historial para ver el estado final.')
        
        except Exception as e:
            messages.error(request, f'❌ Error al intentar lanzar el proceso de respaldo: {e}')
        
        # Redirige a la URL principal del módulo de respaldo
        return redirect(reverse_lazy('backup_module:configuracion_respaldo'))

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

            # (Opcional) Aquí iría la lógica para configurar/actualizar el Programador de Tareas de Windows (manual).
            
            messages.success(request, f'💾 Configuración de respaldo automático guardada: {frecuencia} a las {hora}.')
        except Exception as e:
            messages.error(request, f'❌ Error al guardar la configuración: {e}')
            
        return redirect(reverse_lazy('backup_module:configuracion_respaldo'))


# ------------------------------------------------------------------------------
# 4. VIEW PARA DESCARGAR UN ARCHIVO DE RESPALDO
# ------------------------------------------------------------------------------

# views.py
from django.http import FileResponse, Http404
from django.conf import settings
# ... (asegúrate de que estas importaciones estén en la parte superior) ...

# ------------------------------------------------------------------------------
# 4. VIEW PARA DESCARGAR UN ARCHIVO DE RESPALDO
# ------------------------------------------------------------------------------

class DescargarRespaldoView(SuperuserRequiredMixin, View):
    
    def get(self, request, pk, *args, **kwargs):
        try:
            # log ahora usa la tabla correcta (gracias a models.py)
            log = get_object_or_404(BackupLog, pk=pk)
            ruta_completa = log.obtener_ruta_archivo() # Usa el método del modelo
            
            if not ruta_completa or not os.path.exists(ruta_completa):
                messages.error(request, f'❌ Error: El archivo físico no fue encontrado en la ruta registrada.')
                # Asegúrate de que el reverse_lazy usa el nombre correcto
                return redirect(reverse_lazy('backup_module:configuracion_respaldo')) 

            nombre_archivo = os.path.basename(ruta_completa)
            
            # 🛑 Implementación REAL de la descarga
            response = FileResponse(
                open(ruta_completa, 'rb'), 
                as_attachment=True, 
                filename=nombre_archivo
            )
            return response
            
        except Http404:
            messages.error(request, '❌ Error: El log de respaldo no se encuentra.')
            return redirect(reverse_lazy('backup_module:configuracion_respaldo')) 
            
        except Exception as e:
            messages.error(request, f'❌ Error al intentar descargar el respaldo: {e}')
            return redirect(reverse_lazy('backup_module:configuracion_respaldo'))
    
    def get(self, request, pk, *args, **kwargs):
        try:
            # 1. Obtener el registro de la base de datos
            log = get_object_or_404(BackupLog, pk=pk)
            
            # 2. Obtener la ruta física del archivo
            ruta_completa = log.obtener_ruta_archivo()
            
            if not ruta_completa:
                messages.error(request, '❌ Error: El log existe, pero el archivo no tiene ruta registrada.')
                return redirect(reverse_lazy('apy:configuracion_respaldo')) 

            # 3. Verificación de existencia del archivo
            if not os.path.exists(ruta_completa):
                messages.error(request, f'❌ Error: El archivo físico en la ruta {ruta_completa} no fue encontrado.')
                return redirect(reverse_lazy('apy:configuracion_respaldo')) 

            # 4. Obtener solo el nombre del archivo para la descarga
            nombre_archivo = os.path.basename(ruta_completa)
            
            # 5. Usar FileResponse para enviar el archivo
            # 'rb' (read binary) es necesario para archivos.
            response = FileResponse(
                open(ruta_completa, 'rb'), 
                as_attachment=True, 
                filename=nombre_archivo # Nombre que verá el usuario
            )
            return response
            
        except Http404:
            messages.error(request, '❌ Error: El log de respaldo no se encuentra.')
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
            
            messages.success(request, f'Preparando descarga del respaldo #{pk}...')
            
            # En un caso real, esto sería reemplazado por la lógica de FileResponse o StreamingHttpResponse
            return redirect(reverse_lazy('backup_module:configuracion_respaldo')) 
            
        except Http404:
            messages.error(request, '❌ Error: El archivo de respaldo no se encuentra o la ruta es inválida.')
            return redirect(reverse_lazy('backup_module:configuracion_respaldo')) 
        except Exception as e:
            messages.error(request, '❌ Error: El respaldo solicitado no está disponible o la ruta es incorrecta.')
            return redirect(reverse_lazy('backup_module:configuracion_respaldo'))