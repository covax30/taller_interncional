import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class ComplexPasswordValidator:
    def validate(self, password, user=None):
        if not re.findall('[A-Z]', password):
            raise ValidationError(
                _("La contraseña debe contener al menos una letra mayúscula."),
                code='password_no_upper',
            )
        if not re.findall('[0-9]', password):
            raise ValidationError(
                _("La contraseña debe contener al menos un número."),
                code='password_no_number',
            )
        if not re.findall('[()[\]{}|\\`~!@#$%^&*_\-+=;:\'\",<>./?]', password):
            raise ValidationError(
                _("La contraseña debe contener al menos un carácter especial (@, #, $, etc.)."),
                code='password_no_symbol',
            )

    def get_help_text(self):
        return _("Tu contraseña debe incluir mayúsculas, números y caracteres especiales.")