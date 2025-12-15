from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('apy', '0001_initial'),   # o la migración previa que tengas
    ]

    operations = [
        migrations.AddField(
            model_name='vehiculo',
            name='estado',
            field=models.BooleanField(default=True, verbose_name='Activo'),
        ),
    ]
