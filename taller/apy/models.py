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
    
class Repuesto(models.Model):
    id_marca = models.ForeignKey(marca, on_delete=models.CASCADE)
    categoria = models.CharField(max_length=100)
    fabricante = models.CharField(max_length=100)
    stock = models.IntegerField(default=0)
    ubicacion = models.CharField(max_length=100)
    precio = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.fabricante} ({self.categoria})"

class herramienta(models.Model):
    nombre = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    tipo = models.CharField(max_length=100)
    material = models.CharField(max_length=100)
    id_marca = models.ForeignKey(marca, on_delete=models.CASCADE)
    stock = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.nombre} ({self.tipo})"

class insumos(models.Model):
    id_marca = models.CharField(max_length=50)
    nombre = models.CharField(max_length=100)
    costo = models.IntegerField()
    tipo = models.CharField(max_length=100)
    stock = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.nombre} ({self.stock})"
