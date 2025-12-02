# backup_module/management/commands/backup_db.py

import os
import subprocess
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model
from backup_module.models import BackupLog # Usamos tu modelo existente
import datetime
import time

User = get_user_model()

class Command(BaseCommand):
    help = 'Ejecuta un backup completo de la base de datos MySQL usando mysqldump.'

    def add_arguments(self, parser):
        # Acepta el ID del usuario que inició el backup (si es manual)
        parser.add_argument(
            '--user_id',
            type=int,
            help='ID del usuario que ejecuta el backup (para fines de registro).',
            default=None,
        )

    def _get_db_config(self):
        """Extrae la configuración de la DB por defecto de settings.py."""
        db_settings = settings.DATABASES['default']
        if db_settings.get('ENGINE') != 'django.db.backends.mysql':
            raise CommandError("Este comando solo es compatible con el motor MySQL.")
            
        return {
            'NAME': db_settings.get('NAME'),
            'USER': db_settings.get('USER'),
            'PASSWORD': db_settings.get('PASSWORD', ''), # Contraseña puede ser vacía
            'HOST': db_settings.get('HOST', '127.0.0.1'),
            'PORT': str(db_settings.get('PORT', '3306')),
        }

    def handle(self, *args, **options):
        db_config = None
        log_entry = None
        user_id = options['user_id']
        
        try:
            # 1. Obtener configuración de la DB
            db_config = self._get_db_config()
            db_name = db_config['NAME']
            
            # 2. Registrar inicio del Backup (Tipo Manual si tiene user_id, sino Automático)
            user = User.objects.filter(pk=user_id).first() if user_id else None
            
            log_entry = BackupLog.objects.create(
                tipo='Manual' if user else 'Automático',
                estado='En Proceso',
                usuario=user,
            )
            
            self.stdout.write(f"Iniciando backup de la base de datos '{db_name}'...")
            
            # 3. Generar nombre de archivo y ruta
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{db_name}_backup_{timestamp}.sql"
            backup_path = os.path.join(settings.BACKUP_ROOT, filename)
            
            # 4. Construir el comando mysqldump (SEGURO: usa lista de argumentos)
            command = [
                'mysqldump',
                f'--host={db_config["HOST"]}',
                f'--port={db_config["PORT"]}',
                f'--user={db_config["USER"]}',
                f'--password={db_config["PASSWORD"]}',
                '--default-character-set=utf8',
                '--single-transaction', # Para bases de datos con InnoDB
                db_name
            ]

            # 5. Ejecutar mysqldump y redirigir la salida
            with open(backup_path, 'w', encoding='utf-8') as f:
                process = subprocess.run(
                    command,
                    stdout=f, 
                    stderr=subprocess.PIPE, 
                    text=True,
                    check=False 
                )
            
            # 6. Manejo del resultado
            log_entry.fecha_fin = timezone.now()
            log_entry.ruta_archivo = backup_path

            if process.returncode == 0:
                # Éxito
                file_size = os.path.getsize(backup_path)
                log_entry.estado = 'Éxito'
                log_entry.tamaño_mb = round(file_size / (1024 * 1024), 2) # Bytes a MB
                log_entry.save()
                self.stdout.write(self.style.SUCCESS(f"Backup exitoso. Archivo: {filename} ({log_entry.tamaño_mb} MB)"))
            else:
                # Fallo de mysqldump (ej. credenciales, permisos)
                if os.path.exists(backup_path):
                    os.remove(backup_path) # Eliminar archivo incompleto
                error_output = process.stderr.strip()
                log_entry.estado = 'Fallo'
                log_entry.save()
                raise CommandError(f"Error al ejecutar mysqldump (código {process.returncode}): {error_output}")

        except CommandError as e:
            # Captura errores específicos del comando (DB engine, mysqldump error)
            if log_entry and log_entry.estado != 'Fallo':
                log_entry.estado = 'Fallo'
                log_entry.save()
            self.stderr.write(self.style.ERROR(str(e)))
        except FileNotFoundError:
            # mysqldump o mysql no está en el PATH
            error_msg = "El ejecutable 'mysqldump' no se encontró. Asegúrate de que esté en el PATH del sistema."
            if log_entry:
                log_entry.estado = 'Fallo'
                log_entry.save()
            self.stderr.write(self.style.ERROR(error_msg))
        except Exception as e:
            # Cualquier otro error inesperado (ej. permisos de escritura en BACKUP_ROOT)
            if log_entry:
                log_entry.estado = 'Fallo'
                log_entry.save()
            self.stderr.write(self.style.ERROR(f"Error inesperado durante el backup: {e}"))