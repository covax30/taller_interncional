from django.urls import path
from apy.context_processors import api_stock_bajo
from apy.view.Nomina.views import NominaCreateModalView, NominaCreateView, NominaDeleteView, NominaListView, NominaUpdateView
from apy.view.empresa.views import *
from apy.view.usuario.datos.views import ActualizarPerfilImagenView, PerfilEditarView
from apy.views import *
from apy.view.proveedor.view import *
from apy.view.Gastos.views import *
from apy.view.Marca.views import *
from apy.view.Caja.views import *
from login import views
from .views import *
from apy.view.gen_index.views import index

from apy.views import *

from apy.view.proveedor.view import *
from apy.view.informes.views import *
from apy.view.pago_servicios.views import *
from apy.view.pagos.views import *

from apy.view.herramienta.views import *
from apy.view.tipo_mantenimiento.views import *
from apy.view.insumos.views import *
from apy.view.repuestos.views import *
from apy.view.clientes.views import *
from apy.view.vehiculos.views import *
from apy.view.entrada_vehiculos.views import *
from apy.view.salida_vehiculos.views import *
from apy.view.Estadisticas.views import *
from apy.view.detalle_servicio.views import *
from apy.view.main.main import Main

from apy.view.usuario.views import * 
from apy.view.usuario.detalles.views import *
from apy.view.usuario.contraseña.views import *  
from apy.view.permisos.views import *
from apy.view.registro_usuarios.views import *

from apy.view.ayuda.views import *
from apy.view.buscador.views import *
from apy.view.informacion.views import *

app_name = 'apy'

urlpatterns = [
    # ------Url pagina informacion----------------
    path('bienvenido/', index_informacion, name='index_informacion'),
    path('nosotros/', about_informacion, name='about_informacion'),
    path('contacto/', contact_informacion, name='contact_informacion'),
    path('servicios_informacion/', service_informacion, name='service_informacion'),
    path('terminos/', terms_informacion, name='terms_informacion'), 
    path('contacto/formulario/', contact_informacion, name='contacto_formulario'),

    path('inicio/index/', index.as_view(), name='index'),
    
    path('buscar/', buscador_global, name='buscador_global'),
    
    # ------Url modulo detalle servicio----------------
    path('servicios/', ListServicioView.as_view(), name='lista_servicios'),  
    path('servicios/crear/', CreateServicioView.as_view(), name='crear_servicio'),
    path('servicios/editar/<int:pk>/', UpdateServicioView.as_view(), name='editar_servicio'),
    path('servicios/eliminar/<int:pk>/', DeleteServicioView.as_view(), name='eliminar_servicio'),
    path('servicios/detalle/<int:pk>/', DetalleServicioView.as_view(), name='detalle_servicio'),
    path('servicios/inactivos/', ServicioInactivosListView.as_view(), name='servicios_inactivos'),  
    path('servicios/activar/<int:pk>/', ServicioActivateView.as_view(), name='servicio_activar'),
    path('servicios/modal/crear/', DetalleCreateModalView.as_view(), name='servicio_modal_crear'),
    path('servicios/imprimir/<int:pk>/', imprimir_servicio_factura, name='imprimir_servicio'),
    
    # -------------URL modulo proveedor---------------
    path('Proveedor/listar/', ProveedorListView.as_view(), name='proveedor_lista'),
    path('Proveedor/agregar/', ProveedorCreateView.as_view(), name='proveedor_crear'),
    path('Proveedor/editar/<int:pk>/', ProveedorUpdateView.as_view(), name='proveedor_editar'),
    path('Proveedor/eliminar/<int:pk>/', ProveedorDeleteView.as_view(), name='proveedor_eliminar'),
    path("proveedor/modal/crear/", ProveedorCreateModalView.as_view(), name="proveedor_modal_crear"),
    path("proveedor/inactivos/", ProveedorInactivaListView.as_view(), name="proveedor_inactivos"),
    path('proveedor/activar/<int:pk>/', ProveedorActivateView.as_view(), name="proveedor_activar"),

    # -------------urls Steven--------------
    path('cliente/listar/', ClienteListView.as_view(), name='cliente_lista'),
    path('cliente/agregar/', ClienteCreateView.as_view(), name='cliente_crear'),
    path('cliente/editar/<int:pk>/', ClienteUpdateView.as_view(), name='cliente_editar'),
    path('cliente/eliminar/<int:pk>/', ClienteDeleteView.as_view(), name='cliente_eliminar'),
    path("cliente/modal/crear/", ClienteCreateModalView.as_view(), name="cliente_modal_crear"),
    path("clientes/inactivos/", ClienteInactivosListView.as_view(), name="cliente_inactivos"),
    path('cliente/activar/<int:pk>/', ClienteInactivoDeleteView.as_view(), name="cliente_activar"),
    
    
    
    #---------urls empresa---------
    path('empresa/listar/', EmpresaListView.as_view(), name='empresa_lista'),
    path('empresa/agregar/', EmpresaCreateView.as_view(), name='empresa_crear'),
    path('empresa/editar/<int:pk>/', EmpresaUpdateView.as_view(), name='empresa_editar'),
    path('empresa/eliminar/<int:pk>/', EmpresaDeleteView.as_view(), name='empresa_eliminar'),
    path("empresa/modal/crear/", EmpresaCreateModalView.as_view(), name="empresa_modal_crear"),
    path("empresa/inactivos/", EmpresaInactivasListView.as_view(), name="empresa_inactivos"),
    path("empresa/activar/<int:pk>/", EmpresaInactivaDeleteView.as_view(), name="empresa_activar"),
    

    path('vehiculo/listar/', VehiculoListView.as_view(), name='vehiculo_lista'),
    path('vehiculo/agregar/', VehiculoCreateView.as_view(), name='vehiculo_crear'),
    path('vehiculo/editar/<int:pk>/', VehiculoUpdateView.as_view(), name='vehiculo_editar'),
    path('vehiculo/eliminar/<int:pk>/', VehiculoDeleteView.as_view(), name='vehiculo_eliminar'),
    path("vehiculo/modal/crear/", VehiculoCreateModalView.as_view(), name="vehiculo_modal_crear"),
    path("vehiculo/inactivos/", VehiculoInactivoListView.as_view(), name="vehiculo_inactivos"),
    path('vehiculo/activar/<int:pk>/', VehiculoInactivoDeleteView.as_view(), name="vehiculo_activar"),
    
    path('entrada_vehiculo/listar/', EntradaVehiculoListView.as_view(), name='entrada_vehiculo_lista'),
    path('entrada_vehiculo/agregar/', EntradaVehiculoCreateView.as_view(), name='entrada_vehiculo_crear'),
    path('entrada_vehiculo/editar/<int:pk>/', EntradaVehiculoUpdateView.as_view(), name='entrada_vehiculo_editar'),
    path('entrada_vehiculo/eliminar/<int:pk>/', EntradaVehiculoDeleteView.as_view(), name='entrada_vehiculo_eliminar'),
    path("entrada_vehiculo/modal/crear/", EntradaCreateModalView.as_view(), name="entrada_vehiculo_modal_crear"),
    path('entrada_vehiculo/datos/<int:pk>/', api_entrada_datos, name='api_entrada_datos'),
    
    path('salida_vehiculo/listar/', SalidaVehiculoListView.as_view(), name='salida_vehiculo_lista'),
    path('salida_vehiculo/agregar/', SalidaVehiculoCreateView.as_view(), name='salida_vehiculo_crear'),
    path('salida_vehiculo/editar/<int:pk>/', SalidaVehiculoUpdateView.as_view(), name='salida_vehiculo_editar'),
    path('salida_vehiculo/eliminar/<int:pk>/', SalidaVehiculoDeleteView.as_view(), name='salida_vehiculo_eliminar'),  
    path("salida_vehiculo/modal/crear/", SalidaCreateModalView.as_view(), name="salida_vehiculo_modal_crear"),
    
    # --------------urls Usuario y permisos-------------- 
    path('perfil/', datos_usuario ,name='perfil_usuario'),
    path('perfil/editar/', PerfilEditarView.as_view(), name='editar_usuario'),  
    path('auth/password_change/', PerfilPasswordChangeView.as_view(), name='password_change'),
    path('perfil/foto/', ActualizarPerfilImagenView.as_view(), name='actualizar_perfil_imagen'),

    path('registro/lista/', RegistroUsuarioListView.as_view(), name='registro_usuario_lista'), 
    path('registro/crear/', RegistroUsuarioCreateView.as_view(), name='registro_usuario_crear'), 
    path('registro/editar/<int:pk>/', RegistroUpdateView.as_view(), name='registro_usuario_editar'), 
    path('registro/eliminar/<int:pk>/', RegistroDeleteView.as_view(), name='registro_usuario_eliminar'),
    path('usuarios/inactivos/', RegistroUsuarioInactivosListView.as_view(), name='registro_usuario_inactivos'),
    path('usuarios/activar/<int:pk>/', RegistroUsuarioActivarView.as_view(), name='registro_usuario_activar'),
    path("empleado/modal/crear/", EmpleadoCreateModalView.as_view(), name="empleado_modal_crear"),  
    
    
    path('permisos/', permisos_usuarios, name='permisos_usuarios'),  
  
  
  
  
    
        #--------URL modulo informes----------------
    path('informes/lista/', InformeListView.as_view(), name='informe_lista'),
    path('informes/nuevo/', CreateInformeView.as_view(), name='informe_nuevo'),
    path('informes/detalle/<int:pk>/', InformeDetailView.as_view(), name='informe_detalle'),
    path('informes/exportar/excel/', exportar_informe_excel, name='exportar_excel'),
    path('informes/gerencial/', InformeGerencialView.as_view(), name='informe_gerencial'),

    #--------URL modulo pago de sercicios publicos----------------
    path('PagoServicios/listar/', PagoServiciosListView.as_view() , name='pago_servicios_lista'),
    path('PagoServicios/agregar/', PagoServiciosCreateView.as_view() , name='pago_servicios_crear'),
    path('PagoServicios/editar/<int:pk>/', PagoServiciosUpdateView.as_view() , name='pago_servicios_editar'),
    path('PagoServicios/eliminar/<int:pk>/', PagoServiciosDeleteView.as_view() , name='pago_servicios_eliminar'),
    path("PagoServicios/modal/crear/", PagoServiciosCreateModalView.as_view(), name="PagoServicios_modal_crear"),
    path("PagoServicios/inactivos/", PagoServiciosInactivosListView.as_view(), name="pago_servicios_inactivos"),
    path('PagoServicios/activar/<int:pk>/', PagoServiciosActivateView.as_view(), name="pago_servicios_activar"),
    #--------URL modulo pagos----------------
    path('Pagos/listar/', PagosListView.as_view() , name='pagos_lista'),
    path('Pagos/agregar/', PagosCreateView.as_view() , name='pagos_crear'),
    path('Pagos/editar/<int:pk>/', PagosUpdateView.as_view() , name='pagos_editar'),
    path('Pagos/eliminar/<int:pk>/', PagosDeleteView.as_view() , name='pagos_eliminar'),
    path('Pagos/activar/<int:pk>/', PagosActivateView.as_view(), name="pagos_activar"),

    #--------------urls Yury
    #----------url Gastos-------
    path('gasto/listar/', GastosListView.as_view() , name='gasto_lista'),
    path('gasto/agregar/', GastosCreateView.as_view(), name='gasto_crear'),
    path('gasto/editar/<int:pk>/', GastosUpdateView.as_view(), name='gasto_editar'),
    path('gasto/eliminar/<int:pk>/', GastosDeleteView.as_view(), name='gasto_eliminar'),
    path("gasto/inactivos/", GastosInactivosListView.as_view(), name="gasto_inactivos"),
    path('gasto/activar/<int:pk>/', GastosActivateView.as_view(), name="gasto_activar"),
    
    #----------url Marca-------
    path('marca/listar/', MarcaListView.as_view() , name='marca_lista'),
    path('marca/agregar/',     MarcaCreateView.as_view(), name='marca_crear'),
    path('marca/editar/<int:pk>/',   MarcaUpdateView.as_view(), name='marca_editar'),
    path('marca/eliminar/<int:pk>/', MarcaDeleteView.as_view(), name='marca_eliminar'),
    path("marca/modal/crear/", MarcaCreateModalView.as_view(), name="marca_modal_crear"),
    path("marca/inactivos/", MarcaInactivosListView.as_view(), name="marca_inactivos"),
    path('marca/activar/<int:pk>/', MarcaActivateView.as_view(), name="marca_activar"),
    
    #-------------urls Caja---------------
     path('caja/listar/', CajaListView.as_view() , name='caja_lista'),
    path('caja/agregar/', CajaCreateView.as_view(), name='caja_crear'),
    path('caja/editar/<int:pk>/', CajaUpdateView.as_view(), name='caja_editar'),
    path('caja/eliminar/<int:pk>/', CajaDeleteView.as_view(), name='caja_eliminar'),
    path("caja/inactivos/", CajaInactivaListView.as_view(), name="caja_inactivos"),
    path('caja/activar/<int:pk>/', CajaActivateView.as_view(), name="caja_activar"),

    path('herramienta/listar/', HerramientaListView.as_view() , name='herramienta_lista'),
    path('herramienta/agregar/', HerramientaCreateView.as_view() , name='herramienta_crear'),
    path('herramienta/editar/<int:pk>/', HerramientaUpdateView.as_view() , name='herramienta_editar'),
    path('herramienta/eliminar/<int:pk>/', HerramientaDeleteView.as_view() , name='herramienta_eliminar'),
    path("herramienta/modal/crear/", HerramientaCreateModalView.as_view(), name="herramienta_modal_crear"),
    path("herramienta/inactivos/", HerramientaInactivosListView.as_view(), name="herramienta_inactivos"),
    path('herramienta/activar/<int:pk>/', HerramientaActivateView.as_view(), name="herramienta_activar"),
    
    path('tipo_mantenimiento/listar/', TipoMantenimientoListView.as_view() , name='tipo_mantenimiento_lista'),
    path('tipo_mantenimiento/agregar/', TipoMantenimientoCreateView.as_view() , name='tipo_mantenimiento_crear'),
    path('tipo_mantenimiento/editar/<int:pk>/', TipoMantenimientoUpdateView.as_view() , name='tipo_mantenimiento_editar'),
    path('tipo_mantenimiento/eliminar/<int:pk>/', TipoMantenimientoDeleteView.as_view() , name='tipo_mantenimiento_eliminar'),
    path("tipo_mantenimiento/modal/crear/", TipoMantenimientoCreateModalView.as_view(), name="tipo_mantenimiento_modal_crear"),
    path("detallemantenimiento/modal/crear/", DetalleTipoMantenimientoCreateModalView.as_view(), name="detallemantenimiento_modal_crear"),
    path("tipo_mantenimiento/inactivos/", TipoMantenimientoInactivosListView.as_view(), name="tipo_mantenimiento_inactivos"),
    path('tipo_mantenimiento/activar/<int:pk>/', TipoMantenimientoActivateView.as_view(), name="tipo_mantenimiento_activar"),
    
    path('nomina/listar/', NominaListView.as_view() , name='nomina_lista'),
    path('nomina/agregar/', NominaCreateView.as_view(), name='nomina_crear'),
    path('nomina/editar/<int:pk>/', NominaUpdateView.as_view(), name='nomina_editar'),
    path('nomina/eliminar/<int:pk>/', NominaDeleteView.as_view(), name='nomina_eliminar'),  
    path("nomina/modal/crear/", NominaCreateModalView.as_view(), name="nomina_modal_crear"),

    
    path('insumos/listar/', InsumoListView.as_view() , name='insumo_lista'),
    path('insumos/agregar/', InsumoCreateView.as_view() , name='insumo_crear'),
    path('insumos/editar/<int:pk>/', InsumoUpdateView.as_view() , name='insumo_editar'),
    path('insumos/eliminar/<int:pk>/', InsumoDeleteView.as_view() , name='insumo_eliminar'),
    path("insumos/modal/crear/", InsumoCreateModalView.as_view(), name="insumos_modal_crear"),
    path("detalleinsumos/modal/crear/", InsumoCreateModalView.as_view(), name="detalleinsumos_modal_crear"),
    path("insumos/inactivos/", InsumoInactivoListView.as_view(), name="insumos_inactivos"),
    path('insumo/activar/<int:pk>/', InsumoActivateView.as_view (), name="insumo_activar"),
    
    path('repuestos/listar/', RepuestoListView.as_view() , name='repuesto_lista'),
    path('repuestos/agregar/', RepuestoCreateView.as_view() , name='repuesto_crear'),
    path('repuestos/editar/<int:pk>/', RepuestoUpdateView.as_view() , name='repuesto_editar'),
    path('repuestos/eliminar/<int:pk>/', RepuestoDeleteView.as_view() , name='repuesto_eliminar'),
    path("repuestos/modal/crear/", RepuestoCreateModalView.as_view(), name="repuesto_modal_crear"),
    path("detallerepuesto/modal/crear/", DetalleRepuestoCreateModalView.as_view(), name="detallerepuesto_modal_crear"),
    path("repuestos/inactivos/", RepuestoInactivosListView.as_view(), name="repuestos_inactivos"),
    path('repuesto/activar/<int:pk>/', RepuestoActivateView.as_view (), name="repuesto_activar"),

    path('api/stock-bajo/', api_stock_bajo, name='api_stock_bajo'),
    path('main/', Main.as_view(), name='main'),
    path('estadisticas/', estadisticas, name='estadisticas'),
    path('api/clientes/count/', api_contador_clientes, name='api_contador_clientes'),
    path('api/vehiculos/count/', api_contador_vehiculos, name='api_contador_vehiculos'),
    path('api/insumos/count/', api_contador_insumos, name='api_contador_insumos'),
    path('api/gastos/count/', api_contador_gastos, name='api_contador_gastos'),
    path('ayuda/', ayuda, name='ayuda'),
    
    
]
