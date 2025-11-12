# backup_module/urls.py

from django.urls import path
from . import views # Importa las vistas desde el mismo directorio

app_name = 'backup_module'
urlpatterns = [
    # 1. URL Principal: Muestra la interfaz del módulo de respaldo (GET)
    path('', views.RespaldoView.as_view(), name='configuracion_respaldo'), 
    
    # 2. URL de Acción: Ejecuta el proceso de respaldo manual (POST)
    path('ejecutar/', views.EjecutarRespaldoManualView.as_view(), name='backup_ejecutar'),
    
    # 3. URL de Acción: Guarda la configuración de respaldo automático (POST)
    path('configurar/', views.ConfigurarRespaldoAutomaticoView.as_view(), name='backup_configurar'),
    
    # 4. URL de Acción: Descarga un archivo de respaldo específico (GET)
    path('descargar/<int:pk>/', views.DescargarRespaldoView.as_view(), name='backup_descargar'),
]