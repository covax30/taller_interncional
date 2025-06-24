from django.db import models

# MODULOS STEVEN

class Cliente(models.Model):
    id_cliente = models.IntegerField(unique=True)  
    id_operacion = models.IntegerField(default=0)
    nombre = models.CharField(max_length=100)
    documento = models.BigIntegerField(default=0)
    telefono = models.BigIntegerField(default=0)
    correo = models.EmailField(max_length=100)
    fecha_operacion = models.DateField()
    monto = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.id_cliente} - {self.nombre}"


class Vehiculo(models.Model):
    id_vehiculo = models.IntegerField(unique=True) 
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)  # LLAVE
    placa = models.CharField(max_length=10, unique=True)
    modelo_vehiculo = models.CharField(max_length=100)
    marca_vehiculo = models.CharField(max_length=100)
    color = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.placa} - {self.marca_vehiculo} - {self.modelo_vehiculo}"


class EntradaVehiculo(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)  # LLAVE
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)  # LLAVE
    fecha_ingreso = models.DateField()
    hora_ingreso = models.TimeField()

    def __str__(self):
        return f"{self.cliente.id_cliente} - {self.vehiculo.placa} - {self.fecha_ingreso} {self.hora_ingreso}"


class SalidaVehiculo(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)  # LLAVE
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)  # LLAVE
    diagnostico = models.CharField(max_length=100)
    fecha_ingreso = models.DateField()
    hora_ingreso = models.TimeField()

    def __str__(self):
        return f"{self.cliente.id_cliente} - {self.vehiculo.placa} - {self.diagnostico}"


class Compra(models.Model):
    id_factura_compra = models.IntegerField(unique=True)
    id_compra = models.IntegerField(default=0)
    proveedor = models.CharField(max_length=100)
    fecha_compra = models.DateField()
    hora_compra = models.TimeField()

    def __str__(self):
        return f"{self.id_factura_compra} - {self.proveedor} - {self.fecha_compra} {self.hora_compra}"
#------ MODULOS ERICK ---------
#------ ENTIDAD de TIPO mantenmimiento ---------
class TipoMantenimiento(models.Model):
    id = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nombre
        
#------ ENTIDAD PRODUCTO --------
class Mantenimiento(models.Model):
    fallas = models.TextField()
    procesos = models.CharField(max_length=50)
    id_vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    id_empleado = models.ForeignKey(empleado, on_delete=models.CASCADE)
    id_tipo_mantenimiento = models.ForeignKey(TipoMantenimiento, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.fallas} - {self.id_tipo_mantenimiento}"
    #------ ENTIDAD repuestos --------
class Repuesto(models.Model):
    id_marca = models.ForeignKey(marca, on_delete=models.CASCADE)
    categoria = models.CharField(max_length=100)
    fabricante = models.CharField(max_length=100)
    stock = models.IntegerField(default=0)
    ubicacion = models.CharField(max_length=100)
    precio = models.IntegerField(default=0)
    
    def __str__(self):
<<<<<<<<< Temporary merge branch 1
        return f"{self.nombre} ({self.codigo})"  
    
#-------------Modulo Administrador-----------
class Administrador:
    id_admin = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    identificacion = models.CharField(max_length=20, unique=True)
    edad = models.IntegerField()
    correo = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20)
    fecha_ingreso = models.DateField()
    
    def __str__(self):
        return f"{self.nombre} {self.apellidos}"
    
#------- Gastos--------
class Gastos(models.Model):
    id_gasto =  models.AutoField(primary_key = True)  #ID automatico
    monto= models,models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField() 
    tipo_gastos=models.CharField(max_length=100)
             
#------------Modulo Informes-----------
class Informes:
    id_informe = models.AutoField(primary_key=True)
    repuestos_usados = models.TextField()
    costo_mano_obra = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField()
    hora = models.TimeField()
    id_repuesto = models.ForeignKey(Repuesto, on_delete=models.CASCADE)
    id_empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    tipo_informe = models.CharField(max_length=100)
    id_mantenimiento = models.ForeignKey(Mantenimiento, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.id_informe} {self.tipo_informe}"
    
class Herramienta(models.Model):
    id = models.CharField(max_length=50, unique=True)
    marca = models.CharField(max_length=50)
=========
        return f"{self.fabricante} ({self.categoria})"

class herramienta(models.Model):
>>>>>>>>> Temporary merge branch 2
    nombre = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    tipo = models.CharField(max_length=100)
    material = models.CharField(max_length=100)
    id_marca = models.ForeignKey(marca, on_delete=models.CASCADE)
    stock = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.nombre} ({self.tipo})"

<<<<<<<<< Temporary merge branch 1
class Insumos(models.Model):
    id = models.IntegerField()
=========
class insumos(models.Model):
>>>>>>>>> Temporary merge branch 2
    id_marca = models.CharField(max_length=50)
    nombre = models.CharField(max_length=100)
    costo = models.IntegerField()
    tipo = models.CharField(max_length=100)
    stock = models.IntegerField(default=0)

    def __str__(self):
<<<<<<<<< Temporary merge branch 1
        return f"{self.nombre} ({self.id})"
    
#--------------Modulo Pago Servicio Publicos-----------
class PagoServiciosPublicos:
    id_servicio = models.AutoField(primary_key=True)
    monto = models,models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.id_servicio} {self.monto}"
    
#--------------Modulo Proveedores--------------
class Proveedores:
    id_proveedor = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    correo = models.EmailField(unique=True)
    
    def __str__(self):
        return f"{self.id_proveedor} {self.correo}"
    
#--------------Modulo Pagos-----------------
class Pagos:
    id_pago = models.AutoField(primary_key=True)
    tipo_pago = models.CharField(max_length=100)
    fecha = models.DateField()
    hora = models.TimeField()
    monto = models,models.DecimalField(max_digits=10, decimal_places=2)
    id_proveedor = models.ForeignKey(Proveedores, on_delete=models.CASCADE)
    id_admin = models.ForeignKey(Administrador, on_delete=models.CASCADE)
    id_herramienta = models.ForeignKey(Herramienta, on_delete=models.CASCADE)
    id_insumos = models.ForeignKey(Insumos, on_delete=models.CASCADE)
    id_repuestos = models.ForeignKey(Repuesto, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.id_pago} {self.monto}"


=========
        return f"{self.nombre} ({self.stock})"
>>>>>>>>> Temporary merge branch 2
