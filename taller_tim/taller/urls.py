from django.contrib import admin
from django.urls import path, include
from apy.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    # --------------urls Karol---------------
    #path('Modulo Administrador/', vista_administrador),
    #path('Modulo Informes/', vista_informes),
    #path('Modulo Pago Servicios/', vista_pago_servicios),
    #path('Modulo Proveedores/', vista_proveedores),
    #path('Modulo Pagos/', vista_pagos),
    #path('Modulo Factura/', FacTabla),
    # --------------urls erick---------------
    #path('Modulo gestion_mantenimiento/', vista_gestion_mantenimiento),
    #path('Modulo tipo_mantenimiento/', vista_tipo_mantenimiento),
    #path('Modulo herramientas/',   vista_herramientas),
    #path('Modulo repuestos/', vista_repuestos),
    path('Modulo insumos/', vista_insumos),
    path('apy/', include('apy.urls')),
]