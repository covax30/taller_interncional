from django.contrib import admin
<<<<<<< HEAD
from django.urls import path, include
=======
from django.urls import path,include
>>>>>>> 6ec60e580ab6391c459bb187681d04c60fd33c3b
from apy.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
<<<<<<< HEAD
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
=======
    path('apy/', include('apy.urls'))
>>>>>>> 6ec60e580ab6391c459bb187681d04c60fd33c3b
]