from django.urls import path
from apy.views import *
from apy.Views.contenido.views import *

app_name = 'apy'

urlpatterns = [
    # --------------urls Karol---------------
    path('Modulo_Factura/',  factura, name = 'contenido.factura'),
    path('Contactanos/',  contacto, name = 'contenido.contacto')
] 