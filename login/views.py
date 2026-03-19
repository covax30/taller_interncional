from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView, RedirectView
from django.contrib.auth import logout
from django.conf import settings
from axes.models import AccessAttempt
from django.utils import timezone
from datetime import timedelta

class Login_view(LoginView):
    template_name = "login.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Iniciar sesion'
        return context

class logout_redirect(RedirectView):
    pattern_name = 'login:login' 
    
    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return super().dispatch(request, *args, **kwargs)

class CuentaBloqueadaView(TemplateView):
    template_name = 'lock_out.html'
    # Permitimos POST porque el bloqueo ocurre al enviar el formulario (POST)
    http_method_names = ['get', 'post', 'head']

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Obtener el tiempo de cooloff desde settings (por defecto 30 minutos si no está definido)
        cooloff = getattr(settings, 'AXES_COOLOFF_TIME', timedelta(minutes=30))
        
        # Asegurarnos de que sea un timedelta
        if not isinstance(cooloff, timedelta):
            try:
                cooloff = timedelta(minutes=int(cooloff))
            except (ValueError, TypeError):
                cooloff = timedelta(minutes=30)  # fallback seguro

        # Tiempo por defecto si no encontramos registro
        segundos_rest = int(cooloff.total_seconds())

        # Obtener IP del request (siempre disponible)
        ip = self.request.META.get('REMOTE_ADDR')

        # Username: intentamos obtenerlo de POST o GET (viene del formulario fallido)
        username = (
            self.request.POST.get('username') or 
            self.request.GET.get('username') or 
            ''
        )

        if ip:
            # Query base: solo por IP (más confiable en la mayoría de casos)
            qs = AccessAttempt.objects.filter(ip_address=ip).order_by('-attempt_time')
            
            # Si hay username, lo agregamos al filtro (opcional, pero útil si hay múltiples usuarios desde misma IP)
            if username:
                qs = qs.filter(username=username)
            
            # Tomamos el intento más reciente
            ultimo_intento = qs.first()

            if ultimo_intento:
                expiracion = ultimo_intento.attempt_time + cooloff
                tiempo_restante = expiracion - timezone.now()
                
                # Solo actualizamos si aún queda tiempo positivo
                if tiempo_restante.total_seconds() > 0:
                    segundos_rest = int(tiempo_restante.total_seconds())
                else:
                    segundos_rest = 0  # ya expiró

        # Agregamos al contexto
        context.update({
            'segundos_bloqueo': segundos_rest,
            'minutos_bloqueo': (segundos_rest // 60) + (1 if segundos_rest % 60 > 0 else 0),
        })

        return context

def axes_lockout_view(request, *args, **kwargs):
    response = CuentaBloqueadaView.as_view()(request, *args, **kwargs)
    if hasattr(response, 'render') and callable(response.render):
        response.render()
    return response