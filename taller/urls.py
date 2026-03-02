from django.contrib import admin
from django.urls import path, include, reverse_lazy
from django.contrib.auth import views as auth_views 
from apy.view.usuario.datos.views import *

from apy.view.usuario.contraseña.views import PerfilPasswordChangeView, PerfilPasswordChangeDoneView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('login.urls', 'login'), namespace='login')), 
    path('apy/', include(('apy.urls', 'apy'), namespace='apy')), 
    path('backups/', include('backup_module.urls')), 
    
    # 1. Cambio de Contraseña (USANDO TU VISTA PERSONALIZADA)
    path(
        'cambiar-contraseña/', 
        PerfilPasswordChangeView.as_view(), 
        name='password_change'
    ),
    
    # 2. Éxito del Cambio de Contraseña (Vista con redirección/SweetAlert)
    path(
        'cambio-exitoso/', 
        PerfilPasswordChangeDoneView.as_view(), 
        name='password_change_done'
    ),
    
    path('ia/', include('ia_assistant.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)