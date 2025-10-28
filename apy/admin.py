from django.contrib import admin
from apy.models import *
from apy.models import (
    EntradaVehiculo, TipoMantenimiento, Empleado, SalidaVehiculo, 
    Cliente, Vehiculo, Mantenimiento, 
    # ¡Añade Module aquí!
    Module 
)
admin.site.register(EntradaVehiculo)
admin.site.register(TipoMantenimiento)
admin.site.register(Empleado)
admin.site.register(SalidaVehiculo)
admin.site.register(Cliente)
admin.site.register(Vehiculo)
admin.site.register(Mantenimiento)

# Registra el modelo Module
@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('name',) 