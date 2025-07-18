from django.urls import path
from .views import *
from apy.view.Contenidos.views import *
from apy.view.gen_index.views import index

from apy.views import *
from apy.view.proveedor.view import *

from apy.view.gestion_mantenimiento.views import *
from apy.view.herramienta.views import *
from apy.view.tipo_mantenimiento.views import *
from apy.view.insumos.views import *
from apy.view.repuestos.views import *

app_name = 'apy'

urlpatterns = [
    # --------------urls Karol---------------

    path('inicio/index/', index.as_view(), name='index'),
    
    path('factura/listar/', FacturaListView.as_view() , name='factura_lista'),
    path('factura/agregar/', FacturaCreateView.as_view(), name='factura_crear'),
    path('factura/editar/<int:pk>/', FacturaUpdateView.as_view(), name='factura_editar'),
    path('factura/eliminar/<int:pk>/', FacturaDeleteView.as_view(), name='factura_eliminar'),
    
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
    
] 