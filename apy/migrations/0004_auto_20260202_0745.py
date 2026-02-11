from django.db import migrations

def cargar_empresa_defecto(apps, schema_editor):
    Empresa = apps.get_model('apy', 'Empresa')
    # Solo lo crea si no existe ninguna empresa ya registrada
    if not Empresa.objects.exists():
        Empresa.objects.create(
            nombre="Taller Mecanica Diesel Internacional Arturo Patiño",
            nit="74.187366-2",
            direccion="calle 9 #32-37 Barrio La Isla",
            telefono="3118112714 - 3133342841"
        )

class Migration(migrations.Migration):
    dependencies = [
        ('apy', '0003_alter_cliente_identificacion'),
    ]

    operations = [
        migrations.RunPython(cargar_empresa_defecto),
    ]