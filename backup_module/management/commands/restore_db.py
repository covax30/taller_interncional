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
        # 1. Obtener la configuración de la base de datos
        try:
            db_config = self._get_db_config()
        except CommandError as e:
            self.stderr.write(self.style.ERROR(str(e)))
            return

        # 2. Verificar la ruta del archivo
        # 💡 CORRECCIÓN 2: Normalizar y resolver la ruta para compatibilidad con Windows
        backup_path = str(Path(options['path']).resolve())
        
        if not os.path.exists(backup_path):
            raise CommandError(f"El archivo de respaldo no se encontró en la ruta: {backup_path}")
        
        # 3. Preparar el comando de restauración 'mysql'
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
        
        # 4. Cerrar las conexiones existentes a la DB (CRÍTICO)
        connection.close() 
        self.stdout.write(self.style.WARNING("Conexión a la base de datos de Django cerrada temporalmente."))

        # 5. Ejecutar la restauración
        try:
            # ✅ El comando de gestión abre y maneja el archivo SQL
            with open(backup_path, 'r', encoding='utf-8') as f:
                
                # Ejecutar el comando. stdin=f canaliza el contenido del archivo SQL a mysql.
                process = subprocess.run(
                    command,
                    stdin=f, 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE,
                    check=False # No lanza error si el código de retorno no es 0
                )

            # 6. Manejo de resultados
            if process.returncode == 0:
                self.stdout.write(self.style.SUCCESS(f"✅ Restauración exitosa."))
            else:
                error_output = process.stderr.decode('utf-8').strip()
                raise CommandError(f"Error al ejecutar la restauración (código {process.returncode}): {error_output}")

        except CommandError as e:
            self.stderr.write(self.style.ERROR(str(e)))
        except FileNotFoundError:
            error_msg = "El ejecutable 'mysql' no se encontró. Asegúrate de que esté en el PATH del sistema."
            self.stderr.write(self.style.ERROR(error_msg))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error inesperado durante la restauración: {e}"))