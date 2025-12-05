from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views 
from apy.view.usuario.contraseña.views import PerfilPasswordChangeView 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('login.urls', 'login'), namespace='login')),  # ✅ con namespace
    path('apy/', include(('apy.urls', 'apy'), namespace='apy')),          # idem, por claridad
    path('backups/', include('backup_module.urls')), # Ruta de acceso: /backups/
]

if settings.DEBUG:
    # Esto es crucial para que Django sirva tus archivos de media (fotos de perfil)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # También puedes añadir static files (aunque staticfiles_dirs suele encargarse)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)