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
