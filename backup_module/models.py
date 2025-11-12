from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone # Importación necesaria si usas timezone

# ------------------------------------------------------------------
# MÓDULOS DE RESPALDO (ConfiguracionRespaldo y BackupLog)
# ------------------------------------------------------------------

class ConfiguracionRespaldo(models.Model):
    # ... (Copia aquí el cuerpo de la clase ConfiguracionRespaldo)
    FRECUENCIA_OPCIONES = [
        ('diario', 'Diario'),
        ('semanal', 'Semanal'),
        ('mensual', 'Mensual'),
        ('inactivo', 'Desactivado'),
    ]

    frecuencia = models.CharField(
        max_length=10, 
        choices=FRECUENCIA_OPCIONES, 
        default='semanal',
        verbose_name="Frecuencia"
    )
    hora_ejecucion = models.TimeField(
        default='03:00:00', 
        verbose_name="Hora de Ejecución"
    )

    class Meta:
        # 🛑 Cambiar esto si antes era 'Configuración de Respaldo'
        db_table = 'backup_module_configuracionrespaldo' 
        verbose_name = 'Configuración de Respaldo'
        verbose_name_plural = 'Configuraciones de Respaldo'


class BackupLog(models.Model):
    # ... (Copia aquí el cuerpo de la clase BackupLog)
    TIPO_OPCIONES = [
        ('Manual', 'Manual'),
        ('Automático', 'Automático'),
    ]
    ESTADO_OPCIONES = [
        ('Éxito', 'Éxito'),
        ('Fallo', 'Fallo'),
        ('En Proceso', 'En Proceso'),
    ]
    
    fecha_inicio = models.DateTimeField(auto_now_add=True, verbose_name="Inicio")
    fecha_fin = models.DateTimeField(null=True, blank=True, verbose_name="Fin")
    tipo = models.CharField(max_length=10, choices=TIPO_OPCIONES)
    estado = models.CharField(max_length=10, choices=ESTADO_OPCIONES, default='En Proceso')
    tamaño_mb = models.FloatField(null=True, blank=True, verbose_name="Tamaño (MB)")
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Ejecutado por")
    ruta_archivo = models.CharField(max_length=255, null=True, blank=True, verbose_name="Ruta")
    
    def obtener_ruta_archivo(self):
        """Devuelve la ruta absoluta del archivo de respaldo."""
        # Asumimos que 'ruta_archivo' guarda la ruta absoluta, tal como se configuró en backup_db.py
        return self.ruta_archivo
    
    def __str__(self):
        return f"{self.get_tipo_display()} - {self.fecha_inicio.strftime('%Y-%m-%d %H:%M')}"
    
    class Meta:
        # 🛑 ESTO GARANTIZA QUE EL ORM BUSCA EN EL LUGAR CORRECTO 🛑
        db_table = 'backup_module_backuplog' 
        verbose_name = 'Registro de Respaldo'
        verbose_name_plural = 'Registros de Respaldos'