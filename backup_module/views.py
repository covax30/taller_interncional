# views.py - ARCHIVO COMPLETO Y CORREGIDO

# Importaciones necesarias (basado en tus imports)
from django.shortcuts import render, redirect, get_object_or_404
# Asume que aquí tienes tus modelos de BackupLog y ConfiguracionRespaldo
from .models import BackupLog, ConfiguracionRespaldo 
from django.views import View
from django.http import FileResponse, Http404
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin

# ------------------------------------------------------------------------------
# ✅ IMPORTACIONES REQUERIDAS PARA EJECUCIÓN ASÍNCRONA NATIVA
# ------------------------------------------------------------------------------
from django.conf import settings
import os
import sys         # Para obtener la ruta del intérprete Python
import subprocess  # Para lanzar el proceso en segundo plano
# ------------------------------------------------------------------------------
# Se usa try-except para importar las constantes de Windows solo si están disponibles
try:
    from subprocess import CREATE_NEW_PROCESS_GROUP, DETACHED_PROCESS, CREATE_NO_WINDOW
except ImportError:
    # Esto pasará en sistemas Unix, donde no se necesitan estas constantes.
    pass
# ------------------------------------------------------------------------------
# ✅ FUNCIONES DE EJECUCIÓN ASÍNCRONA (Usan el Comando de Gestión)
# ------------------------------------------------------------------------------

def iniciar_respaldo_en_segundo_plano(user_id):
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
    if sys.platform == "win32":
        flags = 0
        try:
             # Usa las constantes si fueron importadas con éxito
            flags = CREATE_NEW_PROCESS_GROUP | DETACHED_PROCESS | CREATE_NO_WINDOW
        except NameError:
            pass # Si falló la importación, flags es 0
            
        subprocess.Popen(command, 
                         creationflags=flags, 
                         stdout=subprocess.DEVNULL,  
                         stderr=subprocess.DEVNULL)
    else:
        # Fallback para sistemas Unix (Linux/Mac)
        subprocess.Popen(command, start_new_session=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    return True # Indica que el proceso fue lanzado

def iniciar_restauracion_en_segundo_plano(ruta_archivo_sql):
    """
    Lanza el Comando de Gestión 'restore_db' de Django como un proceso secundario,
    pasando la ruta del archivo SQL para que el comando lo gestione de forma segura.
    """
    
    # 1. Rutas críticas
    manage_py_path = os.path.join(settings.BASE_DIR, 'manage.py')
    
    # 2. Comando a ejecutar (Llama a 'python manage.py restore_db --path <ruta>')
    command = [
        sys.executable,  # Ruta al intérprete Python activo (del entorno virtual)
        manage_py_path,
        'restore_db',        # Llama al Comando de Gestión de Django
        f'--path={ruta_archivo_sql}', # Le pasa la ruta. ¡El comando la abre!
    ]
    
    # 3. Lanzar el proceso (CLAVE EN WINDOWS)
    if sys.platform == "win32":
        flags = 0
        try:
            # Usa las constantes si fueron importadas con éxito
            flags = CREATE_NEW_PROCESS_GROUP | DETACHED_PROCESS | CREATE_NO_WINDOW
        except NameError:
            pass # Si falló la importación, flags es 0

        subprocess.Popen(command, 
                         creationflags=flags, 
                         stdout=subprocess.DEVNULL,  
                         stderr=subprocess.DEVNULL)
    
    else:
        # Fallback para sistemas Unix (Linux/Mac)
        subprocess.Popen(command, start_new_session=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    return True # Indica que el proceso fue lanzado

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
        return redirect(reverse_lazy('backup_module:configuracion_respaldo')) # Usa el nombre de tu URL principal

# ------------------------------------------------------------------------------
# 1. VIEW PRINCIPAL (Muestra el estado y los formularios)
# ------------------------------------------------------------------------------

class RespaldoView(SuperuserRequiredMixin, View):
    template_name = 'backup_module/configuracion_respaldo.html' # Ajusta la ruta a tu template

    def dispatch(self, request, *args, **kwargs):
        # Se mantiene la misma convención de tus vistas
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = {}
        context['entidad'] = 'Módulo de Respaldo'
        context['titulo'] = 'Configuración de Respaldo y Mantenimiento'
        
        # 1. Información de Último Respaldo
        try:
            context['ultimo_backup_fecha'] = BackupLog.objects.filter(estado='Éxito').latest('fecha_inicio').fecha_fin
        except:
            context['ultimo_backup_fecha'] = None

        # 2. Configuración Programada
        try:
            configuracion = ConfiguracionRespaldo.objects.get(pk=1) 
            context['frecuencia_actual'] = configuracion.frecuencia
            context['hora_actual'] = configuracion.hora_ejecucion
        except:
            context['frecuencia_actual'] = 'inactivo'
            context['hora_actual'] = '03:00'
        
        # 3. Métricas
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
        
        # Obtener todos los logs (para tu bucle principal)
        logs = BackupLog.objects.all().order_by('-fecha_inicio')
        context['logs'] = logs
        
        # Último backup exitoso (para el panel lateral)
        ultimo_backup = logs.filter(estado='Éxito').order_by('-fecha_fin').first()
        context['ultimo_backup_fecha'] = ultimo_backup.fecha_fin if ultimo_backup else None
        
        return render(request, self.template_name, context)

# ------------------------------------------------------------------------------
# 2. VIEW PARA EJECUTAR RESPALDO MANUAL (Maneja el POST del Bloque Manual)
# ------------------------------------------------------------------------------

class EjecutarRespaldoManualView(SuperuserRequiredMixin, View):
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # 1. Recoger datos del formulario
        incluir_db = 'incluirDB' in request.POST

        if not incluir_db:
            messages.error(request, '❌ La opción de Base de Datos debe estar marcada para ejecutar el respaldo manual.')
            return redirect(reverse_lazy('backup_module:configuracion_respaldo'))

        try:
            # Llamamos a la función que lanza el Comando de Gestión de forma asíncrona
            lanzado = iniciar_respaldo_en_segundo_plano(request.user.pk)
            
            if lanzado:
                messages.success(request, '✅ Respaldo manual **iniciado** correctamente. La tarea se está ejecutando en segundo plano, revisa el historial para ver el estado final.')
            else:
                messages.error(request, '❌ Error al lanzar el proceso de respaldo. Verifique la configuración del sistema.')
        
        except Exception as e:
            messages.error(request, f'❌ Error al intentar lanzar el proceso de respaldo: {e}')
        
        # Redirige a la URL principal del módulo de respaldo
        return redirect(reverse_lazy('backup_module:configuracion_respaldo'))

# ------------------------------------------------------------------------------
# 3. VIEW PARA CONFIGURAR RESPALDO AUTOMÁTICO (Maneja el POST del Bloque Programación)
# ------------------------------------------------------------------------------

class ConfigurarRespaldoAutomaticoView(SuperuserRequiredMixin, View):
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
        
    def post(self, request, *args, **kwargs):
        frecuencia = request.POST.get('frecuencia')
        hora = request.POST.get('hora')
        
        try:
            configuracion, created = ConfiguracionRespaldo.objects.get_or_create(pk=1)
            configuracion.frecuencia = frecuencia
            configuracion.hora_ejecucion = hora 
            configuracion.save()

            messages.success(request, f'💾 Configuración de respaldo automático guardada: {frecuencia} a las {hora}.')
        except Exception as e:
            messages.error(request, f'❌ Error al guardar la configuración: {e}')
            
        return redirect(reverse_lazy('backup_module:configuracion_respaldo'))


# ------------------------------------------------------------------------------
# 4. VIEW PARA DESCARGAR UN ARCHIVO DE RESPALDO (Ya funcionando)
# ------------------------------------------------------------------------------

class DescargarRespaldoView(SuperuserRequiredMixin, View):
    
    def get(self, request, pk, *args, **kwargs):
        try:
            # 1. Obtener el registro de la base de datos
            log = get_object_or_404(BackupLog, pk=pk)
            
            # 2. Obtener la ruta física del archivo (asumiendo que log.obtener_ruta_archivo() funciona)
            ruta_completa = log.obtener_ruta_archivo()
            
            if not ruta_completa:
                messages.error(request, '❌ Error: El log existe, pero el archivo no tiene ruta registrada.')
                return redirect(reverse_lazy('backup_module:configuracion_respaldo')) 

            # 3. Verificación de existencia del archivo
            if not os.path.exists(ruta_completa):
                messages.error(request, f'❌ Error: El archivo físico en la ruta {ruta_completa} no fue encontrado.')
                return redirect(reverse_lazy('backup_module:configuracion_respaldo')) 

            # 4. Obtener solo el nombre del archivo para la descarga
            nombre_archivo = os.path.basename(ruta_completa)
            
            # 5. Usar FileResponse para enviar el archivo
            response = FileResponse(
                open(ruta_completa, 'rb'), 
                as_attachment=True, 
                filename=nombre_archivo # Nombre que verá el usuario
            )
            return response
            
        except Http404:
            messages.error(request, '❌ Error: El log de respaldo no se encuentra.')
            return redirect(reverse_lazy('backup_module:configuracion_respaldo')) 
            
        except Exception as e:
            messages.error(request, f'❌ Error al intentar descargar el respaldo: {e}')
            return redirect(reverse_lazy('backup_module:configuracion_respaldo'))

# ------------------------------------------------------------------------------
# 5. VIEW PARA RESTAURAR EL SISTEMA DESDE UN RESPALDO (Nueva Vista)
# ------------------------------------------------------------------------------

class RestaurarSistemaView(SuperuserRequiredMixin, View):
    
    @method_decorator(csrf_exempt) # Para aceptar POST
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, pk, *args, **kwargs):
        """Maneja la solicitud POST para iniciar la restauración desde un BackupLog específico."""
        
        try:
            # 1. Obtener el registro de la base de datos
            log = get_object_or_404(BackupLog, pk=pk)
            
            # 2. Obtener la ruta física del archivo
            ruta_completa_sql = log.obtener_ruta_archivo()
            
            if not os.path.exists(ruta_completa_sql):
                messages.error(request, f'❌ Error: El archivo de respaldo SQL no fue encontrado en la ruta: {ruta_completa_sql}')
                return redirect(reverse_lazy('backup_module:configuracion_respaldo')) 
            
            # 3. Lanzar el proceso de restauración en segundo plano
            lanzado = iniciar_restauracion_en_segundo_plano(ruta_completa_sql)
            
            if lanzado:
                # El proceso se está ejecutando en el proceso secundario (restore_db.py)
                messages.warning(request, f'⚠️ **Restauración del sistema INICIADA** desde el respaldo #{pk}. El proceso se ejecuta en segundo plano y puede tardar unos minutos.')
            else:
                # Esto es un caso raro si iniciar_restauracion_en_segundo_plano está bien
                messages.error(request, '❌ Error crítico al lanzar el proceso de restauración.')
            
            return redirect(reverse_lazy('backup_module:configuracion_respaldo')) 
            
        except Http404:
            messages.error(request, '❌ Error: El log de respaldo no se encuentra.')
            return redirect(reverse_lazy('backup_module:configuracion_respaldo')) 
            
        except Exception as e:
            messages.error(request, f'❌ Error inesperado durante la restauración: {e}')
            return redirect(reverse_lazy('backup_module:configuracion_respaldo'))