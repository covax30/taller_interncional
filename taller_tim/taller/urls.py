from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('apy/', include('apy.urls')),  # todas las rutas de tu app "apy"
    path('login/', include('login.urls')),  # todas las rutas de tu app "login"
]

