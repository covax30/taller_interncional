from .settings import *

DEBUG = True

# SQLite en memoria: rápido, sin Docker, sin MySQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    },
    'log_db': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

# Axes desactivado para no bloquear usuarios en tests
AXES_ENABLED = False

# Hasher rápido para tests
PASSWORD_HASHERS = ['django.contrib.auth.hashers.MD5PasswordHasher']

RECAPTCHA_PUBLIC_KEY = '6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI'
RECAPTCHA_PRIVATE_KEY = '6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe'