# backup_module/management/commands/restore_db.py

import os
import subprocess
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.db import connection 
from django.utils import timezone
from backup_module.models import BackupLog 
from pathlib import Path 

class Command(BaseCommand):
    help = 'Restaura una base de datos MySQL a partir de un archivo SQL usando el comando mysql.'

    def add_arguments(self, parser):
        # La ruta al archivo SQL que se va a restaurar (Obligatorio)
        parser.add_argument(
            '--path',
            type=str,
            required=True,
            help='Ruta absoluta al archivo .sql de respaldo para restaurar.'
        )
        # ID opcional del log 
        parser.add_argument(
            '--log_pk',
            type=int,
            default=None,
            help='ID del registro de BackupLog que se está restaurando (solo para referencia).'
        )

    def _get_db_config(self):
        """Extrae la configuración de la DB por defecto de settings.py."""
        db_settings = settings.DATABASES['default']
        if db_settings.get('ENGINE') != 'django.db.backends.mysql':
            raise CommandError("Este comando solo es compatible con el motor MySQL.")
            
        return {
            'NAME': db_settings.get('NAME'),
            'USER': db_settings.get('USER'),
            'PASSWORD': db_settings.get('PASSWORD', ''),
            'HOST': db_settings.get('HOST', 'localhost'),
            'PORT': db_settings.get('PORT', '3306'),
        }

    def handle(self, *args, **options):
        # 0. Inicializar variables para manejo de errores y logs
        log_pk = options['log_pk']
        log = None
        estado_final = 'Fallo' # Asumimos fallo por defecto
        error_msg = None
        
        # ----------------------------------------------------
        # 1. BLOQUE PRINCIPAL (try...except...finally)
        # Todo lo que pueda fallar debe ir aquí para que el finally lo maneje
        # ----------------------------------------------------
        try:
            # 1.1 OBTENER EL LOG
            if log_pk:
                try:
                    log = BackupLog.objects.get(pk=log_pk)
                except BackupLog.DoesNotExist:
                    raise CommandError(f"BackupLog con PK={log_pk} no encontrado.")
                
            # 1.2 OBTENER LA CONFIGURACIÓN DE LA BASE DE DATOS
            db_config = self._get_db_config()

            # 1.3 VERIFICAR RUTA DEL ARCHIVO
            backup_path = str(Path(options['path']).resolve())
            if not os.path.exists(backup_path):
                raise CommandError(f"El archivo de respaldo no se encontró en la ruta: {backup_path}")
            
            # 1.4 MARCAR EL LOG COMO EN PROCESO (BLOQUEO)
            # Esto debe ir después de obtener db_config, ya que aquí es donde falla la autenticación
            if log:
                log.estado = 'En Proceso'
                log.fecha_inicio = timezone.now()
                log.save() 
                self.stdout.write(self.style.NOTICE(f"Registro de log #{log.pk} bloqueado y en proceso."))
            
            # 1.5 PREPARAR EL COMANDO 'mysql'
            command = [
                'mysql',
                '--force', # CLAVE: Fuerza la ejecución y ayuda a reportar errores de sintaxis en stderr
                f'-h{db_config["HOST"]}',
                f'-P{db_config["PORT"]}',
                f'-u{db_config["USER"]}',
                f'{db_config["NAME"]}',
                '--default-character-set=utf8mb4'
            ]
            if db_config['PASSWORD']:
                command.append(f'-p{db_config["PASSWORD"]}')

            self.stdout.write(self.style.NOTICE(f"⚠️ Iniciando restauración desde: {os.path.basename(backup_path)}"))
            
            # 1.6 CERRAR CONEXIONES (CRÍTICO)
            connection.close() 
            self.stdout.write(self.style.WARNING("Conexión a la base de datos de Django cerrada temporalmente."))

            # 1.7 EJECUTAR EL COMANDO DE RESTAURACIÓN
            with open(backup_path, 'r', encoding='utf-8') as f:
                process = subprocess.run(
                    command,
                    stdin=f, 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE,
                    check=False
                )

            # 1.8 MANEJO DE RESULTADOS (DETECCIÓN DE FALLOS ROBUSTA)
            error_output = process.stderr.decode('utf-8', errors='ignore').strip() 
            stdout_output = process.stdout.decode('utf-8', errors='ignore').strip()
            
            # Búsqueda de errores por contenido (si returncode es 0)
            full_output = (stdout_output + error_output).upper()
            indicadores_de_fallo = ['ERROR', 'SYNTAX', 'ERROR 1064', 'UNKNOWN COLUMN', 'NO SUCH TABLE', 'ACCESS DENIED']
            es_fallo_sql = any(indicador in full_output for indicador in indicadores_de_fallo)

            # 1.9 DETERMINAR EL ESTADO FINAL
            if process.returncode != 0 or es_fallo_sql:
                
                estado_final = 'Fallo' 
                
                # Unificamos el mensaje de error para errores de código de retorno y errores de contenido
                error_msg = (
                    f"Fallo de restauración. Código de retorno: {process.returncode}.\n"
                    f"Salida de Error (stderr):\n{error_output}"
                )
                
                self.stderr.write(self.style.ERROR(error_msg))

            else:
                # Caso de Éxito Total o con Advertencias Menores
                if error_output:
                    estado_final = 'Éxito con advertencias'
                    error_msg = f"Restauración completada con éxito, pero con advertencias de MySQL: {error_output}"
                    self.stdout.write(self.style.WARNING(error_msg))
                else:
                    estado_final = 'Éxito'
                    error_msg = None
                    self.stdout.write(self.style.SUCCESS("✅ Restauración completada con éxito."))

        # ----------------------------------------------------
        # 2. MANEJO DE EXCEPCIONES DE PYTHON
        # ----------------------------------------------------
        except CommandError as e:
            # Captura errores de configuración, ruta no encontrada o que el motor no es MySQL
            error_msg = str(e)
            self.stderr.write(self.style.ERROR(f"Error de configuración: {error_msg}"))
            estado_final = 'Fallo' 

        except FileNotFoundError:
            # Captura si el binario 'mysql' no está en el PATH
            error_msg = "El ejecutable 'mysql' no se encontró. Asegúrate de que esté en el PATH del sistema."
            self.stderr.write(self.style.ERROR(error_msg))
            estado_final = 'Fallo'

        except Exception as e:
            # Captura cualquier otro error de Python, incluyendo fallo de log.save() por contraseña incorrecta
            error_msg = f"Error inesperado durante la restauración: {e}"
            self.stderr.write(self.style.ERROR(error_msg))
            estado_final = 'Fallo' 

        # ----------------------------------------------------
        # 3. FINALIZACIÓN (Bloque finally)
        # ----------------------------------------------------
        finally:
            if log:
                # Lógica del profesor: Si el resultado fue 'Fallo', lo marca como 'Éxito' para reutilizarlo.
                if estado_final == 'Fallo':
                    log.estado = 'fallo' 
                else:
                    log.estado = estado_final
                    
                log.fecha_fin = timezone.now()
                # ⭐️ CLAVE: Guardamos el mensaje de error/advertencia
                log.mensaje_error = error_msg 
                log.save()
                
            self.stdout.write(self.style.NOTICE("Proceso de restauración finalizado y estado del log actualizado."))