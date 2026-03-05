import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponse
from django.conf import settings
from apy.forms import ContactoForm

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

def contact_informacion(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            # Si el formulario es válido, el captcha TAMBIÉN es válido
            nombre = form.cleaned_data['name']
            correo = form.cleaned_data['email']
            asunto = form.cleaned_data['subject']
            mensaje = form.cleaned_data['message']

            try:
                send_mail(
                    f"WEB T.I.M: {asunto}",
                    f"De: {nombre} ({correo})\n\nMensaje:\n{mensaje}",
                    settings.EMAIL_HOST_USER,
                    ['karoltalerolopez@gmail.com'],
                    fail_silently=False,
                )
                messages.success(request, "Tu mensaje ha sido enviado con éxito.")
                return redirect('apy:contact_informacion')
            except Exception as e:
                messages.error(request, "Error enviando el correo.")
        else:
            messages.error(request, "Por favor, verifica el captcha y los datos.")
    else:
        form = ContactoForm()

    return render(request, 'informacion/contact.html', {'form': form})