# Archivo: login/urls.py
from django.urls import path, include 
from django.contrib.auth import views as auth_views 
from .views import Login_view, logout_redirect
from .forms import CustomPasswordResetForm

# Asegúrate de que esta importación sea correcta según la estructura de tu proyecto
from apy.view.usuario.contraseña.views import PerfilPasswordChangeView 

# ¡ESTA IMPORTACIÓN YA ESTÁ AQUÍ! Ahora solo falta el path.
from apy.view.usuario.datos.views import ActualizarPerfilImagenView

app_name = 'login'
urlpatterns = [

    path('', Login_view.as_view(), name="login"),
    path('logout/', logout_redirect.as_view(), name="logout"),
    
    # ----------------------------------------------------
    # FLUJO DE RESTABLECIMIENTO DE CONTRASEÑA (4 Pasos)
    # ----------------------------------------------------

    # 2. Correo enviado
    path('olvide-contrasena/enviado/', auth_views.PasswordResetDoneView.as_view(
        # ✅ RUTA SIMPLIFICADA
        template_name='recuperar_email_enviado.html'
    ), name='password_reset_done'),

    # 3. Restablecer contraseña (link del email)
    path('reseteo/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        # ✅ RUTA SIMPLIFICADA
        template_name='recuperar_confirmar_nueva.html',
        success_url='/reseteo/listo/',
    ), name='password_reset_confirm'),

    # 4. Finalizado
    path('reseteo/listo/', auth_views.PasswordResetCompleteView.as_view(
        # ✅ RUTA SIMPLIFICADA
        template_name='recuperar_finalizado.html'
    ), name='password_reset_complete'),
    
    # 1. Solicitar Email
    path('olvide-contrasena/', auth_views.PasswordResetView.as_view(
        template_name='recuperar_solicitar_email.html',
        email_template_name='email_reset.html', 
        subject_template_name='email_subject.txt', 
        success_url='/olvide-contrasena/enviado/',
        
        # 🚨 CAMBIO CLAVE: Usar la forma personalizada
        form_class=CustomPasswordResetForm 
        
    ), name='password_reset'),
    
    
    # ----------------------------------------------------
    # FLUJO DE CAMBIO DE CONTRASEÑA (Dentro de sesión)
    # ----------------------------------------------------

    # 1. Mostrar el formulario de cambio de contraseña (TU VISTA)
    path(
        'cambiar-contrasena/',
        PerfilPasswordChangeView.as_view(), # <-- Usa tu vista personalizada
        name='password_change'              # <-- login:password_change
    ),

    # 2. Página de éxito después del cambio
    path(
        'cambio-exitoso/',
        auth_views.PasswordChangeDoneView.as_view(template_name='login/password_change_done.html'), 
        name='password_change_done'         # <-- login:password_change_done
    ),
    
    # ----------------------------------------------------
    # FLUJO DE ACTUALIZACIÓN DE IMAGEN (SOLO IMAGEN)
    # ----------------------------------------------------
    path(
        'perfil/actualizar-imagen/',
        ActualizarPerfilImagenView.as_view(),
        name='actualizar_perfil_imagen' # <-- ¡ESTA ES LA RUTA FALTANTE QUE RESUELVE EL ERROR!
    ),
]