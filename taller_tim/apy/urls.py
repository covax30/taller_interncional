from django.urls import path
from .views import *
from apy.view.gen_index.views import index
from apy.view.Contenidos.views import *
from apy.views import *

from apy.view.proveedor.view import *
from apy.view.administrador.views import *
from apy.view.informes.views import *
from apy.view.pago_servicios.views import *
from apy.view.pagos.views import *

from apy.view.clientes.views import *
from apy.view.compras.views import *
from apy.view.vehiculos.views import *
from apy.view.entrada_vehiculos.views import *
from apy.view.salida_vehiculos.views import *


app_name = 'apy'

urlpatterns = [
    # --------------urls Karol---------------
    #--------URL modulo factura----------------

    path('inicio/index/', index.as_view(), name='index'),
    path('factura/listar/', FacturaListView.as_view() , name='factura_lista'),
    path('factura/agregar/', FacturaCreateView.as_view(), name='factura_crear'),
    path('factura/editar/<int:pk>/', FacturaUpdateView.as_view(), name='factura_editar'),
    path('factura/eliminar/<int:pk>/', FacturaDeleteView.as_view(), name='factura_eliminar'),
    
    # -------------URL modulo proveedor---------------
    path('Proveedor/listar/', ProveedorListView.as_view(), name='proveedor_lista'),
    path('Proveedor/agregar/', ProveedorCreateView.as_view(), name='proveedor_crear'),
    path('Proveedor/editar/<int:pk>/', ProveedorUpdateView.as_view(), name='proveedor_editar'),
    path('Proveedor/eliminar/<int:pk>/', ProveedorDeleteView.as_view(), name='proveedor_eliminar'),

    # -------------urls Steven--------------
    path('cliente/listar/', ClienteListView.as_view(), name='cliente_lista'),
    path('cliente/agregar/', ClienteCreateView.as_view(), name='cliente_crear'),
    path('cliente/editar/<int:pk>/', ClienteUpdateView.as_view(), name='cliente_editar'),
    path('cliente/eliminar/<int:pk>/', ClienteDeleteView.as_view(), name='cliente_eliminar'),

    path('compra/listar/', CompraListView.as_view(), name='compra_lista'),
    path('compra/agregar/', CompraCreateView.as_view(), name='compra_crear'),
    path('compra/editar/<int:pk>/', CompraUpdateView.as_view(), name='compra_editar'),
    path('compra/eliminar/<int:pk>/', CompraDeleteView.as_view(), name='compra_eliminar'),


    path('vehiculo/listar/', VehiculoListView.as_view(), name='vehiculo_lista'),
    path('vehiculo/agregar/', VehiculoCreateView.as_view(), name='vehiculo_crear'),
    path('vehiculo/editar/<int:pk>/', VehiculoUpdateView.as_view(), name='vehiculo_editar'),
    path('vehiculo/eliminar/<int:pk>/', VehiculoDeleteView.as_view(), name='vehiculo_eliminar'),
    
    path('entrada_vehiculo/listar/', EntradaVehiculoListView.as_view(), name='entrada_vehiculo_lista'),
    path('entrada_vehiculo/agregar/', EntradaVehiculoCreateView.as_view(), name='entrada_vehiculo_crear'),
    path('entrada_vehiculo/editar/<int:pk>/', EntradaVehiculoUpdateView.as_view(), name='entrada_vehiculo_editar'),
    path('entrada_vehiculo/eliminar/<int:pk>/', EntradaVehiculoDeleteView.as_view(), name='entrada_vehiculo_eliminar'),
    
    path('salida_vehiculo/listar/', SalidaVehiculoListView.as_view(), name='salida_vehiculo_lista'),
    path('salida_vehiculo/agregar/', SalidaVehiculoCreateView.as_view(), name='salida_vehiculo_crear'),
    path('salida_vehiculo/editar/<int:pk>/', SalidaVehiculoUpdateView.as_view(), name='salida_vehiculo_editar'),
    path('salida_vehiculo/eliminar/<int:pk>/', SalidaVehiculoDeleteView.as_view(), name='salida_vehiculo_eliminar'),    
    
    #--------URL modulo administrador----------------
    path('administrador/listar/', AdministradorListView.as_view() , name='administrador_lista'),
    path('administrador/agregar/', AdministradorCreateView.as_view() , name='administrador_crear'),
    path('administrador/editar/<int:pk>/', AdministradorUpdateView.as_view() , name='administrador_editar'),
    path('administrador/eliminar/<int:pk>/', AdministradorDeleteView.as_view() , name='administrador_eliminar'),
    
    #--------URL modulo informes----------------
    path('informes/listar/', InformesListView.as_view() , name='informes_lista'),
    path('informes/agregar/', InformesCreateView.as_view() , name='informes_crear'),
    path('informes/editar/<int:pk>/', InformesUpdateView.as_view() , name='informes_editar'),
    path('informes/eliminar/<int:pk>/', InformesDeleteView.as_view() , name='informes_eliminar'),
    
    #--------URL modulo pago de sercicios publicos----------------
    path('PagoServicios/listar/', PagoServiciosListView.as_view() , name='pago_servicios_lista'),
    path('PagoServicios/agregar/', PagoServiciosCreateView.as_view() , name='pago_servicios_crear'),
    path('PagoServicios/editar/<int:pk>/', PagoServiciosUpdateView.as_view() , name='pago_servicios_editar'),
    path('PagoServicios/eliminar/<int:pk>/', PagoServiciosDeleteView.as_view() , name='pago_servicios_eliminar'),
    
    #--------URL modulo pagos----------------
    path('Pagos/listar/', PagosListView.as_view() , name='pagos_lista'),
    path('Pagos/agregar/', PagosCreateView.as_view() , name='pagos_crear'),
    path('Pagos/editar/<int:pk>/', PagosUpdateView.as_view() , name='pagos_editar'),
    path('Pagos/eliminar/<int:pk>/', PagosDeleteView.as_view() , name='pagos_eliminar')
    
] 