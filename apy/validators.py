import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class ComplexPasswordValidator:
    def validate(self, password, user=None):
        # Usamos palabras clave consistentes para que el JS las atrape
        if not re.findall('[A-Z]', password):
            raise ValidationError(
                _("La contraseña debe contener al menos una letra MAYÚSCULA."),
                code='password_no_upper',
            )
        if not re.findall('[0-9]', password):
            raise ValidationError(
                _("La contraseña debe contener al menos un NÚMERO."),
                code='password_no_number',
            )
        if not re.findall('[()[\]{}|\\`~!@#$%^&*_\-+=;:\'\",<>./?]', password):
            raise ValidationError(
                _("La contraseña debe contener al menos un carácter ESPECIAL (@, #, $, etc.)."),
                code='password_no_symbol',
            )

    def get_help_text(self):
        return _("Tu contraseña debe incluir mayúsculas, números y caracteres especiales.")

def solo_letras_validator(value):
    if value:
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', value):
            raise ValidationError('Error: Solo se permiten letras en este campo.')
        
def telefono_validator(value):
    if value:
        # Acepta opcionalmente +, seguido de 7 a 15 números (estándar internacional)
        # O simplemente 10 dígitos si es local
        if not re.match(r'^\+?(\d{7,15})$', value):
            raise ValidationError(
                'El teléfono debe contener entre 7 y 15 dígitos y solo números.'
            )