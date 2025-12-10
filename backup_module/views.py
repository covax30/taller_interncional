from django.shortcuts import render, redirect, get_object_or_404
# Asume que aquí tienes tus modelos de BackupLog y ConfiguracionRespaldo
from .models import BackupLog, ConfiguracionRespaldo 
from django.views import View
from django.http import FileResponse, Http404, JsonResponse # JsonResponse añadida por si la necesitas más tarde
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin
import os
import sys # Para obtener la ruta del intérprete Python
import subprocess # Para lanzar el proceso en segundo plano
from django.conf import settings
from django.template.loader import render_to_string
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import uuid
from django.utils import timezone
from django.views.generic.edit import DeleteView # Asegúrate de que DeleteView esté importada
# ------------------------------------------------------------------------------
# Se usa try-except para importar las constantes de Windows solo si están disponibles
try:
    from subprocess import CREATE_NEW_PROCESS_GROUP, DETACHED_PROCESS, CREATE_NO_WINDOW
except ImportError:
    # Esto pasará en sistemas Unix, donde no se necesitan estas constantes.
    pass
# ------------------------------------------------------------------------------
# ✅ FUNCIONES DE EJECUCIÓN ASÍNCRONA (Con la corrección de WinError 2)
# ------------------------------------------------------------------------------
def _lanzar_proceso_asincrono(command):
    """ 
    Función interna para manejar la lógica de Popen de forma segura. 
    INCLUYE LA CORRECCIÓN CRÍTICA PARA WinError 2.
    """
    
    popen_kwargs = {
        'stdout': subprocess.DEVNULL,  
        'stderr': subprocess.DEVNULL,
        'env': os.environ.copy() # Heredar el PATH del entorno virtual (crucial en Windows)
    }

    if sys.platform == "win32":
        flags = 0
        try:
            # Usar constantes de Windows para ejecutar el proceso en segundo plano
            from subprocess import CREATE_NEW_PROCESS_GROUP, DETACHED_PROCESS, CREATE_NO_WINDOW
            flags = CREATE_NEW_PROCESS_GROUP | DETACHED_PROCESS | CREATE_NO_WINDOW
        except ImportError:
            pass
            
        # 🚨 CORRECCIÓN CRÍTICA PARA WinError 2: 
        # Juntar la lista 'command' en un solo string y usar shell=True.
        command_string = " ".join(command) 
        
        subprocess.Popen(command_string, 
                         creationflags=flags, 
                         shell=True, # CLAVE
                         **popen_kwargs)
    
    else:
        # Fallback para sistemas Unix (Linux/Mac)
        subprocess.Popen(command, start_new_session=True, **popen_kwargs)
        
    return True


def iniciar_respaldo_en_segundo_plano(user_pk):
    """ Lanza el Comando 'backup_db' de forma asíncrona. """
    
    manage_py_path = os.path.join(settings.BASE_DIR, 'manage.py')
    
    if sys.platform == "win32":
        # Usar comillas es crucial en Windows si las rutas tienen espacios
        python_exec = f'"{sys.executable}"'
        manage_path = f'"{manage_py_path}"'
    else:
        python_exec = sys.executable
        manage_path = manage_py_path
    
    # El comando llama al manejador de respaldo con el ID del usuario
    command = [
        python_exec,
        manage_path,
        'backup_db',
        f'--user_id={user_pk}', 
    ]
    
    return _lanzar_proceso_asincrono(command)


def iniciar_restauracion_en_segundo_plano(ruta_archivo_sql, log_pk):
    """ 
    Lanza el Comando 'restore_db' de forma asíncrona. 
    Ahora incluye log_pk para que el comando pueda actualizar el estado en BD.
    """
    
    manage_py_path = os.path.join(settings.BASE_DIR, 'manage.py')
    
    if sys.platform == "win32":
        python_exec = f'"{sys.executable}"'
        manage_path = f'"{manage_py_path}"'
        # Usamos comillas dobles para toda la ruta SQL para evitar errores de espacios
        ruta_sql_arg = f'--path="{ruta_archivo_sql}"' 
    else:
        python_exec = sys.executable
        manage_path = manage_py_path
        ruta_sql_arg = f'--path={ruta_archivo_sql}'
        
    # El comando llama al manejador de restauración con la ruta del archivo SQL y el PK del log
    command = [
        python_exec,
        manage_path,
        'restore_db',
        ruta_sql_arg,
        f'--log_pk={log_pk}', # Iportante para actualizar el estado y error
    ]
    
    return _lanzar_proceso_asincrono(command)
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
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = {}
        context['entidad'] = 'Módulo de Respaldo'
        context['titulo'] = 'Configuración de Respaldo y Mantenimiento'
        
        # 1. Información de Último Respaldo
        logs = BackupLog.objects.all().order_by('-fecha_inicio')
        ultimo_backup = logs.filter(estado='Éxito').order_by('-fecha_fin').first()
        context['ultimo_backup_fecha'] = ultimo_backup.fecha_fin if ultimo_backup else None
        
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
        context['espacio_ocupado'] = "1.2 GB" # (Valor estático de ejemplo)

        # 4. Logs del historial (Para llenar la tabla en la parte inferior)
        context['historial_respaldos'] = logs[:20]
        
        # URLs necesarias para los POSTs
        context['ejecutar_url'] = reverse_lazy('backup_module:backup_ejecutar')
        context['configurar_url'] = reverse_lazy('backup_module:backup_configurar')
        
        return context

    def get(self, request, *args, **kwargs):
        """Maneja la solicitud GET para mostrar la página."""
        context = self.get_context_data()
        
        # Obtener todos los logs (para tu bucle principal)
        logs = BackupLog.objects.all().order_by('-fecha_inicio')
        context['logs'] = logs # Se usa logs para la tabla principal
        
        # Último backup exitoso (para el panel lateral)
        ultimo_backup = logs.filter(estado='Éxito').order_by('-fecha_fin').first()
        context['ultimo_backup_fecha'] = ultimo_backup.fecha_fin if ultimo_backup else None
        
        return render(request, self.template_name, context)
    # ⭐️ FUNCIÓN REQUERIDA: Limpia los logs atascados ⭐️
    def _limpiar_logs_en_proceso(self):
        """
        Busca logs de restauración que hayan estado en 'En Proceso' por más de N minutos 
        y los marca como 'Fallo' para que el usuario pueda reintentar.
        """
        # Define el tiempo de espera (15 minutos)
        timeout_threshold = timezone.now() - timezone.timedelta(minutes=15)
        
        # 1. Busca logs atascados
        logs_atascados = BackupLog.objects.filter(
            estado='En Proceso', 
            # Busca logs cuya fecha_inicio es anterior al umbral de tiempo límite
            fecha_inicio__lt=timeout_threshold 
        )
        
        # 2. Actualiza los logs
        if logs_atascados.exists():
            count = logs_atascados.count()
            
            # Usamos update() para eficiencia, marcando el log como Fallo.
            logs_atascados.update(
                estado='Fallo', 
                fecha_fin=timezone.now(),
                mensaje_error='El proceso de restauración excedió el tiempo límite (15 minutos) y fue revertido a Fallo por el sistema de limpieza automático.'
            )
            return count
        return 0


    def get(self, request, *args, **kwargs):
        """Maneja la solicitud GET para mostrar la página."""
        
        # ⭐️ LLAMADA CRÍTICA: Ejecuta la limpieza antes de cargar la página
        logs_limpiados = self._limpiar_logs_en_proceso()
        if logs_limpiados > 0:
            # Muestra un mensaje al administrador sobre los logs corregidos
            messages.warning(request, f'⚠️ Atención: Se detectaron y limpiaron **{logs_limpiados}** logs atascados en "En Proceso". Fueron marcados como Fallo por timeout.')
            
        context = self.get_context_data()
        
        # ... (resto del código get)
        logs = BackupLog.objects.all().order_by('-fecha_inicio')
        context['logs'] = logs # Se usa logs para la tabla principal
        
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
            # NOTA: En este punto, el comando backup_db DEBE crear un log en estado 'Pendiente'/'En Proceso'
            # y luego actualizarlo. Aquí solo lanzamos el proceso.
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
# 4. VIEW PARA DESCARGAR UN ARCHIVO DE RESPALDO
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
# 5. VIEW PARA RESTAURAR EL SISTEMA DESDE UN RESPALDO
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
            
            # 3. Lanzar el proceso de restauración en segundo plano (pasando el PK)
            # Pasamos el PK para que el comando 'restore_db' pueda actualizar el log
            lanzado = iniciar_restauracion_en_segundo_plano(ruta_completa_sql, log.pk)
            
            if lanzado:
                # El proceso se está ejecutando en el proceso secundario (restore_db.py)
                messages.warning(request, f'⚠️ **Restauración del sistema INICIADA** desde el respaldo #{pk}. El proceso se ejecuta en segundo plano y puede tardar unos minutos.')
            else:
                messages.error(request, '❌ Error crítico al lanzar el proceso de restauración.')
            
            return redirect(reverse_lazy('backup_module:configuracion_respaldo')) 
            
        except Http404:
            messages.error(request, '❌ Error: El log de respaldo no se encuentra.')
            return redirect(reverse_lazy('backup_module:configuracion_respaldo')) 
            
        except Exception as e:
            messages.error(request, f'❌ Error inesperado durante la restauración: {e}')
            return redirect(reverse_lazy('backup_module:configuracion_respaldo'))
        
# ------------------------------------------------------------------------------
# 6. VIEW PARA SUBIR UN RESPALDO EXTERNO (SOLO SUBIDA)
# ------------------------------------------------------------------------------
class SubirRespaldoExternoView(SuperuserRequiredMixin, View):
    
    def post(self, request, *args, **kwargs):
        archivo_respaldo = request.FILES.get('archivo_restauracion')
        
        if not archivo_respaldo:
            messages.error(request, '❌ Debe seleccionar un archivo SQL o GZ para subir.')
            return redirect(reverse_lazy('backup_module:configuracion_respaldo'))

        # Validar tipo de archivo
        if not archivo_respaldo.name.lower().endswith(('.sql', '.gz', '.zip')):
            messages.error(request, '❌ Formato de archivo no válido. Solo se permiten .sql, .gz o .zip.')
            return redirect(reverse_lazy('backup_module:configuracion_respaldo'))
        
        try:
            # 1. Preparar y guardar el archivo subido en el directorio de backups
            fs = FileSystemStorage(location=settings.BACKUP_ROOT)
            nombre_base = os.path.splitext(archivo_respaldo.name)[0]
            extension = os.path.splitext(archivo_respaldo.name)[1]
            nombre_final = f"EXTERNAL_{nombre_base}_{uuid.uuid4().hex[:6]}{extension}"
            
            filename = fs.save(nombre_final, archivo_respaldo)
            ruta_completa_sql = os.path.join(settings.BACKUP_ROOT, filename)
            
            # Calcular el tamaño
            tamaño_bytes = os.path.getsize(ruta_completa_sql)
            tamaño_mb = tamaño_bytes / (1024 * 1024)
            
            # 2. Crear el log en la BD (marcado como Éxito porque el archivo está listo)
            nuevo_log = BackupLog.objects.create(
                fecha_inicio=timezone.now(),
                fecha_fin=timezone.now(),
                tipo='Externo', # Tipo: Externo
                estado='Éxito', # Estado: Listo para restaurar
                ruta_archivo=ruta_completa_sql,
                usuario=request.user,
                tamaño_mb=tamaño_mb,
            )
            
            messages.success(request, f'✅ Archivo **{archivo_respaldo.name}** subido correctamente. Ya está disponible en el Historial (Log #{nuevo_log.pk}) para su restauración.')
            
        except Exception as e:
            messages.error(request, f'❌ Error al procesar o guardar el archivo: {e}')
        
        return redirect(reverse_lazy('backup_module:configuracion_respaldo'))
# ------------------------------------------------------------------------------
# 🚨 7. VISTA API PARA EL ESTADO DE LOS LOGS 🚨
# ------------------------------------------------------------------------------
class LogsEstadoAPIView(View):
    """
    Retorna los datos de los logs recientes para ser consumidos por AJAX.
    """
    # Nota: No necesitamos limpiar los logs aquí, ya que la RespaldoView lo hace.
    def get(self, request, *args, **kwargs):
        # Obtener los logs más recientes (ej. los últimos 50, o logs "En Proceso")
        logs_recientes = BackupLog.objects.all().order_by('-fecha_inicio')[:50]
        
        # Serializar los datos (convertir objetos de Django a JSON)
        # Solo necesitamos los campos clave para la tabla
        logs_data = []
        for log in logs_recientes:
            logs_data.append({
                'pk': log.pk,
                'fecha_inicio': timezone.localtime(log.fecha_inicio).strftime('%d/%m/%Y %H:%M'), # Formatear fecha
                'fecha_fin': timezone.localtime(log.fecha_fin).strftime('%H:%M') if log.fecha_fin else 'N/A',
                'tipo': log.get_tipo_display(),
                'estado': log.estado,
                'tamaño_mb': f"{log.tamaño_mb:.2f}" if log.tamaño_mb else 'N/A',
                'usuario': log.usuario.username if log.usuario else 'Sistema',
                'ruta_archivo': os.path.basename(log.ruta_archivo) if log.ruta_archivo else 'N/A',
                'mensaje_error': log.mensaje_error,
            })

        return JsonResponse({'logs': logs_data})
    
class EliminarRespaldoView(DeleteView):
    # Especifica el modelo a eliminar
    model = BackupLog 
    # Define a dónde redirigir después de una eliminación exitosa
    success_url = reverse_lazy('backup_module:configuracion_respaldo') 
    
    # Este método se usa para manejar la solicitud POST de eliminación
    def form_valid(self, form):
        # Aquí puedes agregar lógica adicional antes de eliminar, como eliminar el archivo físico
        try:
            # Lógica para eliminar el archivo del sistema de archivos si existe
            # if self.object.file_path and os.path.exists(self.object.file_path):
            #     os.remove(self.object.file_path)
            
            # Llamar al método delete para eliminar el registro de la base de datos
            response = super().form_valid(form)
            messages.success(self.request, "El respaldo ha sido eliminado exitosamente.")
            return response
            
        except Exception as e:
            messages.error(self.request, f"Ocurrió un error al intentar eliminar el respaldo: {e}")
            # Si hay un error, redirigir a la página principal
            return redirect(self.success_url)