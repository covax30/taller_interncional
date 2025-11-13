
# Asegura que la aplicación Celery se importe cuando se inicia Django.
from .celery import app as celery_app

__all__ = ('celery_app',)