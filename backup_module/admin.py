from django.contrib import admin
from .models import ConfiguracionRespaldo, BackupLog
from django.utils.html import format_html # Para renderizar HTML en list_display
from django.urls import reverse # Para construir la URL de descarga

# ------------------------------------------------------------------
# Administración del Módulo de Respaldo
# ------------------------------------------------------------------

@admin.register(ConfiguracionRespaldo)
class ConfiguracionRespaldoAdmin(admin.ModelAdmin):
    # Campos que se muestran en la vista de lista
    list_display = ('frecuencia', 'hora_ejecucion')
    
    # 🚨 Detalle de usabilidad:
    # Como solo debe haber una configuración, limitamos la creación y eliminación.
    
    def has_add_permission(self, request):
        """Permite añadir solo si aún no existe un registro de configuración."""
        return not ConfiguracionRespaldo.objects.exists()

    def has_delete_permission(self, request, obj=None):
        """Previene la eliminación del único registro de configuración."""
        return False


@admin.register(BackupLog)
class BackupLogAdmin(admin.ModelAdmin):
    # Campos que se muestran en la lista
    list_display = (
        'id', 
        'fecha_inicio', 
        'tipo', 
        'estado', 
        'tamaño_mb', 
        'usuario', 
        'ruta_archivo_link' # Campo personalizado
    )
    
    # Filtros laterales para búsqueda rápida
    list_filter = ('estado', 'tipo', 'fecha_inicio')
    
    # Campos de solo lectura (la mayoría se llenan automáticamente al ejecutar el backup)
    readonly_fields = (
        'fecha_inicio', 
        'fecha_fin', 
        'tipo', 
        'estado', 
        'tamaño_mb', 
        'usuario', 
        'ruta_archivo'
    )
    
    # Orden por defecto (el más reciente primero)
    ordering = ('-fecha_inicio',)

    # Permite buscar por el ID, el tipo o la ruta
    search_fields = ('id', 'tipo', 'ruta_archivo')
    
    # ----------------------------------------------------
    # MÉTODO PERSONALIZADO PARA LA RUTA
    # ----------------------------------------------------
    
    @admin.display(description='Ruta / Enlace de Descarga')
    def ruta_archivo_link(self, obj):
        """Muestra la ruta y un enlace a la vista de descarga si está disponible."""
        if obj.ruta_archivo and obj.estado == 'Éxito':
            try:
                # Asume el nombre de URL de tu app 'backup_module' y el nombre de URL 'backup_descargar'
                # (Basado en el archivo urls.py que has mencionado en el contexto)
                download_url = reverse("backup_module:backup_descargar", args=[obj.pk])
                return format_html('<a href="{}" target="_blank">Descargar (PK: {})</a>', download_url, obj.pk)
            except:
                 # Si la URL no está configurada, solo muestra la ruta del archivo
                return format_html('<code>{}</code>', obj.ruta_archivo.split('/')[-1])
        elif obj.estado == 'Fallo':
            return "⛔ Fallo"
        elif obj.estado == 'En Proceso':
            return "⏳ En Proceso"
        return "-"
        
    # Deshabilita la opción de crear nuevos logs manualmente en el admin
    def has_add_permission(self, request):
        return False