from django.contrib import admin
from .models import Repuesto, Insumos,Herramienta
# Register your models here.

admin.site.register(Repuesto)
admin.site.register(Insumos)
admin.site.register(Herramienta)