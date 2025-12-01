from django.urls import path
from apy.views import *
from apy.view.Contenidos.views import *
from apy.view.proveedor.view import *
from apy.view.Empleado.views import *
from apy.view.Gastos.views import *
from apy.view.Marca.views import *
from apy.view.Nomina.views import *
from apy.view.Caja.views import *
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
from apy.view.clientes.views import *
from apy.view.compras.views import *
from apy.view.vehiculos.views import *
from apy.view.entrada_vehiculos.views import *
from apy.view.salida_vehiculos.views import *
from apy.view.Estadisticas.views import *
from apy.view.main.main import Main

from apy.view.usuario.views import *  
from apy.view.usuario.contraseña.views import *  
from apy.view.permisos.views import *
from apy.view.registro_usuarios.views import *

app_name = 'apy'

urlpatterns = [
    # --------------urls Karol---------------
    #path('Modulo_Factura/',  factura, name = 'contenido.factura'),
    #path('Contactanos/',  contacto, name = 'contenido.contacto'),
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
    
    # --------------urls Usuario y permisos-------------- 
    path('perfil/', PerfilUsuarioUpdateView.as_view(), name='perfil_usuarios'),  
    path('auth/password_change/', PerfilPasswordChangeView.as_view(), name='password_change'),

    path('registro/lista/', RegistroUsuarioListView.as_view(), name='registro_usuario_lista'), 
    path('registro/crear/', RegistroUsuarioCreateView.as_view(), name='registro_usuario_crear'), 
    path('registro/editar/<int:pk>/', RegistroUpdateView.as_view(), name='registro_usuario_editar'), 
    path('registro/eliminar/<int:pk>/', RegistroDeleteView.as_view(), name='registro_usuario_eliminar'),
    
    path('permisos/', permisos_usuarios, name='permisos_usuarios'),  
  
  
  
  
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
    path('Pagos/eliminar/<int:pk>/', PagosDeleteView.as_view() , name='pagos_eliminar'),






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
    
    path('main/', Main.as_view(), name='main'),
    path('estadisticas/', estadisticas, name='estadisticas'),
    path('api/clientes/count/', api_contador_clientes, name='api_contador_clientes'),
    path('api/vehiculos/count/', api_contador_vehiculos, name='api_contador_vehiculos'),
    path('api/insumos/count/', api_contador_insumos, name='api_contador_insumos'),
    path('api/gastos/count/', api_contador_gastos, name='api_contador_gastos'),

 ]