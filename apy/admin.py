from django.contrib import admin
from apy.models import *
from apy.models import (
    EntradaVehiculo, TipoMantenimiento, SalidaVehiculo, 
    Cliente, Vehiculo, 
    # ¡Añade Module aquí!
    Module 
)
admin.site.register(EntradaVehiculo)
admin.site.register(TipoMantenimiento)
admin.site.register(SalidaVehiculo)
admin.site.register(Cliente)
admin.site.register(Vehiculo)

# Registra el modelo Module
@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('name',) 