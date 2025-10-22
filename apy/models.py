from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from django.contrib.auth.models import User

import re

#------------------FUNCION DE VALIDACION ----------------------
def validar_email (value):  
    if re.search(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', value) is None:
        raise ValidationError('El correo no es valido')
    
def validar_telefono(value):
    s = str(value).strip()
    
    if not re.fullmatch(r'^\d+$', s):
        raise ValidationError('El telefono debe contener únicamente números')
    
    if not (7 <= len(s) <= 10):
        raise ValidationError('El teléfono debe tener entre 7 y 10 dígitos')
    
def validar_identificacion(value):
    s = str(value).strip()

    # Verifica solo números (sin letras ni símbolos)
    if not re.fullmatch(r'^\d+$', s):
        raise ValidationError('La identificación debe contener únicamente números')

    # Verifica la longitud
    if not (8 <= len(s) <= 11):
        raise ValidationError('La identificación debe tener entre 8 y 11 dígitos')
    
def validar_edad(value):
    if value < 16 or value > 90:
        raise ValidationError('La edad debe estar en un rango entre 16 a 90 años')
    
def validar_monto(value):
    s = str(value).strip()

    # Regex: solo números con opcional parte decimal
    if not re.fullmatch(r'^\d+(\.\d+)?$', s):
        raise ValidationError('El monto debe ser un número válido (entero o decimal)')

    monto = float(s)

    if monto < 99:
        raise ValidationError('El monto debe ser mayor o igual a 99')

placa_regex = RegexValidator(
        regex=r'^[A-Z0-9]{6}$',
        message="La placa debe tener exactamente 6 caracteres alfanuméricos (letras mayúsculas o números)."
    )

modelo_regex = RegexValidator(
        regex=r'^\d{4}$',
        message="El modelo debe ser un año válido de 4 dígitos (ej: 2024)."
    )

marca_regex = RegexValidator(
        regex=r'^[A-Za-z\s]+$',
        message="La marca solo debe contener letras."
    )

color_regex = RegexValidator(
        regex=r'^[A-Za-z\s]+$',
        message="El color solo debe contener letras."
    )


#------ MODULOS ERICK ---------

#------ ENTIDAD de TIPO mantenmimiento ---------1
class TipoMantenimiento(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

   
#------- Marca-------- 
class Marca(models.Model):
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre} - {self.tipo}"

#------ ENTIDAD REPUESTOS --------3
class Repuesto(models.Model):
    id_marca = models.ForeignKey(Marca, on_delete=models.CASCADE)  # LLAVE
    nombre = models.CharField(max_length=100)
    CATEGORIA_OPCIONES = [
        ('automotriz', 'Automotriz'),
        ('industrial', 'Industrial'),
    ]
    categoria = models.CharField(max_length=100, choices=CATEGORIA_OPCIONES)
    fabricante = models.CharField(max_length=100)
    stock = models.IntegerField()
    ubicacion = models.CharField(max_length=100)
    precio = models.IntegerField(  # 🔹 ENTEROS, sin decimales
        error_messages={
            'invalid': 'Ingrese un número válido para el precio.',
            'required': 'El precio del repuesto es obligatorio.'
        } , validators=[validar_monto]
    )
    
    def __str__(self):
        return f"{self.nombre} "   
   
    
#------ ENTIDAD HERRAMIENTAS --------4
class Herramienta(models.Model):

    nombre = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    TIPO_OPCIONES = [
        ('manuales', 'Manuales'),
        ('eléctricas', 'Eléctricas'),
        ('neumáticas', 'Neumáticas'),
        ('de medición', 'De Medición'),
    ]
    tipo = models.CharField(max_length=100, choices=TIPO_OPCIONES)
    material = models.CharField(max_length=100)
    id_marca = models.ForeignKey(Marca, on_delete=models.CASCADE)
    stock = models.IntegerField()

    def __str__(self):
        return self.nombre

#------ ENTIDAD INSUMOS --------
class Insumos(models.Model):

    id_marca = models.ForeignKey(Marca, on_delete=models.CASCADE)
    costo = models.IntegerField(  # 🔹 ENTEROS, sin decimales
        error_messages={
            'invalid': 'Ingrese un número válido para el costo.',
            'required': 'El costo del insumo es obligatorio.'
        }, validators=[validar_monto]
    )
    stock = models.IntegerField()
    CANTIDAD_OPCIONES = [
        ('galon', 'Galón'),
        ('litro', 'Litro'),
        ('mililitro', 'Mililitro'),
        ('unidades', 'Unidades'),
    ]

    cantidad = models.CharField(max_length=20, choices=CANTIDAD_OPCIONES)

    def __str__(self):

        return f"{self.id_marca} ({self.cantidad})"


# MODULOS STEVEN
class Module(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Permission(models.Model):
    module = models.ForeignKey(Module, related_name='perms', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='permissions', on_delete=models.CASCADE)
    view = models.BooleanField(default=False)
    add = models.BooleanField(default=False)
    change = models.BooleanField(default=False)
    delete = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.module.name}"




class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    documento = models.BigIntegerField(validators=[validar_identificacion])
    telefono = models.BigIntegerField(validators=[validar_telefono])
    correo = models.EmailField(max_length=100, validators=[validar_email])
    fecha_operacion = models.DateField()
    monto = models.IntegerField(  # 🔹 ENTEROS, sin decimales
        error_messages={
            'invalid': 'Ingrese un número válido para el monto.',
            'required': 'El monto del cliente es obligatorio.'
        } , validators=[validar_monto]
    )

    def __str__(self):
        return f"{self.id_cliente} - {self.nombre}"


class Vehiculo(models.Model):
    id_vehiculo = models.AutoField(primary_key=True)
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)  
    placa = models.CharField(max_length=10, unique=True,validators=[placa_regex])
    modelo_vehiculo = models.CharField(max_length=4,validators=[modelo_regex])
    marca_vehiculo = models.CharField(max_length=100, validators=[marca_regex])
    color = models.CharField(max_length=100, validators=[color_regex])

    def __str__(self):
        return f"{self.placa} - {self.marca_vehiculo} - {self.modelo_vehiculo}"
    

class EntradaVehiculo(models.Model):
    id_entrada = models.AutoField(primary_key=True)
    id_vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE) # LLAVE
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)  # LLAVE
    fecha_ingreso = models.DateField()
    hora_ingreso = models.TimeField()

    def __str__(self):
        return f"{self.id_cliente.id_cliente} - {self.id_vehiculo.placa} - {self.fecha_ingreso} {self.hora_ingreso}"
    

class SalidaVehiculo(models.Model):
    id_salida = models.AutoField(primary_key=True)
    id_vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE) # LLAVE
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)  # LLAVE
    diagnostico = models.CharField(max_length=100)
    fecha_salida = models.DateField()
    hora_salida = models.TimeField()

    def __str__(self):
        return f"{self.id_cliente.id_cliente} - {self.id_vehiculo.placa} - {self.diagnostico}"


 
#-------------MODULOS DE karol-----------
#-------------Modulo Administrador-----------
class Administrador(models.Model):
    id_admin = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    identificacion = models.IntegerField(max_length=11, unique=True, validators=[validar_identificacion])
    edad = models.PositiveIntegerField(validators=[validar_edad])
    correo = models.EmailField(unique=True, validators=[validar_email])
    telefono = models.IntegerField(max_length=10, validators=[validar_telefono])
    fecha_ingreso = models.DateField()
    
    def __str__(self):
        return f"{self.nombre} {self.apellidos}"


#--------------Modulo Pago Servicio Publicos-----------
class PagoServiciosPublicos(models.Model):
    id_servicio = models.AutoField(primary_key=True)
    SERVICIO_OPCIONES = [
        ('luz', 'Luz'),
        ('agua', 'Agua'),
        ('gas', 'Gas'),
        ('internet', 'Internet'),
    ]

    servicio = models.CharField(
        max_length=20,
        choices=SERVICIO_OPCIONES
    )
    monto = models.IntegerField(  # 🔹 ENTEROS, sin decimales
        error_messages={
            'invalid': 'Ingrese un número válido para el monto.',
            'required': 'El monto de la nomina es obligatorio.'
        } , validators=[validar_monto]
    )
    
    def __str__(self):
        return f"{self.id_servicio} - {self.servicio} -{self.monto}"
    
#--------------Modulo Proveedores--------------
class Proveedores(models.Model):
    id_proveedor = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, validators=[validar_telefono])
    correo = models.EmailField(unique=True, validators=[validar_email])
    
    def __str__(self):
        return f"{self.id_proveedor} {self.correo}"
    



class Gastos(models.Model):
   
    monto = models.IntegerField(  # 🔹 ENTEROS, sin decimales
        error_messages={
            'invalid': 'Ingrese un número válido para el monto.',
            'required': 'El monto del gasto es obligatorio.'
        }, validators=[validar_monto]
    )
    descripcion = models.TextField() 
    TIPO_GASTOS_OPCIONES = [
        ('costo fijo', 'Costo fijo'),
        ('costo directo', 'Costo directo'),
        ('costo variable', 'Costo variable'),
    ]
    tipo_gastos=models.CharField(max_length=100, choices=TIPO_GASTOS_OPCIONES)
    id_pagos_servicios = models.ForeignKey(PagoServiciosPublicos, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.tipo_gastos} - ${self.monto}"
     #class meta
       #verbose_name = 'Gastos'
        #verbose_name_plural = 'Gastos'          

#-------- Empleado-------
class Empleado(models.Model): 
   
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15, validators=[validar_telefono])
    identificacion = models.CharField(max_length=20, unique=True, validators=[validar_identificacion]) 
    Correo= models.EmailField(max_length=254, unique=True, validators=[validar_email])
    direccion = models.CharField(max_length=255)
    def __str__(self):
        return f"{self.nombre} ({self.identificacion})"
    #class meta
        #verbose_name = 'Empleado'
        #verbose_name_plural = 'Empleado'



#------ ENTIDAD GESTION DE MANTENIMIENTO --------2
class Mantenimiento(models.Model):
    fallas = models.TextField()
    procesos = models.CharField(max_length=50)
    id_vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    id_empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    id_tipo_mantenimiento = models.ForeignKey(TipoMantenimiento, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.fallas} - {self.id_tipo_mantenimiento}"

    
#------------Modulo Informes-----------
class Informes(models.Model):
    id_informe = models.AutoField(primary_key=True)
    repuestos_usados = models.TextField()
    costo_mano_obra = models.IntegerField(  # 🔹 ENTEROS, sin decimales
        error_messages={
            'invalid': 'Ingrese un número válido para el costo de mano de obra.',
            'required': 'El costo de mano de obra es obligatorio.'
        }, validators=[validar_monto]
    )
    fecha = models.DateField()
    hora = models.TimeField()
    id_repuesto = models.ForeignKey(Repuesto, on_delete=models.CASCADE)
    id_empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    tipo_informe = models.CharField(max_length=100)
    id_mantenimiento = models.ForeignKey(Mantenimiento, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.id_informe} {self.tipo_informe}"
    
    
#-------- nomina------
class Nomina(models.Model):
    
    TIPO_ROL = [
        ('administrador', 'Administrador'),
        ('empleado', 'Empleado'),
    ]
    
    rol = models.CharField(max_length=100, choices=TIPO_ROL)
    monto = models.IntegerField(  # 🔹 ENTEROS, sin decimales
        error_messages={
            'invalid': 'Ingrese un número válido para el monto.',
            'required': 'El monto de la nomina es obligatorio.'
        } , validators=[validar_monto]
    )
    fecha_pago =  models.DateField() 
    id_empleado =   models.ForeignKey(Empleado, on_delete=models.CASCADE)            
    def __str__(self):
        return f"{self.rol} - ${self.monto} - {self.fecha_pago}"
     #class meta
        #verbose_name = 'Nomina'
        #verbose_name_plural = 'Nomina'


#--------------Modulo Pagos-----------------
class Pagos(models.Model):
    id_pago = models.AutoField(primary_key=True)
    tipo_pago = models.CharField(max_length=100)
    fecha = models.DateField()
    hora = models.TimeField()
    monto = models.IntegerField(  # 🔹 ENTEROS, sin decimales
        error_messages={
            'invalid': 'Ingrese un número válido para el monto.',
            'required': 'El monto del pago es obligatorio.'
        } , validators=[validar_monto]
    )
    id_proveedor = models.ForeignKey(Proveedores, on_delete=models.CASCADE)
    id_admin = models.ForeignKey(Administrador, on_delete=models.CASCADE)
    id_herramienta = models.ForeignKey(Herramienta, on_delete=models.CASCADE)
    id_insumos = models.ForeignKey(Insumos, on_delete=models.CASCADE)
    id_repuesto = models.ForeignKey(Repuesto, on_delete=models.CASCADE)
    id_nomina= models.ForeignKey(Nomina, on_delete=models.CASCADE, blank=True, null=True) 
    
    def __str__(self):
        return f"{self.id_pago} {self.monto}"


#-----------Factura-----------------
class Factura(models.Model):
    
    tipo_pago = models.CharField(max_length=45)
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    id_vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    id_tipo_mantenimiento = models.ForeignKey(TipoMantenimiento, on_delete=models.CASCADE)
    servicio_prestado = models.CharField(max_length=45)
    nombre_empresa = models.CharField(max_length=45)
    direccion_empresa = models.CharField(max_length=45)
    id_empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    monto = models.IntegerField(  # 🔹 ENTEROS, sin decimales
        error_messages={
            'invalid': 'Ingrese un número válido para el monto.',
            'required': 'El monto de la factura es obligatorio.'
        } , validators=[validar_monto]
    )

    def __str__(self):
        return f"Factura {self.id} - {self.tipo_pago or 'Sin pago'}"


#--------------Modulo Compra (STEVEN)-----------------
class Compra(models.Model):
    id_compra = models.AutoField(primary_key=True)
    id_factura_compra = models.ForeignKey(Factura, on_delete=models.CASCADE)
    id_proveedor = models.ForeignKey(Proveedores, on_delete=models.CASCADE)  # LLAVE
    fecha_compra = models.DateField()
    hora_compra = models.TimeField()

    def __str__(self):
        return f"{self.id_factura_compra} - {self.proveedor} - {self.fecha_compra} {self.hora_compra}"


#-----------Caja-----------------
class Caja(models.Model):
    TIPO_OPCIONES = [
        ('Ingreso', 'Ingreso'),
        ('Gasto', 'Gasto'),
        ('Venta', 'Venta'),
        ('Compra', 'Compra'),
    ]

    tipo_movimiento = models.CharField(
        max_length=20,
        choices=TIPO_OPCIONES
    )
    monto = models.IntegerField(  # 🔹 ENTEROS, sin decimales
        error_messages={
            'invalid': 'Ingrese un número válido para el monto.',
            'required': 'El monto de la caja es obligatorio.'
        } , validators=[validar_monto]
    )
    fecha= models.DateField()
    hora=models.TimeField()
    id_admin=models.ForeignKey(Administrador, on_delete=models.CASCADE) 
    id_Factura= models.ForeignKey(Factura, on_delete=models.CASCADE, blank=True, null=True)
    def __str__(self):
        return f"{self.tipo_movimiento} - {self.monto} en {self.fecha} {self.hora}"   
    #class meta
        #verbose_name = 'Caja'
        #verbose_name_plural = 'Caja'


