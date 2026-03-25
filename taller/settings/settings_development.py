from .settings import *

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Silencia warning de reCAPTCHA con keys de prueba
SILENCED_SYSTEM_CHECKS = ['django_recaptcha.recaptcha_test_key_error']

# Correo en consola
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Sin compresión de estáticos
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

# Evita error si no existe la carpeta static
STATICFILES_DIRS = [d for d in STATICFILES_DIRS if os.path.exists(d)]