# apy/migrations/0002_create_initial_modules.py 

from django.db import migrations
from django.db.models import F
from django.db import models


# Función que contiene la lógica para crear los registros de Module
def create_initial_modules(apps, schema_editor):
    Module = apps.get_model('apy', 'Module')

    print("\nCreando 21 módulos iniciales del sistema...") # Ajustar conteo si es necesario
    
    # ----------------------------------------------------
    # Módulos de Clientes y Movimiento (STEVEN)
    # ----------------------------------------------------
    Module.objects.get_or_create(name='Clientes', defaults={'description': 'Gestión de información de clientes.'})
    Module.objects.get_or_create(name='Vehiculos', defaults={'description': 'Gestión de la flota de vehículos.'})
    # CORRECCIÓN DE ESPACIOS
    Module.objects.get_or_create(name='Entrada Vehiculo', defaults={'description': 'Registro de ingreso de vehículos al taller.'})
    Module.objects.get_or_create(name='Salida Vehiculo', defaults={'description': 'Registro de egreso y diagnóstico de vehículos.'})
    # MÓDULO GASTOS AÑADIDO Y CAJA SEPARADA
    Module.objects.get_or_create(name='Caja', defaults={'description': 'Registro de movimientos de caja (Ingresos/Gastos).'})
    Module.objects.get_or_create(name='Gastos', defaults={'description': 'Registro y gestión de gastos'}) # Nuevo Módulo de Gastos
    Module.objects.get_or_create(name='Compra', defaults={'description': 'Registro de las compras a proveedores.'})

    # ----------------------------------------------------
    # Módulos de Mantenimiento e Inventario (ERICK)
    # ----------------------------------------------------
    # CORRECCIÓN DE ESPACIOS
    Module.objects.get_or_create(name='Tipo Mantenimiento', defaults={'description': 'Definición de tipos de mantenimiento (ej: cambio de aceite).'})
    Module.objects.get_or_create(name='Mantenimiento', defaults={'description': 'Gestión de fallas y procesos de reparación de vehículos.'})
    Module.objects.get_or_create(name='Marca', defaults={'description': 'Gestión de marcas de repuestos y herramientas.'})
    Module.objects.get_or_create(name='Repuestos', defaults={'description': 'Gestión del inventario de repuestos.'})
    Module.objects.get_or_create(name='Herramientas', defaults={'description': 'Gestión del inventario de herramientas.'})
    Module.objects.get_or_create(name='Insumos', defaults={'description': 'Gestión del inventario de insumos (líquidos, etc.).'})
    Module.objects.get_or_create(name='Informes', defaults={'description': 'Generación y consulta de informes de mantenimiento.'})

    # ----------------------------------------------------
    # Módulos Financieros y Administrativos (KAROL)
    # ----------------------------------------------------
    Module.objects.get_or_create(name='Administradores', defaults={'description': 'Gestión de administradores/gerentes.'})
    Module.objects.get_or_create(name='Empleados', defaults={'description': 'Gestión de información del personal.'})
    Module.objects.get_or_create(name='Nomina', defaults={'description': 'Gestión y registro de pagos de nómina.'})
    Module.objects.get_or_create(name='Proveedores', defaults={'description': 'Gestión de información de proveedores.'})
    Module.objects.get_or_create(name='Pagos', defaults={'description': 'Registro de pagos a proveedores y otros egresos.'})
    # CORRECCIÓN DE ESPACIOS
    Module.objects.get_or_create(name='Servicios Públicos', defaults={'description': 'Registro de pagos de servicios públicos (Luz, Agua, Gas).'})
    Module.objects.get_or_create(name='Facturación', defaults={'description': 'Generación y consulta de facturas a clientes.'})


class Migration(migrations.Migration):

    dependencies = [
        ('apy', '0001_initial'), 
    ]

    operations = [
        # ==========================================================
        # 1. PASO CRUCIAL: AGREGAR EL CAMPO A LA BASE DE DATOS
        # ==========================================================
        migrations.AddField(
            model_name='module',
            name='description',
            # **IMPORTANTE**: Ajusta este campo para que coincida exactamente
            # con la definición de 'description' en tu models.py, por ejemplo:
            field=models.TextField(verbose_name='Descripción', blank=True, default=''), 
            # Si tu models.py lo tiene con 'null=True' o sin 'default', úsalo.
        ),
        
        # ==========================================================
        # 2. PASO: EJECUTAR EL CÓDIGO PYTHON (AHORA LA COLUMNA EXISTE)
        # ==========================================================
        migrations.RunPython(create_initial_modules, migrations.RunPython.noop),
    ]