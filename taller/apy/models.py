from django.db import models


class TipoMantenimiento(models.Model):
    id = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre
        
#------ ENTIDAD PRODUCTO ---------

class Mantenimiento(models.Model):
    equipo = models.ForeignKey( on_delete=models.CASCADE)
    tipo = models.ForeignKey(TipoMantenimiento, on_delete=models.SET_NULL, null=True)
    fecha = models.DateField()
    descripcion = models.TextField()
    realizado_por = models.CharField(max_length=100)
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.equipo.nombre} - {self.fecha}"
    
class Repuesto(models.Model):
    id = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    stock = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.nombre} ({self.codigo})"










































class herramienta(models.Model):
    id = models.CharField(max_length=50, unique=True)
    marca = models.CharField(max_length=50)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    stock = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.nombre} ({self.id})"

class insumos(models.Model):
    id = models.IntegerField()
    id_marca = models.CharField(max_length=50)
    nombre = models.CharField(max_length=100)
    costo = models.IntegerField()
    tipo = models.CharField(max_length=100)
    stock = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.nombre} ({self.id})"