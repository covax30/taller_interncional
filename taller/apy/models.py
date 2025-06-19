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
    id_insumos = models.ForeignKey(Insumo, on_delete=models.CASCADE)
    id_repuestos = models.ForeignKey(Repuesto, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.id_pago} {self.monto}"