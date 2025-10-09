from django.contrib import admin
from django.urls import path, include
from login.views import forgot_view# taller/urls.py
from django.contrib.auth import views as auth_views 
from apy.view.usuario.contraseña.views import PerfilPasswordChangeView 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', include(('login.urls', 'login'), namespace='login')),  # ✅ con namespace
    path('apy/', include(('apy.urls', 'apy'), namespace='apy')),          # idem, por claridad
    path('forgot/', forgot_view.as_view(), name="forgot"),
    
     # 1. Solicitar Email
    path('forgot/', auth_views.PasswordResetView.as_view(
        template_name='usuario/contraseña/recuperar_solicitar_email.html',
        email_template_name='usuario/contraseña/email_reset.html', # (Opcional) Plantilla del contenido del email
    ), name='password_reset'), 

    # 2. Correo enviado
    path('forgot/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='usuario/contraseña/recuperar_email_enviado.html'
    ), name='password_reset_done'),

    # 3. Restablecer contraseña (link del email)
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='usuario/contraseña/recuperar_confirmar_nueva.html'
    ), name='password_reset_confirm'),

    # 4. Finalizado
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='usuario/contraseña/recuperar_finalizado.html'
    ), name='password_reset_complete'),

    # --------------------------------------------------------------------------
    # B. CAMBIO DE CONTRASEÑA EN PERFIL (USUARIO LOGUEADO)
    # --------------------------------------------------------------------------
    path('auth/password_change/', PerfilPasswordChangeView.as_view(), name='password_change'),
    
    path('auth/', include('django.contrib.auth.urls')),  # Rutas de autenticación de Django (login, logout, password_change, etc.)
]
