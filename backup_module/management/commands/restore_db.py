# backup_module/management/commands/restore_db.py

import os
import subprocess
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.db import connection # Necesario para cerrar conexiones
from django.utils import timezone
from backup_module.models import BackupLog # Asume que BackupLog existe
from pathlib import Path # 💡 CORRECCIÓN 1: Importar Path para manejo robusto de rutas

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
        # ID opcional del log (aunque la restauración es crítica y no actualiza el log de forma activa)
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
        
        # 1. Intentar obtener el log y establecer el estado de inicio (BLOQUEO)
        if log_pk:
            try:
                log = BackupLog.objects.get(pk=log_pk)
                # Establecer el estado 'En Proceso' (Inicio del bloqueo)
                log.estado = 'En Proceso'
                log.fecha_inicio = timezone.now()
                log.save()
            except BackupLog.DoesNotExist:
                self.stderr.write(self.style.ERROR(f"BackupLog con PK={log_pk} no encontrado."))
                return # No podemos continuar sin el log
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Error al iniciar el log: {e}"))
                return # Error grave, no podemos continuar

        # --- PREPARACIÓN Y VERIFICACIÓN ---
        
        # 2. Obtener la configuración y verificar la ruta
        try:
            db_config = self._get_db_config()
        except CommandError as e:
            error_msg = str(e)
            estado_final = 'Fallo'
            if log: pass 
            else: return 
        
        # La lógica de verificación de ruta también debe estar dentro del try para que el finally la maneje si es un error
        backup_path = str(Path(options['path']).resolve())
        if not os.path.exists(backup_path):
            error_msg = f"El archivo de respaldo no se encontró en la ruta: {backup_path}"
            self.stderr.write(self.style.ERROR(error_msg))
            estado_final = 'Fallo'
            if log: pass 
            else: return 

        # 3. Preparar el comando 'mysql'
        command = [
            'mysql',
            f'-h{db_config["HOST"]}',
            f'-P{db_config["PORT"]}',
            f'-u{db_config["USER"]}',
            f'{db_config["NAME"]}',
            '--default-character-set=utf8mb4'
        ]
        if db_config['PASSWORD']:
            command.append(f'-p{db_config["PASSWORD"]}')

        self.stdout.write(self.style.NOTICE(f"⚠️ Iniciando restauración desde: {os.path.basename(backup_path)}"))
        
        # 4. Cerrar las conexiones existentes (CRÍTICO)
        connection.close() 
        self.stdout.write(self.style.WARNING("Conexión a la base de datos de Django cerrada temporalmente."))

        # --- EJECUCIÓN CON try...except...finally ---
        
        try:
            # ✅ LÓGICA CRÍTICA DENTRO DEL TRY
            with open(backup_path, 'r', encoding='utf-8') as f:
                
                process = subprocess.run(
                    command,
                    stdin=f, 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE,
                    check=False
                )

            # 5. Manejo de resultados
            if process.returncode == 0:
                self.stdout.write(self.style.SUCCESS(f"✅ Restauración exitosa."))
                estado_final = 'Éxito' 
            else:
                error_output = process.stderr.decode('utf-8').strip()
                self.stderr.write(self.style.ERROR(f"Error al ejecutar la restauración (código {process.returncode}): {error_output}"))
                error_msg = f"Error MySQL: {error_output}"
                estado_final = 'Fallo' 

        except FileNotFoundError:
            error_msg = "El ejecutable 'mysql' no se encontró. Asegúrate de que esté en el PATH del sistema."
            self.stderr.write(self.style.ERROR(error_msg))
            estado_final = 'Fallo'

        except Exception as e:
            # Captura cualquier otro error durante la ejecución (incluido CommandError si ocurre aquí)
            error_msg = f"Error inesperado durante la restauración: {e}"
            self.stderr.write(self.style.ERROR(error_msg))
            estado_final = 'Fallo' 

        # ----------------------------------------------------
        # 6. FINALIZACIÓN (Bloque finally)
        # ----------------------------------------------------
        finally:
            if log:
                # 💡 La clave de la solución de tu profesor:
                # Si el proceso falla, liberamos el bloqueo y lo marcamos como 'Éxito' para que sea reutilizable.
                if estado_final == 'Fallo':
                    log.estado = 'Éxito' # Vuelve a ser utilizable
                else:
                    log.estado = estado_final
                    
                log.fecha_fin = timezone.now()
                log.mensaje_error = error_msg # Se guarda el error_msg (si lo hay)
                log.save()
                
            self.stdout.write(self.style.NOTICE("Proceso de restauración finalizado y estado del log actualizado."))