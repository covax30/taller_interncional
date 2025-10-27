# taller/celery.py

import os
from celery import Celery

# 1. Establece el módulo de configuración de Django para el programa 'celery'.
# Se asegura de que Celery utilice la configuración que acabas de definir en settings.py.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taller.settings')

# 2. Crea la instancia de la aplicación Celery.
# El nombre de la aplicación puede ser el nombre del proyecto, 'taller'.
app = Celery('taller')

# 3. Carga la configuración de Celery desde la configuración de Django (settings.py).
# Esto usa todas las variables CELERY_XXXX que definiste.
app.config_from_object('django.conf:settings', namespace='CELERY')

# 4. Descubre automáticamente las tareas en los archivos 'tasks.py' de todas tus apps.
# Celery buscará el archivo 'tasks.py' en la carpeta 'apy' (donde crearás las tareas de respaldo).
app.autodiscover_tasks()


# Tarea de prueba opcional (para verificar que Celery funciona)
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')# taller/celery.py

import os
from celery import Celery

# 1. Establece el módulo de configuración de Django para el programa 'celery'.
# Se asegura de que Celery utilice la configuración que acabas de definir en settings.py.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taller.settings')

# 2. Crea la instancia de la aplicación Celery.
# El nombre de la aplicación puede ser el nombre del proyecto, 'taller'.
app = Celery('taller')

# 3. Carga la configuración de Celery desde la configuración de Django (settings.py).
# Esto usa todas las variables CELERY_XXXX que definiste.
app.config_from_object('django.conf:settings', namespace='CELERY')

# 4. Descubre automáticamente las tareas en los archivos 'tasks.py' de todas tus apps.
# Celery buscará el archivo 'tasks.py' en la carpeta 'apy' (donde crearás las tareas de respaldo).
app.autodiscover_tasks()


# Tarea de prueba opcional (para verificar que Celery funciona)
@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')