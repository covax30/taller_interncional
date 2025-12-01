from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views 
from apy.view.usuario.contraseña.views import PerfilPasswordChangeView 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('login.urls', 'login'), namespace='login')),  # ✅ con namespace
    path('apy/', include(('apy.urls', 'apy'), namespace='apy')),          # idem, por claridad
    path('', include('django.contrib.auth.urls')),  
]
