import requests
from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpResponse
from django.conf import settings

def index_informacion(request):
    return render(request, 'informacion/index.html')

def about_informacion(request):
    return render(request, 'informacion/about.html')

def contact_informacion(request):
    return render(request, 'informacion/contact.html')

def service_informacion(request):
    return render(request, 'informacion/service-details.html')

def terms_informacion(request):
    return render(request, 'informacion/terms.html')

def contacto_formulario(request):
    if request.method == 'POST':
        # 1. Capturar el token del captcha y los datos del formulario
        recaptcha_response = request.POST.get('g-recaptcha-response')
        nombre = request.POST.get('name')
        correo_cliente = request.POST.get('email')
        asunto_cliente = request.POST.get('subject')
        mensaje_cliente = request.POST.get('message')

        # 2. Validar con Google
        data = {
            'secret': settings.RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        
        try:
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = r.json()

            # 3. Si el captcha es exitoso (puntaje >= 0.5)
            # Cambia 0.5 por 0.1 temporalmente
            if result.get('success') and result.get('score', 0) >= 0.1:
                
                # Enviamos el correo 
                send_mail(
                    f"WEB T.I.M: {asunto_cliente}",
                    f"De: {nombre} ({correo_cliente})\n\nMensaje:\n{mensaje_cliente}",
                    settings.EMAIL_HOST_USER,
                    ['soportecnico.t.i.m@gmail.com'], # Tu correo donde recibes
                    fail_silently=False,
                )
                
                # Importante: Retornar OK para que la plantilla muestre el mensaje verde
                return HttpResponse("OK")
            
            else:
                # Si Google dice que es un robot
                return HttpResponse("Error: Validación de seguridad fallida. Inténtalo de nuevo.", status=400)
                
        except Exception as e:
            return HttpResponse(f"Error en el servidor: {str(e)}", status=500)

    # Si la petición es GET (entrar a la página), enviamos la Site Key al HTML
    return render(request, 'informacion/contact.html', {
        'RECAPTCHA_SITE_KEY': settings.RECAPTCHA_SITE_KEY
    })