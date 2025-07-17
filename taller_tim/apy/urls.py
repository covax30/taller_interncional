from django.urls import path

from .Views import *
from apy.Views.contenido.views import *
from apy.Views.fixed_sidebar import *
from apy.views import *
from apy.view.proveedor.view import *


app_name = 'apy'

urlpatterns = [
    # --------------urls Karol---------------

    path('Modulo_Factura/',  factura, name = 'contenido.factura'),
    path('Contactanos/',  contacto, name = 'contenido.contacto'),
    path('index/', index.as_view(), name = 'contenido.index'),
    #path('Modulo_Factura/',  factura, name = 'contenido.factura'),
    #path('Contactanos/',  contacto, name = 'contenido.contacto'),
    path('factura/listar/', FacturaListView.as_view() , name='factura_lista'),
    path('factura/agregar/', FacturaCreateView.as_view(), name='factura_crear'),
    path('factura/editar/<int:pk>/', FacturaUpdateView.as_view(), name='factura_editar'),
    path('factura/eliminar/<int:pk>/', FacturaDeleteView.as_view(), name='factura_eliminar'),
    path('Proveedor/listar/', ProveedorListView.as_view() , name='proveedor_lista'),
    path('Proveedor/agregar/', ProveedorCreateView.as_view() , name='proveedor_crear'),
    path('Proveedor/editar/<int:pk>/', ProveedorUpdateView.as_view() , name='proveedor_editar'),
    path('Proveedor/eliminar/<int:pk>/', ProveedorDeleteView.as_view() , name='proveedor_eliminar')
] 