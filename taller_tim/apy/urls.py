from django.urls import path
from apy.views import *
from apy.view.Contenidos.views import *
from apy.view.proveedor.view import *
from apy.view.Empleado.views import *
from apy.view.Gastos.views import *
from apy.view.Marca.views import *
from apy.view.Nomina.views import *
from apy.view.Caja.views import *

app_name = 'apy'

urlpatterns = [
    # --------------urls Karol---------------
    #path('Modulo_Factura/',  factura, name = 'contenido.factura'),
    #path('Contactanos/',  contacto, name = 'contenido.contacto'),
    path('factura/listar/', FacturaListView.as_view() , name='factura_lista'),
    path('factura/agregar/', FacturaCreateView.as_view(), name='factura_crear'),
    path('factura/editar/<int:pk>/', FacturaUpdateView.as_view(), name='factura_editar'),
    path('factura/eliminar/<int:pk>/', FacturaDeleteView.as_view(), name='factura_eliminar'),
    path('Proveedor/listar/', ProveedorListView.as_view() , name='proveedor_lista'),
    path('Proveedor/agregar/', ProveedorCreateView.as_view() , name='proveedor_crear'),
    path('Proveedor/editar/<int:pk>/', ProveedorUpdateView.as_view() , name='proveedor_editar'),
    path('Proveedor/eliminar/<int:pk>/', ProveedorDeleteView.as_view() , name='proveedor_eliminar'),
    
    #--------------urls Yury
    #----------url Empleado -------
       
    path('empleado/listar/', EmpleadoListView.as_view() , name='empleado_lista'),
    path('empleado/agregar/', EmpleadoCreateView.as_view(), name='empleado_crear'),
    path('empleado/editar/<int:pk>/', EmpleadoUpdateView.as_view(), name='empleado_editar'),
    path('empleado/eliminar/<int:pk>/', EmpleadoDeleteView.as_view(), name='empleado_eliminar'),
    #----------url Gastos-------
    path('gasto/listar/', GastosListView.as_view() , name='gasto_lista'),
    path('gasto/agregar/', GastosCreateView.as_view(), name='gasto_crear'),
    path('gasto/editar/<int:pk>/', GastosUpdateView.as_view(), name='gasto_editar'),
    path('gasto/eliminar/<int:pk>/', GastosDeleteView.as_view(), name='gasto_eliminar'),
    #----------url Marca-------
    path('marca/listar/', MarcaListView.as_view() , name='marca_lista'),
    path('marca/agregar/',     MarcaCreateView.as_view(), name='marca_crear'),
    path('marca/editar/<int:pk>/',   MarcaUpdateView.as_view(), name='marca_editar'),
    path('marca/eliminar/<int:pk>/', MarcaDeleteView.as_view(), name='marca_eliminar'),
    
    #----------url Nomina-------
    path('nomina/listar/', NominaListView.as_view() , name='nomina_lista'),
    path('nomina/agregar/', NominaCreateView.as_view(), name='nomina_crear'),
    path('nomina/editar/<int:pk>/', NominaUpdateView.as_view(), name='nomina_editar'),
    path('nomina/eliminar/<int:pk>/', NominaDeleteView.as_view(), name='nomina_eliminar'),  
    
    #-------------urls Caja---------------
     path('caja/listar/', CajaListView.as_view() , name='caja_lista'),
    path('caja/agregar/', CajaCreateView.as_view(), name='caja_crear'),
    path('caja/editar/<int:pk>/', CajaUpdateView.as_view(), name='caja_editar'),
    path('caja/eliminar/<int:pk>/', CajaDeleteView.as_view(), name='caja_eliminar'),  
] 