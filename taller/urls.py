from django.contrib import admin
from django.urls import path, include
from login.views import forgot_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('login.urls', 'login'), namespace='login')),  # ✅ con namespace
    path('apy/', include(('apy.urls', 'apy'), namespace='apy')),          # idem, por claridad
    path('forgot/', forgot_view.as_view(), name="forgot"),
    
    path('auth/', include('django.contrib.auth.urls')),  # Rutas de autenticación de Django (login, logout, password_change, etc.)
]
