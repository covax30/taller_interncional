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
   
    monto= models,models.DecimalField(max_digits=10, decimal_places=2)
    descripcion = models.TextField() 
    tipo_gastos=models.CharField(max_length=100,  unique=True)
    id_pagos_servicios = models.ForeignKey(Pago_servicios, on_delete=models.SET_NULL, null=True)
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
    def __str__(self):
        return f"{self.nombre} ({self.identificacion})"
    #class meta
        #verbose_name = 'Empleado'
        #verbose_name_plural = 'Empleado'
    
#-------- nomina------
class Nomina(models.Model):
   
    rol = models.CharField(max_length=100,  unique=True) 
    monto= models.DecimalField(max_digits=10, decimal_places=2) 
    fecha_pago =  models.DateField() 
    id_empleado =   models.ForeignKey(Empleado, on_delete=models.SET_NULL, null=True)            
    def __str__(self):
        return f"{self.rol} - ${self.monto} - {self.fecha_pago}"
     #class meta
        #verbose_name = 'Nomina'
        #verbose_name_plural = 'Nomina'
    
    
#-----------Caja-----------------
class Caja(models.Model):
   
    tipo_movimiento= models.CharField(max_length=50)
    monto= models.DecimalField(max_digits=10, decimal_places=2)
    fecha= models.DateField()
    hora=models.TimeField()
    id_gasto= models.ForeignKey( Gastos , on_delete=models.CASCADE, null=True, blank=True )
    id_admin=models.ForeignKey(Administrador, on_delete=models.CASCADE, null=True, blank=True) 
    id_Factura= models.ForeignKey(Factura, on_delete=models.CASCADE, null=True, blank=True)
    id_pagos= models.ForeignKey(Pago, on_delete=models.CASCADE, null=True, blank=True)
    id_nomina= models.ForeignKey(Nomina, on_delete=models.CASCADE, null=True, blank=True) 
    def __str__(self):
        return f"{self.tipo_movimiento} - {self.monto} en {self.fecha} {self.hora}"   
    #class meta
        #verbose_name = 'Caja'
        #verbose_name_plural = 'Caja'