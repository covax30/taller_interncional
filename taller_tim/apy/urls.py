from django.urls import path
from .Views import *
from apy.Views.contenido.views import *
from apy.Views.fixed_sidebar import *

app_name = 'apy'

urlpatterns = [
    # --------------urls Karol---------------
    path('Modulo_Factura/',  factura, name = 'contenido.factura'),
    path('Contactanos/',  contacto, name = 'contenido.contacto'),
    path('index/', index.as_view(), name = 'contenido.index'),
] 