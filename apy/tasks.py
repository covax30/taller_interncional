# apy/tasks.py
from celery import shared_task
from django.conf import settings
from django.utils import timezone
from apy.models import BackupLog, ConfiguracionRespaldo 
from django.db import connection

import os
import subprocess 
import shutil
import time
from datetime import datetime, timedelta

# --- TAREAS PRINCIPALES DEL MÓDULO DE RESPALDO ---

@shared_task
def ejecutar_respaldo_asincrono(log_id, incluir_db, incluir_archivos, ubicacion):
    """
    Tarea principal que ejecuta la lógica de copia de seguridad (DB y/o archivos)
    y actualiza el registro de log.
    """
    log = BackupLog.objects.get(pk=log_id)
    log.estado = 'En Proceso'
    log.save()
    
    # ⚠️ DIRECTORIO DONDE SE ALMACENARÁN TEMPORALMENTE LOS BACKUPS
    BACKUP_BASE_DIR = os.path.join(settings.MEDIA_ROOT, 'backups')
    os.makedirs(BACKUP_BASE_DIR, exist_ok=True)
    
    db_file_path = None
    media_zip_path = None
    archivo_final_nombre = None
    
    try:
        # -----------------------------------------------------------------
        # 1. RESPALDO DE BASE DE DATOS (Se asume SQLite por tu settings.py)
        # -----------------------------------------------------------------
        if incluir_db:
            # Si usas SQLite, la forma más sencilla es simplemente copiar el archivo.
            # Si usas Postgres o MySQL, usarías 'subprocess.run' con pg_dump o mysqldump.
            
            db_settings = settings.DATABASES['default']
            db_engine = db_settings['ENGINE']
            
            if 'sqlite3' in db_engine:
                # Copiar el archivo db.sqlite3
                db_source_path = db_settings['NAME']
                db_filename = f"db_dump_{log_id}_{timezone.now().strftime('%Y%m%d%H%M%S')}.sqlite3"
                db_file_path = os.path.join(BACKUP_BASE_DIR, db_filename)
                
                # Cierra las conexiones activas a la base de datos para asegurar una copia limpia
                connection.close()
                shutil.copy2(db_source_path, db_file_path)
                print(f"Base de datos SQLite copiada a: {db_file_path}")
                
            elif 'postgresql' in db_engine:
                 # Esta es solo la plantilla. Debes configurar bien las variables de entorno para la contraseña.
                 # Comando real: pg_dump -h HOST -U USER DATABASE_NAME > db_file_path
                 db_filename = f"db_dump_{log_id}_{timezone.now().strftime('%Y%m%d%H%M%S')}.sql"
                 db_file_path = os.path.join(BACKUP_BASE_DIR, db_filename)
                 # ... Lógica de subprocess para pg_dump ...
                 pass # Sustituir con la lógica real de pg_dump

        # -----------------------------------------------------------------
        # 2. COMPRESIÓN DE ARCHIVOS MEDIA
        # -----------------------------------------------------------------
        if incluir_archivos:
            # Comprime la carpeta MEDIA_ROOT. El resultado es media_temp_[ID].zip
            media_temp_base = os.path.join(BACKUP_BASE_DIR, f"media_temp_{log_id}")
            shutil.make_archive(media_temp_base, 'zip', root_dir=settings.MEDIA_ROOT, base_dir='.')
            media_zip_path = media_temp_base + '.zip'
            print(f"Archivos media comprimidos a: {media_zip_path}")
        
        # -----------------------------------------------------------------
        # 3. EMPAQUETADO FINAL (Si se generaron archivos)
        # -----------------------------------------------------------------
        
        # Lista de archivos generados para el paquete final
        files_to_zip = []
        if db_file_path and os.path.exists(db_file_path):
            files_to_zip.append(db_file_path)
        if media_zip_path and os.path.exists(media_zip_path):
            files_to_zip.append(media_zip_path)

        if not files_to_zip:
             raise Exception("No se seleccionó incluir DB ni Archivos, o no se pudieron generar.")

        # Crea un ZIP final que contiene el dump de DB y el zip de Media
        timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
        archivo_final_nombre = f"full_backup_{timestamp}.zip"
        archivo_final_path = os.path.join(BACKUP_BASE_DIR, archivo_final_nombre)
        
        with zipfile.ZipFile(archivo_final_path, 'w', zipfile.ZIP_DEFLATED) as final_zip:
            for file_path in files_to_zip:
                # Añade el archivo al zip, usando solo el nombre del archivo como nombre interno
                final_zip.write(file_path, os.path.basename(file_path))
        
        # -----------------------------------------------------------------
        # 4. LIMPIEZA Y ACTUALIZACIÓN DEL LOG
        # -----------------------------------------------------------------
        
        # Limpia los archivos temporales (dump de DB y zip de media)
        if db_file_path and os.path.exists(db_file_path):
            os.remove(db_file_path)
        if media_zip_path and os.path.exists(media_zip_path):
            os.remove(media_zip_path)
            
        # Actualiza el registro de Log
        log.fecha_fin = timezone.now()
        log.estado = 'Éxito'
        log.ruta_archivo = archivo_final_nombre
        log.tamaño_mb = os.path.getsize(archivo_final_path) / (1024 * 1024)
        log.save()
        
        # Aquí iría la lógica opcional para subir a la nube (S3, Drive, etc.) si 'ubicacion' lo indica

    except Exception as e:
        # Manejo de errores
        log.fecha_fin = timezone.now()
        log.estado = 'Fallo'
        log.detalles = f"Error al ejecutar el respaldo: {e}"
        log.save()
        # Se recomienda enviar una notificación de fallo por correo

# --- TAREA PARA EL SCHEDULER AUTOMÁTICO (CELERY BEAT) ---

# Se usa un intervalo bajo para verificar la programación a menudo
@shared_task(name='apy.check_scheduled_backup')
def revisar_configuracion_programada():
    """
    Tarea que se ejecuta periódicamente (ej. cada minuto) y verifica
    si se debe iniciar un respaldo automático basado en ConfiguracionRespaldo.
    """
    try:
        config = ConfiguracionRespaldo.objects.get(pk=1) # Asume que solo hay una fila de configuración
    except ConfiguracionRespaldo.DoesNotExist:
        return # No hay configuración de respaldo automático

    if not config.activar_respaldo_automatico:
        return

    now = timezone.now()
    program_time_str = config.hora_programada.strftime('%H:%M')
    current_time_str = now.strftime('%H:%M')

    # 1. Verificar la Hora
    if program_time_str == current_time_str:
        # La hora coincide. Ahora verificamos la frecuencia
        last_log = BackupLog.objects.filter(tipo='Automático', estado='Éxito').order_by('-fecha_fin').first()
        
        should_run = False
        if config.frecuencia == 'Diaria':
            # Correrá si el último respaldo fue antes de hoy.
            if not last_log or last_log.fecha_fin < now.date():
                should_run = True
        
        elif config.frecuencia == 'Semanal':
            # Correrá si el último respaldo fue hace más de 6 días (7 días totales)
            if not last_log or last_log.fecha_fin < now - timedelta(days=6):
                should_run = True

        elif config.frecuencia == 'Mensual':
            # Correrá si el último respaldo fue el mes pasado
            if not last_log or last_log.fecha_fin.month != now.month:
                should_run = True
        
        if should_run:
            # 2. Crear el Log e iniciar la tarea
            log = BackupLog.objects.create(
                tipo='Automático',
                estado='En Proceso',
                usuario=None, # Nadie lo ejecuta, es el sistema
            )
            
            # 3. Llamar a la tarea de ejecución asíncrona
            ejecutar_respaldo_asincrono.delay(
                log.pk, 
                config.incluir_base_datos, 
                config.incluir_archivos_media, 
                config.ubicacion
            )
            print(f"Respaldo automático iniciado para Log ID: {log.pk}")