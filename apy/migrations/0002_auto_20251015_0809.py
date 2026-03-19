# apy/migrations/0002_create_initial_modules.py
from django.db import migrations

def manage_modules(apps, schema_editor):
    Module = apps.get_model('apy', 'Module')
    
    # Lista Maestra: (Nombre Técnico, Descripción para el usuario)
    modulos_maestros = [
        ('EstadisticasGenerales', 'Dashboard y métricas de rendimiento.'),
        ('Informes', 'Reportes detallados del sistema.'),
        ('EntradaVehiculos', 'Registro de ingreso de vehículos.'),
        ('SalidaVehiculos', 'Registro de salida de vehículos.'),
        ('Vehiculos', 'Administración de la flota.'),
        ('Marca', 'Gestión de marcas de vehículos.'),
        ('GestionMantenimiento', 'Control de servicios técnicos.'),
        ('Repuestos', 'Inventario y stock de repuestos.'),
        ('TipoMantenimientos', 'Categorías de servicio.'),
        ('Herramientas', 'Control de inventario de herramientas.'),
        ('Insumos', 'Control de materiales y suministros.'),
        ('Gastos', 'Registro de egresos operativos.'),
        ('Factura', 'Gestión de facturación (Detalle de Servicio).'),
        ('Pagos', 'Registro de transacciones y abonos.'),
        ('Caja', 'Control de flujo de caja diario.'),
        ('PagoServicios', 'Pagos de servicios del local.'),
        ('Proveedor', 'Administración de proveedores.'),
        ('Clientes', 'Base de datos de clientes.'),
        ('GestionUsuarios', 'Administración de cuentas de acceso.'),
        ('Permisos', 'Gestión de privilegios por módulo.'),
        ('Respaldos', 'Ejecución de backups de base de datos.')
    ]

    nombres_nuevos = [m[0] for m in modulos_maestros]
    # Eliminamos lo que no esté en la lista para evitar duplicados con espacios
    Module.objects.exclude(name__in=nombres_nuevos).delete()

    for nombre, desc in modulos_maestros:
        Module.objects.update_or_create(
            name=nombre, 
            defaults={'description': desc}
        )

class Migration(migrations.Migration):
    dependencies = [('apy', '0001_initial')]
    operations = [
        migrations.RunPython(manage_modules, reverse_code=migrations.RunPython.noop),
    ]