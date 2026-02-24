from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from django.contrib.auth.models import User

import re
from django.core.validators import MinValueValidator, MaxValueValidator

from decimal import Decimal



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
    if not re.fullmatch(r'^\d{7,10}(-\d{1})?$', s):
        raise ValidationError('Ingrese solo números (Cédula) o el formato 123456789-0 (NIT).')
    
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

nit_validator = RegexValidator(
    regex=r'^(\d{1,3}(\.?\d{3}){2})\-\d$',
    message="El NIT debe tener el formato: 123456789-0 o 12.345.678-0"
)

def validar_por_tipo(numero, tipo):
    """
    Valida el número de identificación según el tipo de documento.
    """
    numero = str(numero).strip().upper()
    reglas = {
        'CC':  (r'^\d{5,10}$', 'La Cédula debe tener entre 5 y 10 dígitos numéricos.'),
        'TI':  (r'^\d{10,11}$', 'La Tarjeta de Identidad debe tener 10 u 11 dígitos.'),
        'RC':  (r'^\d{10,11}$', 'El Registro Civil debe tener 10 u 11 dígitos.'),
        'NIT': (r'^\d{7,10}-\d{1}$', 'El NIT debe tener formato 123456789-0.'),
        'CE':  (r'^\d{3,9}$', 'La Cédula de Extranjería debe ser numérica (hasta 9 dígitos).'),
        'PAS': (r'^[A-Z0-9]{5,20}$', 'El Pasaporte debe ser alfanumérico (5-20 caracteres).'),
        'PPT': (r'^[A-Z0-9]{4,15}$', 'El PPT debe ser alfanumérico.'),
    }

    if tipo not in reglas:
        raise ValidationError("Tipo de documento no soportado.")

    regex, mensaje = reglas[tipo]
    if not re.fullmatch(regex, numero):
        raise ValidationError(mensaje)

#------ MODULOS ERICK ---------

#------ ENTIDAD de TIPO mantenmimiento ---------1
class TipoMantenimiento(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField()
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

   
 
#------- Marca-------- 
class Marca(models.Model):
    tipo= [
        ('Repuesto', 'Repuesto'),
        ('Herramienta', 'Herramienta'),
        ('Insumo', 'Insumo'),
        ('Vehiculo', 'Vehiculo'),
    ]
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=100, choices=tipo)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} "
#------ ENTIDAD REPUESTOS --------3
class Repuesto(models.Model):
    id_marca = models.ForeignKey(Marca, on_delete=models.PROTECT) 
    nombre = models.CharField(max_length=100)
    CATEGORIA_OPCIONES = [
        ('automotriz', 'Automotriz'),
        ('industrial', 'Industrial'),
    ]
    categoria = models.CharField(max_length=100, choices=CATEGORIA_OPCIONES)
    fabricante = models.CharField(max_length=100)
    
    estado = models.BooleanField(default=True)
    
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
    id_marca = models.ForeignKey(Marca, on_delete=models.PROTECT)
    
    estado = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

#------ ENTIDAD INSUMOS --------
class Insumos(models.Model):

    id_marca = models.ForeignKey(Marca, on_delete=models.PROTECT)
    nombre = models.CharField(max_length=100)
    costo = models.IntegerField(  
        error_messages={
            'invalid': 'Ingrese un número válido para el costo.',
            'required': 'El costo del insumo es obligatorio.'
        }, validators=[validar_monto]
    )
    CANTIDAD_OPCIONES = [
        ('galon', 'Galón'),
        ('litro', 'Litro'),
        ('mililitro', 'Mililitro'),
        ('unidades', 'Unidades'),
    ]

    cantidad = models.CharField(max_length=20, choices=CANTIDAD_OPCIONES)
    estado = models.BooleanField(default=True)
    
    def __str__(self):

        return f"{self.id_marca} ({self.cantidad})"


# MODULOS STEVEN
class Module(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Nombre del Módulo")
    description = models.TextField(blank=True, verbose_name="Descripción")

    class Meta:
        verbose_name = "Módulo de Permiso"
        verbose_name_plural = "Módulos de Permisos"
        
    def __str__(self):
        return self.name

class Permission(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='custom_permissions', verbose_name="Usuario")
    module = models.ForeignKey(Module, on_delete=models.PROTECT, verbose_name="Módulo")
    
    # Campos booleanos para los permisos
    view = models.BooleanField(default=False, verbose_name="Ver")
    add = models.BooleanField(default=False, verbose_name="Crear")
    change = models.BooleanField(default=False, verbose_name="Editar")
    delete = models.BooleanField(default=False, verbose_name="Eliminar")

    class Meta:
        # Asegura que un usuario solo tenga un conjunto de permisos por módulo
        unique_together = ('user', 'module') 
        verbose_name = "Permiso Personalizado"
        verbose_name_plural = "Permisos Personalizados"

    def __str__(self):
        return f"Permisos de {self.user.username} en {self.module.name}"

class Profile(models.Model):
    TIPO_DOC_CHOICES = [
        ('CC', 'Cédula de Ciudadanía'),
        ('TI', 'Tarjeta de Identidad'),
        ('RC', 'Registro Civil'),
        ('NIT', 'NIT'),
        ('CE', 'Cédula de Extranjería'),
        ('PAS', 'Pasaporte'),
        ('PPT', 'Permiso de Protección Temporal'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo_identificacion = models.CharField(max_length=5, choices=TIPO_DOC_CHOICES, default='CC')
    identificacion = models.CharField(max_length=20, null=True, blank=True)
    telefono = models.CharField(max_length=10, validators=[validar_telefono], null=True, blank=True)
    direccion = models.CharField(max_length=150, null=True, blank=True)
    imagen = models.ImageField(upload_to='users/%Y/%m/%d', null=True, blank=True)
    
    def clean(self):
        super().clean()
        if self.tipo_identificacion and self.identificacion:
            # Esto lanzará el error si no cumple la regex
            validar_por_tipo(self.identificacion, self.tipo_identificacion)
    
    def __str__(self):
        return f'Perfil de {self.user.username}'
    
class Cliente(models.Model):

    TIPO_CLIENTE = [
        ('cliente particular', 'Cliente Particular'),
        ('empresa', 'Empresa'),
    ]
    tipo = models.CharField(max_length=20, choices=TIPO_CLIENTE)
    nombre = models.CharField(max_length=255, verbose_name="Nombre/Razón Social")
    identificacion = models.CharField(
        max_length=50, 
        unique=True, 
        verbose_name="Documento/NIT", 
        validators=[validar_identificacion], 
        blank=False, 
        null=False 
    )
    telefono = models.CharField(max_length=20)
    correo = models.EmailField(validators=[validar_email], unique=True)
    direccion = models.TextField(verbose_name="Dirección")
    estado = models.BooleanField(default=True, verbose_name="Activo")

    def __str__(self):
        return f"{self.nombre} - {self.identificacion}"
    



class Vehiculo(models.Model):
    id_vehiculo = models.AutoField(primary_key=True) 
    id_cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)  
    placa = models.CharField(max_length=10, unique=True,validators=[placa_regex])
    modelo_vehiculo = models.CharField(max_length=4,validators=[modelo_regex])
    marca_vehiculo = models.CharField(max_length=100, validators=[marca_regex])
    color = models.CharField(max_length=100, validators=[color_regex])
    estado = models.BooleanField(default=True, verbose_name="Activo")

    def __str__(self):
        return f"{self.placa} -  {self.marca_vehiculo} - {self.modelo_vehiculo}- {self.color} - {self.id_cliente.id}"
    

class EntradaVehiculo(models.Model):
    id_entrada = models.AutoField(primary_key=True)
    fecha_ingreso = models.DateField()
    hora_ingreso = models.TimeField()

    def __str__(self):
        return f"{self.fecha_ingreso} - {self.hora_ingreso}"
    

class SalidaVehiculo(models.Model):
    id_salida = models.AutoField(primary_key=True)
    fecha_salida = models.DateField()
    hora_salida = models.TimeField()
    def __str__(self):
    # Usamos .id (el identificador por defecto de Django) 
    # o simplemente self.id_cliente (que usará el nombre del cliente)
        return f"{self.fecha_salida} - {self.hora_salida} "

 
#-------------MODULOS DE karol-----------


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
    estado = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.id_servicio} - {self.servicio} -{self.monto}"
    
#--------------Modulo Proveedores--------------
class Proveedores(models.Model):
    DOCUMENT_CHOICES = [
        ('CC', 'Cédula de Ciudadanía'),
        ('CE', 'Cédula de Extranjería'),
        ('NIT', 'NIT'),
        ('TI', 'Tarjeta de Identidad'),
        ('RC', 'Registro Civil'),
        ('PAS', 'Pasaporte'),
        ('PPT', 'Permiso por Protección Temporal'),
    ]

    id_proveedor = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, validators=[validar_telefono])
    
    # IMPORTANTE: Quité el unique=True de aquí porque podrías tener varios 
    # proveedores con CC, pero diferentes números. El unique va en la identificación.
    tipo_identificacion = models.CharField(choices=DOCUMENT_CHOICES, max_length=5)
    
    identificacion = models.CharField(max_length=20, unique=True)
    correo = models.EmailField(unique=True, validators=[validar_email])
    estado = models.BooleanField(default=True)

    def clean(self):
        """
        Este método se ejecuta antes de guardar los datos.
        Valida la identificación dependiendo del tipo seleccionado.
        """
        super().clean()
        
        # Obtenemos los valores y limpiamos espacios
        tipo = self.tipo_identificacion
        valor = str(self.identificacion).strip().upper()

        # Diccionario de Reglas: { 'TIPO': (Regex, Mensaje) }
        reglas = {
            'CC': (r'^\d{5,10}$', 'La Cédula de Ciudadanía debe tener entre 5 y 10 dígitos numéricos.'),
            'CE': (r'^\d{3,9}$', 'La Cédula de Extranjería debe tener hasta 9 dígitos numéricos.'),
            'NIT': (r'^\d{7,10}-\d{1}$', 'El NIT debe seguir el formato 123456789-0.'),
            'TI': (r'^\d{10,11}$', 'La Tarjeta de Identidad debe tener 10 u 11 dígitos numéricos.'),
            'RC': (r'^\d{10,11}$', 'El Registro Civil debe tener 10 u 11 dígitos numéricos.'),
            'PAS': (r'^[A-Z0-9]{5,20}$', 'El Pasaporte debe tener entre 5 y 20 caracteres alfanuméricos.'),
            'PPT': (r'^[A-Z0-9]{4,15}$', 'El PPT debe tener entre 4 y 15 caracteres alfanuméricos.'),
        }

        if tipo in reglas:
            regex, mensaje = reglas[tipo]
            if not re.fullmatch(regex, valor):
                # Lanzamos el error específicamente en el campo identificación
                raise ValidationError({'identificacion': mensaje})

    def __str__(self):
        return f"{self.nombre} - {self.identificacion}"


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
    id_pagos_servicios = models.ForeignKey(PagoServiciosPublicos, on_delete=models.PROTECT)
    estado = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.tipo_gastos} - ${self.monto}"
     #class meta
       #verbose_name = 'Gastos'
        #verbose_name_plural = 'Gastos'          


#------ ENTIDAD GESTION DE MANTENIMIENTO --------2
class Mantenimiento(models.Model):
    fallas = models.TextField()
    procesos = models.CharField(max_length=50)
    id_vehiculo = models.ForeignKey(Vehiculo, on_delete=models.PROTECT)
    id_empleado = models.ForeignKey(Profile, on_delete=models.PROTECT, db_column='id_usuario_id')
    id_tipo_mantenimiento = models.ForeignKey(TipoMantenimiento, on_delete=models.PROTECT)
    estado = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.fallas} - {self.id_tipo_mantenimiento}"

    
#------------Modulo Informes-----------
    
    
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
    id_proveedor = models.ForeignKey(Proveedores, on_delete=models.PROTECT)
    id_herramienta = models.ForeignKey(Herramienta, on_delete=models.PROTECT)
    id_insumos = models.ForeignKey(Insumos, on_delete=models.PROTECT)
    id_repuesto = models.ForeignKey(Repuesto, on_delete=models.PROTECT)
    estado = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.id_pago} {self.monto}"

# ----- modulo detalle servicio  ---------
class DetalleServicio(models.Model):
    PROCESO_OPCIONES = [
        ('terminado', 'Terminado'),
        ('proceso', 'En proceso'),
    ]
    id_vehiculo = models.ForeignKey(Vehiculo, on_delete=models.PROTECT,related_name="servicios")
    cliente = models.ForeignKey(Cliente,on_delete=models.PROTECT)
    id_entrada = models.ForeignKey(EntradaVehiculo, on_delete=models.PROTECT, blank=True, null=True)
    empresa = models.ForeignKey('Empresa', on_delete=models.PROTECT, blank=True, null=True)
    empleado = models.ForeignKey(Profile, on_delete=models.PROTECT, blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    id_salida = models.ForeignKey(SalidaVehiculo, on_delete=models.PROTECT, blank=True, null=True)
    proceso = models.CharField(max_length=20, choices=PROCESO_OPCIONES, default='proceso')
    estado = models.BooleanField(default=True)

    #class Meta:
        #verbose_name = "Detalle de Servicio"
        #verbose_name_plural = "Detalles de Servicio"

    # ---------- TOTALES ----------
    @property
    def total_repuestos(self):
        return sum(
            d.subtotal for d in self.detallerepuesto_set.all()
        )

    @property
    def total_mantenimientos(self):
        return sum(
            d.subtotal for d in self.detalletipomantenimiento_set.all()
        )

    @property
    def total_insumos(self):
        return sum(
            d.subtotal for d in self.detalleinsumos_set.all()
        )

    @property
    def subtotal(self):
        return (
            self.total_repuestos +
            self.total_mantenimientos +
            self.total_insumos
        )

    @property
    def total_items(self):
        return (
            self.detallerepuesto_set.count() +
            self.detalletipomantenimiento_set.count() +
            self.detalleinsumos_set.count()
        )

    def __str__(self):
        return f"Servicio #{self.id} - {self.id_vehiculo.placa}"

class DetalleRepuesto(models.Model):
    detalle_servicio = models.ForeignKey(DetalleServicio, on_delete=models.PROTECT)
    id_repuesto = models.ForeignKey(Repuesto, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    precio_unitario = models.PositiveIntegerField(validators=[validar_monto])
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    @property
    def subtotal(self):
        return self.cantidad * self.precio_unitario
    
    def __str__(self):
        return f"Repuesto: {self.id_repuesto.nombre} - Cantidad: {self.cantidad}"
    

class DetalleTipoMantenimiento(models.Model):
    detalle_servicio = models.ForeignKey(DetalleServicio, on_delete=models.PROTECT)
    id_tipo_mantenimiento = models.ForeignKey(TipoMantenimiento, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    precio_unitario = models.PositiveIntegerField(validators=[validar_monto])
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    def save(self, *args, **kwargs):
        self.subtotal = self.cantidad * self.precio_unitario
        super().save(*args, **kwargs)

    

    def __str__(self):
        return f"Mantenimiento: {self.id_tipo_mantenimiento.nombre}"

class DetalleInsumos(models.Model):
    detalle_servicio = models.ForeignKey(DetalleServicio, on_delete=models.PROTECT)
    id_insumos = models.ForeignKey(Insumos, on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    precio_unitario = models.PositiveIntegerField(validators=[validar_monto])
    #subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    @property
    def subtotal(self):
        return self.cantidad * self.precio_unitario
    
    def __str__(self):
        return f"Insumo: {self.id_insumos} - Cantidad: {self.cantidad}"
    
 #-----Empresa----------------------
class Empresa(models.Model):
    nombre = models.CharField(max_length=255,default= "Taller Mecanica Diesel Internacional Arturo Patiño"  )
    nit = models.CharField(max_length=50,default="74.187366-2",validators=[nit_validator])
    direccion =  models.CharField(default="calle 9 #32-37 Barrio La Isla", max_length=200)
    telefono = models.CharField(default="3118112714 - 3133342841", max_length=50)
    estado = models.BooleanField(default=True) 

    
    def __str__(self):
        return f"{self.nombre} - {self.nit} en {self.direccion} {self.telefono}"   
    
class Informes(models.Model):
    id_informe = models.AutoField(primary_key=True)
    detalle_servicio = models.OneToOneField(DetalleServicio, on_delete=models.PROTECT, verbose_name="Detalle de Servicio")
    id_empleado = models.ForeignKey(Profile, on_delete=models.PROTECT, verbose_name="Mecánico Responsable")
    fecha = models.DateField(auto_now_add=True)
    hora = models.TimeField(auto_now_add=True)
    tipo_informe = models.CharField(max_length=20, choices=[('Preventivo', 'Preventivo'), ('Correctivo', 'Correctivo')])
    costo_mano_obra = models.PositiveIntegerField(validators=[validar_monto], verbose_name="Costo Mano de Obra")
    total_repuestos = models.PositiveIntegerField(default=0, editable=False)
    total_insumos = models.PositiveIntegerField(default=0, editable=False)
    total_final = models.PositiveIntegerField(default=0, editable=False)
    diagnostico_final = models.TextField(blank=True, null=True, verbose_name="Notas del Mecánico")
    estado = models.BooleanField(default=True)

    def __str__(self):
        return f"Informe {self.id_informe} - {self.detalle_servicio.id_vehiculo.placa}"
    
    def save(self, *args, **kwargs):
        if self.detalle_servicio:
            self.total_repuestos = self.detalle_servicio.total_repuestos
            self.total_insumos = self.detalle_servicio.total_insumos
            self.total_final = self.total_repuestos + self.total_insumos + self.costo_mano_obra
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Informe {self.id_informe} - {self.id_mantenimiento.id_vehiculo}"
    
    def save(self, *args, **kwargs):
    # Esto asegura que antes de guardar, se traigan los totales reales
        if self.detalle_servicio:
            self.total_repuestos = self.detalle_servicio.total_repuestos
            self.total_insumos = self.detalle_servicio.total_insumos
            # Sumamos los totales de productos más la mano de obra manual
            self.total_final = self.total_repuestos + self.total_insumos + self.costo_mano_obra
        super().save(*args, **kwargs)
#-----------Factura-----------------
class Factura(models.Model):
    METODO_PAGO = [
        ('efectivo', 'Efectivo'),
        ('transferencia', 'Transferencia'),
    ]
    ORDEN_SERVICIO_OPCIONES = [
        ('mantenimiento', 'Mantenimiento'),
        ('repuestos', 'Repuestos'),
        ('insumos', 'Insumos'),
    ]
    # USAR MINÚSCULAS AQUÍ:
    empresa = models.ForeignKey(Empresa, on_delete=models.PROTECT)
    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT)
    empleado = models.ForeignKey(Profile, on_delete=models.PROTECT)
    detalle_servicio = models.OneToOneField(DetalleServicio, on_delete=models.PROTECT, related_name="factura")
    
    fecha = models.DateField(auto_now_add=True)
    orden_servicio = models.CharField(max_length=20, choices=ORDEN_SERVICIO_OPCIONES)
    metodo_pago = models.CharField(max_length=50, choices=METODO_PAGO)
    estado = models.BooleanField(default=True)

    @property
    def subtotal(self):
        return self.detalle_servicio.subtotal if self.detalle_servicio else 0

    def __str__(self):
        return f"Factura #{self.id} - {self.cliente.nombre}"



    
#--------------Modulo Compra (STEVEN)-----------------
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
    estado = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.tipo_movimiento} - {self.monto} en {self.fecha} {self.hora}"   
    #class meta
        #verbose_name = 'Caja'
        #verbose_name_plural = 'Caja'")