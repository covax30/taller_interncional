from django.db import models


class TipoMantenimiento(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre
        
#------ ENTIDAD PRODUCTO ---------
class Equipo(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    ubicacion = models.CharField(max_length=100)
    fecha_adquisicion = models.DateField()
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

class Mantenimiento(models.Model):
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE)
    tipo = models.ForeignKey(TipoMantenimiento, on_delete=models.SET_NULL, null=True)
    fecha = models.DateField()
    descripcion = models.TextField()
    realizado_por = models.CharField(max_length=100)
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.equipo.nombre} - {self.fecha}"
    
class Repuesto(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True)
    stock = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.nombre} ({self.codigo})"
    
#------- Gastos-------- ya esta subido
class Gastos(models.Model):
    id_gasto =  models.AutoField(primary_key = True)  #ID automatico
    monto= models,models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField() 
    tipo_gastos=models.CharField(max_length=100)
          
           