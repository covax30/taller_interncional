from django.urls import path
from .views import *
from apy.view.Contenidos.views import *
from apy.view.gen_index.views import index

from apy.views import *
from apy.view.proveedor.view import *
from apy.view.administrador.views import *
from apy.view.informes.views import *
from apy.view.pago_servicios.views import *
from apy.view.pagos.views import *

from apy.view.gestion_mantenimiento.views import *
from apy.view.herramienta.views import *
from apy.view.tipo_mantenimiento.views import *
from apy.view.insumos.views import *
from apy.view.repuestos.views import *

app_name = 'apy'

urlpatterns = [
    # --------------urls Karol---------------
    #--------URL modulo factura----------------

    path('inicio/index/', index.as_view(), name='index'),
    
    path('factura/listar/', FacturaListView.as_view() , name='factura_lista'),
    path('factura/agregar/', FacturaCreateView.as_view(), name='factura_crear'),
    path('factura/editar/<int:pk>/', FacturaUpdateView.as_view(), name='factura_editar'),
    path('factura/eliminar/<int:pk>/', FacturaDeleteView.as_view(), name='factura_eliminar'),
    
    #--------URL modulo proveedor----------------
    path('Proveedor/listar/', ProveedorListView.as_view() , name='proveedor_lista'),
    path('Proveedor/agregar/', ProveedorCreateView.as_view() , name='proveedor_crear'),
    path('Proveedor/editar/<int:pk>/', ProveedorUpdateView.as_view() , name='proveedor_editar'),
    path('Proveedor/eliminar/<int:pk>/', ProveedorDeleteView.as_view() , name='proveedor_eliminar'),
    
    # --------------urls erick---------------
    
    path('mantenimiento/listar/', MantenimientoListView.as_view() , name='mantenimiento_lista'),
    path('mantenimiento/agregar/', MantenimientoCreateView.as_view() , name='mantenimiento_crear'),
    path('mantenimiento/editar/<int:pk>/', MantenimientoUpdateView.as_view() , name='mantenimiento_editar'),
    path('mantenimiento/eliminar/<int:pk>/', MantenimientoDeleteView.as_view() , name='mantenimiento_eliminar'),
    
    path('herramienta/listar/', HerramientaListView.as_view() , name='herramienta_lista'),
    path('herramienta/agregar/', HerramientaCreateView.as_view() , name='herramienta_crear'),
    path('herramienta/editar/<int:pk>/', HerramientaUpdateView.as_view() , name='herramienta_editar'),
    path('herramienta/eliminar/<int:pk>/', HerramientaDeleteView.as_view() , name='herramienta_eliminar'),
    
    path('tipo_mantenimiento/listar/', TipoMantenimientoListView.as_view() , name='tipo_mantenimiento_lista'),
    path('tipo_mantenimiento/agregar/', TipoMantenimientoCreateView.as_view() , name='tipo_mantenimiento_crear'),
    path('tipo_mantenimiento/editar/<int:pk>/', TipoMantenimientoUpdateView.as_view() , name='tipo_mantenimiento_editar'),
    path('tipo_mantenimiento/eliminar/<int:pk>/', TipoMantenimientoDeleteView.as_view() , name='tipo_mantenimiento_eliminar'),
    
    path('insumos/listar/', InsumoListView.as_view() , name='insumo_lista'),
    path('insumos/agregar/', InsumoCreateView.as_view() , name='insumo_crear'),
    path('insumos/editar/<int:pk>/', InsumoUpdateView.as_view() , name='insumo_editar'),
    path('insumos/eliminar/<int:pk>/', InsumoDeleteView.as_view() , name='insumo_eliminar'),
    
    path('repuestos/listar/', RepuestoListView.as_view() , name='repuesto_lista'),
    path('repuestos/agregar/', RepuestoCreateView.as_view() , name='repuesto_crear'),
    path('repuestos/editar/<int:pk>/', RepuestoUpdateView.as_view() , name='repuesto_editar'),
    path('repuestos/eliminar/<int:pk>/', RepuestoDeleteView.as_view() , name='repuesto_eliminar'),
    
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