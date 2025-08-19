from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
import re

#------------------FUNCION DE VALIDACION ----------------------
def validar_email (value):  
    if re.search(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', value) is None:
        raise ValidationError('El correo no es valido')
    
telefono_regex = RegexValidator(
    regex=r'^\d{7,10}$',
    message="El teléfono debe contener solo números y tener entre 7 y 10 dígitos."
)

identificacion_regex = RegexValidator(
    regex=r'^\d{5,20}$',
    message="La identificación debe contener solo números y mínimo 5 dígitos."
)

# MODULOS STEVEN

class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    id_operacion = models.IntegerField(default=0)
    nombre = models.CharField(max_length=100)
    documento = models.BigIntegerField(default=0)
    telefono = models.BigIntegerField(default=0)
    correo = models.EmailField(max_length=100)
    fecha_operacion = models.DateField()
    monto = models.IntegerField(default=0)

    def _str_(self):
        return f"{self.id_cliente} - {self.nombre}"


class Vehiculo(models.Model):
    id_vehiculo = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, blank=True,null=True)  # LLAVE
    placa = models.CharField(max_length=10, unique=True)
    modelo_vehiculo = models.CharField(max_length=100)
    marca_vehiculo = models.CharField(max_length=100)
    color = models.CharField(max_length=100)

    def _str_(self):
        return f"{self.placa} - {self.marca_vehiculo} - {self.modelo_vehiculo}"
    

class EntradaVehiculo(models.Model):
    id_entrada = models.AutoField(primary_key=True)
    id_vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE ,blank=True) # LLAVE
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE , blank=True,null=True)  # LLAVE
    fecha_ingreso = models.DateField()
    hora_ingreso = models.TimeField()

    def _str_(self):
        return f"{self.id_cliente.id_cliente} - {self.id_vehiculo.placa} - {self.fecha_ingreso} {self.hora_ingreso}"
    



class SalidaVehiculo(models.Model):
    id_salida = models.AutoField(primary_key=True)
    id_vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE, blank=True,null=True) # LLAVE
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE,blank=True,null=True)  # LLAVE
    diagnostico = models.CharField(max_length=100)
    fecha_salida = models.DateField()
    hora_salida = models.TimeField()

    def _str_(self):
        return f"{self.id_cliente.id_cliente} - {self.id_vehiculo.placa} - {self.diagnostico}"


#------ MODULOS ERICK ---------

#------ ENTIDAD de TIPO mantenmimiento ---------1
class TipoMantenimiento(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def _str_(self):
        return self.nombre

   
#------- Marca-------- 
class Marca(models.Model):
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=100)

    def _str_(self):
        return self.nombre

#------ ENTIDAD REPUESTOS --------3
class Repuesto(models.Model):
    id_marca = models.ForeignKey(Marca, on_delete=models.CASCADE, blank=True, null=True)  # LLAVE
    nombre = models.CharField(max_length=100)
    categoria = models.CharField(max_length=100)
    fabricante = models.CharField(max_length=100)
    stock = models.IntegerField(default=0)
    ubicacion = models.CharField(max_length=100)
    precio = models.IntegerField(default=0)
    stock_minimo = models.IntegerField(default=2)
    
    def __str__(self):
        return f"{self.nombre} "   
   
    
#------ ENTIDAD HERRAMIENTAS --------4
class Herramienta(models.Model):

    nombre = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    tipo = models.CharField(max_length=100)
    material = models.CharField(max_length=100)
    id_marca = models.ForeignKey(Marca, on_delete=models.CASCADE, blank=True, null=True)
    stock = models.IntegerField(default=0)

    def _str_(self):
        return self.nombre

#------ ENTIDAD INSUMOS --------5
class Insumos(models.Model):

    id_marca = models.ForeignKey(Marca, on_delete=models.SET_NULL, blank=True, null=True)
    nombre = models.CharField(max_length=100)
    costo = models.IntegerField()
    tipo = models.CharField(max_length=100)
    stock = models.IntegerField(default=0)

    def _str_(self):

        return f"{self.nombre} ({self.id})"

 
#-------------MODULOS DE karol-----------
#-------------Modulo Administrador-----------
class Administrador(models.Model):
    id_admin = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, error_messages={'blank': 'El nombre es obligatorio'})
    apellidos = models.CharField(max_length=100, error_messages={'blank': 'El apellido es obligatorio'})
    identificacion = models.BigIntegerField(unique=True, error_messages={'unique': 'Ya existe un administrador con esa identificación', 
                        'blank': 'La identificación es obligatoria'})
    edad = models.PositiveIntegerField(error_messages={'blank': 'La edad es obligatoria'})
    correo = models.EmailField(unique=True, validators=[validar_email],
            error_messages={
            'unique': 'Ya existe un administrador con ese correo',
            'invalid': 'El correo no tiene un formato válido',
            'blank': 'El correo es obligatorio'
        })
    telefono = models.CharField(max_length=20, validators=[telefono_regex], error_messages={'blank': 'El teléfono es obligatorio'})
    fecha_ingreso = models.DateField(error_messages={'blank': 'La fecha de ingreso es obligatoria'})
    
    def _str_(self):
        return f"{self.nombre} {self.apellidos}"


#--------------Modulo Pago Servicio Publicos-----------
class PagoServiciosPublicos(models.Model):
    id_servicio = models.AutoField(primary_key=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    
    def _str_(self):
        return f"{self.id_servicio} {self.monto}"
    
#--------------Modulo Proveedores--------------
class Proveedores(models.Model):
    id_proveedor = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, validators=[telefono_regex])
    correo = models.EmailField(unique=True, validators=[validar_email])
    
    def _str_(self):
        return f"{self.id_proveedor} {self.correo}"
    

#--------------Modulo Compra (STEVEN)-----------------
class Compra(models.Model):
    id_compra = models.AutoField(primary_key=True)
    id_factura_compra = models.IntegerField(unique=True)
    id_proveedor = models.ForeignKey(Proveedores, on_delete=models.CASCADE, blank=True,null=True)  # LLAVE
    fecha_compra = models.DateField()
    hora_compra = models.TimeField()

    def _str_(self):
        return f"{self.id_factura_compra} - {self.proveedor} - {self.fecha_compra} {self.hora_compra}"

    
        



#--------------Modulo Pagos-----------------
class Pagos(models.Model):
    id_pago = models.AutoField(primary_key=True)
    tipo_pago = models.CharField(max_length=100)
    fecha = models.DateField()
    hora = models.TimeField()
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    id_proveedor = models.ForeignKey(Proveedores, on_delete=models.SET_NULL, null=True,blank=True)
    id_admin = models.ForeignKey(Administrador, on_delete=models.SET_NULL, null=True,blank=True)
    id_herramienta = models.ForeignKey(Herramienta, on_delete=models.SET_NULL, null=True, blank=True)
    id_insumos = models.ForeignKey(Insumos, on_delete=models.SET_NULL, null=True, blank=True)
    id_repuestos = models.ForeignKey(Repuesto, on_delete=models.SET_NULL, null=True, blank=True)
    
    def _str_(self):
        return f"{self.id_pago} {self.monto}"



class Gastos(models.Model):
   
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField() 
    tipo_gastos=models.CharField(max_length=100)
    id_pagos_servicios = models.ForeignKey(PagoServiciosPublicos, on_delete=models.SET_NULL, null=True, blank=True,)
    def __str__(self):
        return f"{self.tipo_gastos} - ${self.monto}"
     #class meta
       #verbose_name = 'Gastos'
        #verbose_name_plural = 'Gastos'          

#-------- Empleado-------
class Empleado(models.Model): 
   
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    identificacion = models.CharField(max_length=20, unique=True) 
    Correo= models.EmailField(max_length=254, unique=True)
    direccion = models.CharField(max_length=255)
    def _str_(self):
        return f"{self.nombre} ({self.identificacion})"
    #class meta
        #verbose_name = 'Empleado'
        #verbose_name_plural = 'Empleado'



#------ ENTIDAD GESTION DE MANTENIMIENTO --------2
class Mantenimiento(models.Model):
    fallas = models.TextField()
    procesos = models.CharField(max_length=50)
    id_vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE,blank=True,null=True)
    id_empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE,blank=True,null=True)
    id_tipo_mantenimiento = models.ForeignKey(TipoMantenimiento, on_delete=models.CASCADE,blank=True,null=True)

    def _str_(self):
        return f"{self.fallas} - {self.id_tipo_mantenimiento}"

    
#------------Modulo Informes-----------
class Informes(models.Model):
    id_informe = models.AutoField(primary_key=True)
    repuestos_usados = models.TextField()
    costo_mano_obra = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField()
    hora = models.TimeField()
    id_repuesto = models.ForeignKey(Repuesto, on_delete=models.SET_NULL, null=True, blank=True)
    id_empleado = models.ForeignKey(Empleado, on_delete=models.SET_NULL, null=True, blank=True)
    tipo_informe = models.CharField(max_length=100)
    id_mantenimiento = models.ForeignKey(Mantenimiento, on_delete=models.SET_NULL, null=True, blank=True)
    
    def _str_(self):
        return f"{self.id_informe} {self.tipo_informe}"
    
    
#-------- nomina------
class Nomina(models.Model):
   
    rol = models.CharField(max_length=100) 
    monto= models.DecimalField(max_digits=10, decimal_places=2) 
    fecha_pago =  models.DateField() 
    id_empleado =   models.ForeignKey(Empleado, on_delete=models.SET_NULL, null=True,blank=True)            
    def __str__(self):
        return f"{self.rol} - ${self.monto} - {self.fecha_pago}"
     #class meta
        #verbose_name = 'Nomina'
        #verbose_name_plural = 'Nomina'


#-----------Factura-----------------
class Factura(models.Model):
    
    tipo_pago = models.CharField(max_length=45, null=True, blank=True)
    id_cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True)
    id_vehiculo = models.ForeignKey(Vehiculo, on_delete=models.SET_NULL, null=True, blank=True)
    id_tipo_mantenimiento = models.ForeignKey(TipoMantenimiento, on_delete=models.SET_NULL, null=True, blank=True)
    servicio_prestado = models.CharField(max_length=45, null=True, blank=True)
    nombre_empresa = models.CharField(max_length=45, null=True, blank=True)
    direccion_empresa = models.CharField(max_length=45, null=True, blank=True)
    id_empleado = models.ForeignKey(Empleado, on_delete=models.SET_NULL, null=True, blank=True)

    def _str_(self):
        return f"Factura {self.id} - {self.tipo_pago or 'Sin pago'}"

#-----------Caja-----------------
class Caja(models.Model):
   
    tipo_movimiento= models.CharField(max_length=50)
    monto= models.DecimalField(max_digits=10, decimal_places=2)
    fecha= models.DateField()
    hora=models.TimeField()
    id_gasto= models.ForeignKey( Gastos , on_delete=models.SET_NULL, null=True, blank=True )
    id_admin=models.ForeignKey(Administrador, on_delete=models.SET_NULL, null=True, blank=True) 
    id_Factura= models.ForeignKey(Factura, on_delete=models.SET_NULL, null=True, blank=True)
    id_pagos= models.ForeignKey(Pagos, on_delete=models.SET_NULL, null=True, blank=True)
    id_nomina= models.ForeignKey(Nomina, on_delete=models.SET_NULL, null=True, blank=True) 
    def __str__(self):
        return f"{self.tipo_movimiento} - {self.monto} en {self.fecha} {self.hora}"   
    #class meta
        #verbose_name = 'Caja'
        #verbose_name_plural = 'Caja'


