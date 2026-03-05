from pyexpat.errors import messages
from django import forms
from django.forms import ModelForm, Select, NumberInput, DateInput, TimeInput, TextInput, EmailInput
from django.forms import inlineformset_factory
from decimal import Decimal, InvalidOperation
from django.contrib.auth.hashers import make_password
from django import forms
from django.contrib.auth.models import User, Permission
from django.core.exceptions import ValidationError
from .models import Profile,DetalleServicio
from .validators import solo_letras_validator, ComplexPasswordValidator, telefono_validator
from django.contrib.auth.password_validation import validate_password
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox

from apy.models import *
        
class ContactoForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre completo'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}))
    subject = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Asunto'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Mensaje', 'rows': 5}))
    
    # AQUÍ ESTÁ EL CUADRITO
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

class EmpresaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',  
                'autocomplete': 'off'
            })
        
        self.fields['nombre'].widget.attrs.update({'autofocus': True})
    
    class Meta:
        model = Empresa
        fields = ['nombre', 'nit', 'direccion', 'telefono']  
        widgets = {
            'nombre': TextInput(
                attrs={
                    'class': 'form-control'
                    }),
            'nit': TextInput(
                attrs={
                    'class': 'form-control', 'min': '1'
                    }),
            'direccion': TextInput(
                attrs={
                    'class': 'form-control', 'placeholder': '0.00', 'step': '0.01'
                    }),
            'telefono': NumberInput(
                attrs={
                    'class': 'form-control', 'min': '1'
                    }),
        }
        
        error_messages = {
            'nombre': {
                'required': 'El nombre de la empresa  es obligatorio',
            },
            'nit': {
                'required': 'El Número de Identificación Tributaria es oblicatorio',
            },
            'direccion ': {
                'required': 'La direccion de la empresa es  obligatorio',
            },
            'telefono': {
                'required': 'El telefono de la empresa es  obligatorio',
            }
        }

class RepuestoscantidadForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_repuesto'].queryset = Repuesto.objects.all()
        self.fields['id_repuesto'].widget.attrs.update({
            'class': 'form-control',
            'autofocus': True
        })

    class Meta:
        model = DetalleRepuesto
        fields = ['id_repuesto', 'cantidad', 'precio_unitario']
        widgets = {
            'id_repuesto': Select(attrs={'class': 'form-control'}),
            'cantidad': NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'precio_unitario': NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el precio unitario', 'step': '0.01'}),
        }
        
        error_messages = {
            'id_repuesto': {
                'required': 'El nombre del repuesto es obligatorio',
            },
            'cantidad': {
                'required': 'La cantidad del repuesto es obligatoria',
            },
            'precio_unitario': {
                'required': 'El costo del repuesto es obligatorio',
            }
        }

class DetalleTipo_MantenimientoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_tipo_mantenimiento'].queryset = TipoMantenimiento.objects.all()
        self.fields['id_tipo_mantenimiento'].widget.attrs.update({
            'class': 'form-control',
    })
    # Protección: solo configurar 'empleado' si ya existe en el form
        if 'empleado' in self.fields:
            self.fields['empleado'].queryset = Profile.objects.select_related('user').all()
            self.fields['empleado'].label_from_instance = (
                lambda obj: f"{obj.user.get_full_name() or obj.user.username}"
            )
            self.fields['empleado'].widget.attrs.update({'class': 'form-control'})
            self.fields['empleado'].required = False
    class Meta:
        model = DetalleTipoMantenimiento
        fields = ['id_tipo_mantenimiento', 'empleado', 'cantidad', 'precio_unitario']  # ← empleado añadido
        widgets = {
            'id_tipo_mantenimiento': Select(
                attrs={'class': 'form-control'}
            ),
            'empleado': Select(
                attrs={'class': 'form-control'}
            ),
            'cantidad': NumberInput(
                attrs={
                    'placeholder': 'Cantidad',
                    'class': 'form-control',
                    'min': '1'
                }
            ),
            'precio_unitario': NumberInput(
                attrs={
                    'placeholder': 'Precio unitario',
                    'step': '0.01',
                    'class': 'form-control',
                }
            ),
        }
        error_messages = {
            'id_tipo_mantenimiento': {'required': 'El tipo de mantenimiento es obligatorio'},
            'cantidad':              {'required': 'La cantidad es obligatoria'},
            'precio_unitario':       {'required': 'El precio unitario es obligatorio'},
        }


# ============================================================
# CAMBIO EN forms.py
# Busca DetalleTipoMantenimientoFormSet y reemplázalo con este:
# ============================================================

DetalleTipoMantenimientoFormSet = inlineformset_factory(
    DetalleServicio,
    DetalleTipoMantenimiento,
    form=DetalleTipo_MantenimientoForm,
    fields=('id_tipo_mantenimiento', 'empleado', 'cantidad', 'precio_unitario'),  # ← empleado añadido
    extra=1,
    can_delete=True
)

class DetalleInsumoForm(ModelForm):  
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_insumos'].queryset = Insumos.objects.all()
        self.fields['id_insumos'].widget.attrs.update({
            'class': 'form-control',
            'autofocus': True
        })
           
    class Meta:
        model = DetalleInsumos
        fields = ['id_insumos', 'cantidad', 'precio_unitario']
        widgets = {
            'id_insumos': Select(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el nombre del insumo',
                }
            ),
            'nombre': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el nombre del insumo',
                }
            ),
            'cantidad': NumberInput(
                attrs={
                    'placeholder': 'Ingrese la cantidad del insumo',
                }
            ),
            'precio_unitario': NumberInput(
                attrs={
                    'placeholder': 'Ingrese el precio unitario',
                    'step': '0.01',
                    'class': 'form-control',
                }
            )
        }
        error_messages = {
            'id_insumos': {
                'required': 'El nombre del insumo es obligatorio',
            },
            'cantidad': {
                'required': 'La cantidad del insumo es obligatoria',
            },
            'precio_unitario': {
                'required': 'El costo del insumo es obligatorio',
            }
        }

# Formulario detalle servicio
class DetalleServicioForm(ModelForm):
    class Meta:
        model = DetalleServicio
        fields = ['id_vehiculo','cliente','id_entrada','empresa','id_salida','proceso' , 'empleado']
        widgets = {
            'id_vehiculo': Select(attrs={
                'class': 'form-control',
                'placeholder': 'Seleccione un vehículo'
            }),
            'cliente': Select(attrs={
                'class': 'form-control',
                'placeholder': 'Seleccione un cliente'
            }),
            'id_entrada': Select(attrs={
                'class': 'form-control',
                'placeholder': 'Seleccione una entrada de vehículo'
            }),
            'empresa': Select(attrs={   
                'class': 'form-control',
                'placeholder': 'Seleccione una empresa'
            }),
            'empleado': Select(attrs={
                'class': 'form-control',
                'placeholder': 'Seleccione un empleado'
            }),
            
            'id_salida': Select(attrs={   
                'class': 'form-control',
                'placeholder': 'Seleccione una salida de vehículo'
            }),
            'proceso': Select(attrs={
                'class': 'form-control',
                'placeholder': 'Seleccione el proceso del servicio'
            }),
        }
        error_messages = {
            'id_vehiculo': {
                'required': 'El vehículo es obligatorio.',
            },
            'cliente': {
                'required': 'El cliente es obligatorio.',
            },
            'id_entrada': {
                'required': 'La entrada del vehículo es obligatoria.',
            },
            'empresa': {
                    'required': 'La empresa es obligatoria.',
                },
            
            'proceso': {
                    'required': 'El proceso del servicio es obligatorio.',
                },
        
            
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Configurar cómo se muestran los vehículos en el select
        self.fields['id_vehiculo'].label_from_instance = (
            lambda obj: f"{obj.placa} - {obj.marca_vehiculo} {obj.modelo_vehiculo} - {obj.color}"
        )

# Formsets definidos fuera de las clases
DetalleRepuestoFormSet = inlineformset_factory(
    DetalleServicio,
    DetalleRepuesto,
    form=RepuestoscantidadForm,
    fields=('id_repuesto', 'cantidad', 'precio_unitario'),
    extra=1, 
    can_delete=True
)

DetalleTipoMantenimientoFormSet = inlineformset_factory(
    DetalleServicio,
    DetalleTipoMantenimiento,
    form=DetalleTipo_MantenimientoForm,
    fields=('id_tipo_mantenimiento', 'cantidad', 'precio_unitario'),
    extra=1, 
    can_delete=True
)

DetalleInsumosFormSet = inlineformset_factory(
    DetalleServicio,
    DetalleInsumos,
    form=DetalleInsumoForm,
    fields=('id_insumos', 'cantidad', 'precio_unitario'),
    extra=1, 
    can_delete=True
)

  
        
# -----------Formulario modelo proveedor------------------        
class ProveedorForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs['autofocus'] = True

    class Meta:
        model = Proveedores
        exclude = ['estado']  # Excluimos el campo 'estado' para que no sea visible en el formulario
        fields = '__all__'
        widgets = {
            'nombre': TextInput(attrs={'placeholder': 'Ingrese el nombre'}),
            'telefono': TextInput(attrs={'placeholder': 'Ingrese el teléfono'}), # Cambiado a TextInput por si el tel tiene + o espacios
            'tipo_identificacion': Select(attrs={'class': 'form-control'}),
            'identificacion': TextInput(attrs={'placeholder': 'Ingrese el número de documento'}),
            'correo': EmailInput(attrs={'placeholder': 'Ingrese el correo'}),
        }
        # ... tus error_messages aquí ...

    def clean(self):
        """Validación personalizada que cruza tipo y número"""
        cleaned_data = super().clean()
        tipo = cleaned_data.get('tipo_identificacion')
        identificacion = cleaned_data.get('identificacion')

        if tipo and identificacion:
            valor = str(identificacion).strip().upper()
            
            # Definición de reglas por cada tipo del SELECT
            reglas = {
                'CC': (r'^\d{5,10}$', 'La Cédula debe tener entre 5 y 10 dígitos numéricos.'),
                'TI': (r'^\d{10,11}$', 'La Tarjeta de Identidad debe tener 10 u 11 dígitos.'),
                'RC': (r'^\d{10,11}$', 'El Registro Civil debe tener 10 u 11 dígitos.'),
                'NIT': (r'^\d{7,10}-\d{1}$', 'El NIT debe tener formato 123456789-0.'),
                'CE': (r'^\d{3,9}$', 'La Cédula de Extranjería debe ser numérica (hasta 9 dígitos).'),
                'PAS': (r'^[A-Z0-9]{5,20}$', 'El Pasaporte debe ser alfanumérico (5-20 caracteres).'),
                'PPT': (r'^[A-Z0-9]{4,15}$', 'El PPT debe ser alfanumérico.'),
            }

            if tipo in reglas:
                regex, mensaje = reglas[tipo]
                if not re.fullmatch(regex, valor):
                    # Agrega el error específicamente al campo 'identificacion'
                    self.add_error('identificacion', mensaje)
        
        return cleaned_data
        error_messages = {
            'nombre': {
                'required': 'El nombre del proveedor es obligatorio',
            },
            'telefono': {
                'required': 'El telefono del proveedor es obligatorio',
            },
            'correo': {
                'required': 'El correo del proveedor es obligatorio',
                'invalid': 'El correo no tiene un formato válido',
                'unique': 'Ya existe un cliente con ese correo',
            }
        }
        
# ------------------- FORMS STEVEN -------------------     
# ─────────────────────────────────────────────────────────────────────────────
# CONSTANTES DE VALIDACIÓN
# ─────────────────────────────────────────────────────────────────────────────
SOLO_LETRAS_RE       = re.compile(r'^[A-Za-záéíóúÁÉÍÓÚüÜñÑ\s\-]+$')
SOLO_NUMEROS_RE      = re.compile(r'^\d+$')
TELEFONO_RE          = re.compile(r'^\+?[\d\s\-]{7,15}$')
USERNAME_RE          = re.compile(r'^[\w.@+\-]+$')   # mismo patrón que Django, explicitado
IDENTIFICACION_MIN   = 5
IDENTIFICACION_MAX   = 20
TELEFONO_MIN         = 7
TELEFONO_MAX         = 15
USERNAME_MIN         = 3
USERNAME_MAX         = 150
NOMBRE_MIN           = 2
NOMBRE_MAX           = 50
PASSWORD_MIN         = 8
DIRECCION_MIN        = 5
DIRECCION_MAX        = 200
ROLES_VALIDOS        = {'normal', 'admin'}


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS INTERNOS
# ─────────────────────────────────────────────────────────────────────────────
def _validar_solo_letras(valor: str, nombre_campo: str) -> str:
    """Verifica que el valor solo contenga letras, espacios o guiones."""
    valor = valor.strip()
    if not valor:
        raise forms.ValidationError(f"El {nombre_campo} no puede estar vacío.")
    if len(valor) < NOMBRE_MIN:
        raise forms.ValidationError(
            f"El {nombre_campo} debe tener al menos {NOMBRE_MIN} caracteres."
        )
    if len(valor) > NOMBRE_MAX:
        raise forms.ValidationError(
            f"El {nombre_campo} no puede superar los {NOMBRE_MAX} caracteres."
        )
    if not SOLO_LETRAS_RE.match(valor):
        raise forms.ValidationError(
            f"El {nombre_campo} solo puede contener letras, espacios o guiones."
        )
    return valor


# ─────────────────────────────────────────────────────────────────────────────
# FORMULARIO PRINCIPAL: Registro / Edición de Usuario (por parte del Admin)
# ─────────────────────────────────────────────────────────────────────────────
class RegistroUsuarioForm(forms.ModelForm):

    # ── Campos extra no presentes en el modelo User ──────────────────────────
    old_password = forms.CharField(
        label='Contraseña Antigua',
        widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña actual'}),
        required=False,
    )

    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'}),
        strip=False,
        required=True,
    )

    password2 = forms.CharField(
        label='Confirmar Contraseña',
        widget=forms.PasswordInput(attrs={'placeholder': 'Repita la contraseña'}),
        strip=False,
        required=True,
    )

    role = forms.ChoiceField(
        label='Rol',
        choices=[('normal', 'Empleado'), ('admin', 'Gerente')],
        widget=forms.Select(),
        required=True,
    )

    tipo_identificacion = forms.ChoiceField(
        label='Tipo de Documento',
        choices=Profile.TIPO_DOC_CHOICES,
        widget=forms.Select(),
    )

    identificacion = forms.CharField(
        label='Identificación',
        required=True,
        widget=forms.TextInput(),
    )

    direccion = forms.CharField(
        label='Dirección',
        required=True,   # ← ahora obligatorio
        widget=forms.TextInput(),
    )

    telefono = forms.CharField(
        label='Teléfono',
        required=True,   # ← ahora obligatorio
        widget=forms.TextInput(),
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    # ── __init__ ──────────────────────────────────────────────────────────────
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            # En edición la contraseña es opcional
            self.fields['password'].required = False
            self.fields['password2'].required = False

            # Sincronizar rol
            self.initial['role'] = 'admin' if self.instance.is_superuser else 'normal'

            # Cargar datos del perfil
            try:
                perfil = self.instance.profile
                self.initial.update({
                    'tipo_identificacion': perfil.tipo_identificacion,
                    'identificacion':      perfil.identificacion,
                    'direccion':           perfil.direccion,
                    'telefono':            perfil.telefono,
                })
            except (Profile.DoesNotExist, AttributeError):
                pass

    # ── Validaciones de campo ─────────────────────────────────────────────────

    def clean_first_name(self):
        valor = self.cleaned_data.get('first_name', '')
        if not valor or not valor.strip():
            raise forms.ValidationError("El nombre es obligatorio.")
        return _validar_solo_letras(valor, 'nombre')

    def clean_last_name(self):
        valor = self.cleaned_data.get('last_name', '')
        if not valor or not valor.strip():
            raise forms.ValidationError("El apellido es obligatorio.")
        return _validar_solo_letras(valor, 'apellido')

    def clean_username(self):
        username = self.cleaned_data.get('username', '').strip()

        if not username:
            raise forms.ValidationError("El nombre de usuario es obligatorio.")
        if len(username) < USERNAME_MIN:
            raise forms.ValidationError(
                f"El nombre de usuario debe tener al menos {USERNAME_MIN} caracteres."
            )
        if len(username) > USERNAME_MAX:
            raise forms.ValidationError(
                f"El nombre de usuario no puede superar los {USERNAME_MAX} caracteres."
            )
        if not USERNAME_RE.match(username):
            raise forms.ValidationError(
                "Solo se permiten letras, números y los caracteres: . @ + - _"
            )

        qs = User.objects.filter(username=username)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Este nombre de usuario ya está en uso.")

        return username

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip()

        if not email:
            raise forms.ValidationError("El correo electrónico es obligatorio.")

        # Validación básica de formato (Django ya la hace, pero la dejamos explícita)
        if '@' not in email or '.' not in email.split('@')[-1]:
            raise forms.ValidationError("Ingresa un correo electrónico válido.")

        qs = User.objects.filter(email__iexact=email)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Este correo electrónico ya está registrado.")

        return email.lower()

    def clean_role(self):
        role = self.cleaned_data.get('role', '')
        if role not in ROLES_VALIDOS:
            raise forms.ValidationError("Rol no válido. Selecciona Empleado o Gerente.")
        return role

    def clean_identificacion(self):
        identificacion = self.cleaned_data.get('identificacion', '').strip()
        tipo = self.cleaned_data.get('tipo_identificacion', '')

        if not identificacion:
            raise forms.ValidationError("El número de identificación es obligatorio.")

        # Solo dígitos en CC/TI/CE; pasaportes pueden contener letras
        if tipo in ('CC', 'TI', 'CE'):
            if not SOLO_NUMEROS_RE.match(identificacion):
                raise forms.ValidationError(
                    "Para este tipo de documento solo se permiten números."
                )

        if len(identificacion) < IDENTIFICACION_MIN:
            raise forms.ValidationError(
                f"La identificación debe tener al menos {IDENTIFICACION_MIN} dígitos."
            )
        if len(identificacion) > IDENTIFICACION_MAX:
            raise forms.ValidationError(
                f"La identificación no puede superar los {IDENTIFICACION_MAX} caracteres."
            )

        qs = Profile.objects.filter(identificacion=identificacion)
        if self.instance and self.instance.pk:
            qs = qs.exclude(user=self.instance)
        if qs.exists():
            raise forms.ValidationError("Este número de identificación ya está registrado.")

        if tipo and identificacion:
            try:
                validar_por_tipo(identificacion, tipo)
            except ValidationError as e:
                raise forms.ValidationError(e.message)

        return identificacion

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono', '').strip()

        if not telefono:
            raise forms.ValidationError("El teléfono es obligatorio.")

        # No debe contener letras
        if re.search(r'[A-Za-z]', telefono):
            raise forms.ValidationError("El teléfono no puede contener letras.")

        # Solo dígitos, espacios, guiones y '+' inicial
        if not TELEFONO_RE.match(telefono):
            raise forms.ValidationError(
                "Ingresa un teléfono válido (ej: 3001234567 o +57 300 123 4567)."
            )

        digitos = re.sub(r'\D', '', telefono)
        if len(digitos) < TELEFONO_MIN:
            raise forms.ValidationError(
                f"El teléfono debe tener al menos {TELEFONO_MIN} dígitos."
            )
        if len(digitos) > TELEFONO_MAX:
            raise forms.ValidationError(
                f"El teléfono no puede tener más de {TELEFONO_MAX} dígitos."
            )

        try:
            telefono_validator(telefono)
        except ValidationError as e:
            raise forms.ValidationError(e.message)

        return telefono

    def clean_direccion(self):
        direccion = self.cleaned_data.get('direccion', '').strip()

        if not direccion:
            raise forms.ValidationError("La dirección es obligatoria.")
        if len(direccion) < DIRECCION_MIN:
            raise forms.ValidationError(
                f"La dirección debe tener al menos {DIRECCION_MIN} caracteres."
            )
        if len(direccion) > DIRECCION_MAX:
            raise forms.ValidationError(
                f"La dirección no puede superar los {DIRECCION_MAX} caracteres."
            )
        # Debe contener al menos un número (número de calle/carrera)
        if not re.search(r'\d', direccion):
            raise forms.ValidationError(
                "La dirección debe incluir un número (ej: Calle 10 # 5-30)."
            )
        return direccion

    def clean_password(self):
        password = self.cleaned_data.get('password')

        # En edición, campo vacío = no cambiar contraseña
        if not password and self.instance and self.instance.pk:
            return None

        if password:
            if password != password.strip():
                raise forms.ValidationError(
                    "La contraseña no puede comenzar ni terminar con espacios."
                )
            if len(password) < PASSWORD_MIN:
                raise forms.ValidationError(
                    f"La contraseña debe tener al menos {PASSWORD_MIN} caracteres."
                )
            validate_password(password, self.instance)

        return password

    # ── Validación cruzada (clean general) ───────────────────────────────────
    def clean(self):
        cleaned_data = super().clean()
        password    = cleaned_data.get("password")
        password2   = cleaned_data.get("password2")
        old_password = cleaned_data.get("old_password")
        role        = cleaned_data.get('role')

        # Contraseña antigua incorrecta
        if self.instance and self.instance.pk and old_password:
            if not self.instance.check_password(old_password):
                self.add_error('old_password', "La contraseña actual no es correcta.")

        # Nueva contraseña y confirmación no coinciden
        if password and password != password2:
            self.add_error('password2', "Las nuevas contraseñas no coinciden.")

        # Protección: único administrador
        if self.instance and self.instance.pk and self.instance.is_superuser:
            if role == 'normal':
                admins_activos = User.objects.filter(is_superuser=True).count()
                if admins_activos <= 1:
                    raise forms.ValidationError(
                        "No puedes quitarte el rol de Gerente porque eres el único en el sistema."
                    )

        return cleaned_data

    # ── save ─────────────────────────────────────────────────────────────────
    def save(self, commit=True):
        user = super().save(commit=False)

        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)

        role = self.cleaned_data.get('role')
        if role == 'admin':
            user.is_superuser = True
            user.is_staff     = True
        else:
            user.is_superuser = False
            user.is_staff     = True

        if commit:
            user.save()
            Profile.objects.update_or_create(
                user=user,
                defaults={
                    'tipo_identificacion': self.cleaned_data.get('tipo_identificacion'),
                    'identificacion':      self.cleaned_data.get('identificacion'),
                    'direccion':           self.cleaned_data.get('direccion'),
                    'telefono':            self.cleaned_data.get('telefono'),
                }
            )
        return user


# ─────────────────────────────────────────────────────────────────────────────
# FORMULARIO DE PERFIL PROPIO: Edición de datos del usuario (vista de empleado)
# ─────────────────────────────────────────────────────────────────────────────
class PerfilUsuarioForm(forms.ModelForm):
    first_name = forms.CharField(required=True, label="Nombres")
    last_name  = forms.CharField(required=True, label="Apellidos")
    email      = forms.EmailField(required=True, label="Correo Electrónico")

    class Meta:
        model  = User
        fields = ['first_name', 'last_name', 'email', 'username']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'required': 'required'})
        self.fields['last_name'].widget.attrs.update({'required': 'required'})
        placeholder_map = {
            'first_name': 'Tu nombre',
            'last_name':  'Tu apellido',
            'username':   'Nombre de Usuario',
            'email':      'ejemplo@dominio.com',
        }
        for name, field in self.fields.items():
            field.widget.attrs.update({
                'class':       'form-control',
                'placeholder': placeholder_map.get(name, field.label),
            })

    def clean_first_name(self):
        valor = self.cleaned_data.get('first_name', '')
        if not valor or not valor.strip():
            raise forms.ValidationError("El nombre no puede estar vacío.")
        return _validar_solo_letras(valor, 'nombre')

    def clean_last_name(self):
        valor = self.cleaned_data.get('last_name', '')
        if not valor or not valor.strip():
            raise forms.ValidationError("El apellido no puede estar vacío.")
        return _validar_solo_letras(valor, 'apellido')

    def clean_username(self):
        username = self.cleaned_data.get('username', '').strip()

        if not username:
            raise forms.ValidationError("El nombre de usuario es obligatorio.")
        if len(username) < USERNAME_MIN:
            raise forms.ValidationError(
                f"El nombre de usuario debe tener al menos {USERNAME_MIN} caracteres."
            )
        if not USERNAME_RE.match(username):
            raise forms.ValidationError(
                "Solo se permiten letras, números y los caracteres: . @ + - _"
            )

        qs = User.objects.filter(username=username)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Este nombre de usuario ya está en uso.")

        return username

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip()

        if not email:
            raise forms.ValidationError("El correo electrónico es obligatorio.")
        if '@' not in email or '.' not in email.split('@')[-1]:
            raise forms.ValidationError("Ingresa un correo electrónico válido.")

        if User.objects.filter(email__iexact=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Este correo electrónico ya está registrado.")

        return email.lower()


# ─────────────────────────────────────────────────────────────────────────────
# FORMULARIO DE PERFIL EXTRA: Datos del modelo Profile
# ─────────────────────────────────────────────────────────────────────────────
class ProfileForm(forms.ModelForm):
    class Meta:
        model  = Profile
        fields = ['tipo_identificacion', 'identificacion', 'direccion', 'telefono', 'imagen']
        labels = {
            'tipo_identificacion': 'Tipo de Documento',
            'identificacion':      'Número de Identificación',
            'direccion':           'Dirección de Residencia',
            'telefono':            'Número de Teléfono',
            'imagen':              'Imagen de Perfil',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholder_map = {
            'identificacion': 'Ingrese su documento de identidad',
            'direccion':      'Calle, Carrera, Ciudad...',
            'telefono':       'Número de Teléfono (Ej: 3000000000)',
        }
        for name, field in self.fields.items():
            if name != 'imagen':
                field.widget.attrs.update({
                    'class':       'form-control',
                    'placeholder': placeholder_map.get(name, ''),
                })

    def clean_tipo_identificacion(self):
        tipo = self.cleaned_data.get('tipo_identificacion', '').strip()
        if not tipo:
            raise forms.ValidationError("Debes seleccionar un tipo de documento.")
        return tipo

    def clean_identificacion(self):
        identificacion = self.cleaned_data.get('identificacion', '').strip()
        tipo           = self.cleaned_data.get('tipo_identificacion', '')

        if not identificacion:
            raise forms.ValidationError("El número de identificación es obligatorio.")

        if tipo in ('CC', 'TI', 'CE'):
            if not SOLO_NUMEROS_RE.match(identificacion):
                raise forms.ValidationError(
                    "Para este tipo de documento solo se permiten números."
                )

        if len(identificacion) < IDENTIFICACION_MIN:
            raise forms.ValidationError(
                f"La identificación debe tener al menos {IDENTIFICACION_MIN} dígitos."
            )
        if len(identificacion) > IDENTIFICACION_MAX:
            raise forms.ValidationError(
                f"La identificación no puede superar los {IDENTIFICACION_MAX} caracteres."
            )

        qs = Profile.objects.filter(identificacion=identificacion)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Este número de identificación ya está registrado.")

        if tipo and identificacion:
            validar_por_tipo(identificacion, tipo)

        return identificacion

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono', '').strip()

        if not telefono:
            raise forms.ValidationError("El teléfono es obligatorio.")
        if re.search(r'[A-Za-z]', telefono):
            raise forms.ValidationError("El teléfono no puede contener letras.")
        if not TELEFONO_RE.match(telefono):
            raise forms.ValidationError(
                "Ingresa un teléfono válido (ej: 3001234567 o +57 300 123 4567)."
            )

        digitos = re.sub(r'\D', '', telefono)
        if len(digitos) < TELEFONO_MIN:
            raise forms.ValidationError(
                f"El teléfono debe tener al menos {TELEFONO_MIN} dígitos."
            )
        if len(digitos) > TELEFONO_MAX:
            raise forms.ValidationError(
                f"El teléfono no puede tener más de {TELEFONO_MAX} dígitos."
            )

        try:
            telefono_validator(telefono)
        except ValidationError as e:
            raise forms.ValidationError(e.message)

        return telefono

    def clean_direccion(self):
        direccion = self.cleaned_data.get('direccion', '').strip()

        if not direccion:
            raise forms.ValidationError("La dirección es obligatoria.")
        if len(direccion) < DIRECCION_MIN:
            raise forms.ValidationError(
                f"La dirección debe tener al menos {DIRECCION_MIN} caracteres."
            )
        if len(direccion) > DIRECCION_MAX:
            raise forms.ValidationError(
                f"La dirección no puede superar los {DIRECCION_MAX} caracteres."
            )
        if not re.search(r'\d', direccion):
            raise forms.ValidationError(
                "La dirección debe incluir un número (ej: Calle 10 # 5-30)."
            )
        return direccion

    def clean_imagen(self):
        imagen = self.cleaned_data.get('imagen')
        if imagen and hasattr(imagen, 'content_type'):
            tipos_permitidos = ('image/jpeg', 'image/png', 'image/webp', 'image/gif')
            if imagen.content_type not in tipos_permitidos:
                raise forms.ValidationError(
                    "Formato de imagen no válido. Usa JPG, PNG, WEBP o GIF."
                )
            limite_mb = 2
            if imagen.size > limite_mb * 1024 * 1024:
                raise forms.ValidationError(
                    f"La imagen no puede pesar más de {limite_mb} MB."
                )
        return imagen
    
class ClienteForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs['autofocus'] = True
        
    class Meta:
        model = Cliente
        exclude = ['estado']
        fields = '__all__'
        widgets = {
            'tipo':Select(
                attrs={
                    'class': 'form-control',
                    'class': 'form-control foreign-key-field',
                    'autofocus': True
                }
            ),
            
            'nombre':TextInput(
                attrs={
                    'placeholder':'Ingrese el nombre del cliente',
                }
            ),
            'tipo_identificacion': Select(
                attrs={
                    'class': 'form-control'
                }
            ),
            'identificacion':TextInput(
                attrs={
                    'placeholder':'Ingrese el documento del cliente',
                }
            ),
            'telefono':NumberInput(
                attrs={
                    'placeholder':'Ingrese el telefono del cliente',
                }
            ),
            'correo':TextInput(
                attrs={
                    'placeholder':'Ingrese el correo del cliente',
                }
            ),
            'direccion':TextInput(
                attrs={
                    'placeholder':'Ingrese la dirección del cliente',
                }
            ),
            
            
        }
        error_messages = {
            'tipo': {
                'required': 'El tipo de cliente es obligatorio',
            },
            'nombre': {
                'required': 'El nombre del cliente es obligatorio',
                'invalid': 'Por favor ingrese solo letras en el nombre del cliente',
            },
            'identificacion': {
                'required': 'El docmuento de identidad es obligatorio',
                'unique': 'Ya existe un cliente con ese documento de identidad',
                'invalid': 'Por favor ingrese solo números en el documento de identidad',
            },
            'telefono': {
                'required': 'El teléfono es obligatorio',
                'invalid': 'Por favor ingrese solo números en el telefono',
            },
            'correo': {
                'required': 'El correo es obligatorio',
                'invalid': 'El correo no tiene un formato válido',
                'unique': 'Ya existe un cliente con ese correo',
            },
            'direccion': {
                'required': 'La dirección es obligatoria',
                'invalid': 'Por favor ingrese solo letras y números en la dirección',
            }
           
        }
        def clean(self):
            """Validación personalizada que cruza tipo y número"""
            cleaned_data = super().clean()
            tipo = cleaned_data.get('tipo_identificacion')
            identificacion = cleaned_data.get('identificacion')

            if tipo and identificacion:
                valor = str(identificacion).strip().upper()
            
                # Definición de reglas por cada tipo del SELECT
                reglas = {
                    'CC': (r'^\d{5,10}$', 'La Cédula debe tener entre 5 y 10 dígitos numéricos.'),
                    'TI': (r'^\d{10,11}$', 'La Tarjeta de Identidad debe tener 10 u 11 dígitos.'),
                    'RC': (r'^\d{10,11}$', 'El Registro Civil debe tener 10 u 11 dígitos.'),
                    'NIT': (r'^\d{7,10}-\d{1}$', 'El NIT debe tener formato 123456789-0.'),
                    'CE': (r'^\d{3,9}$', 'La Cédula de Extranjería debe ser numérica (hasta 9 dígitos).'),
                    'PAS': (r'^[A-Z0-9]{5,20}$', 'El Pasaporte debe ser alfanumérico (5-20 caracteres).'),
                    'PPT': (r'^[A-Z0-9]{4,15}$', 'El PPT debe ser alfanumérico.'),
                }

                if tipo in reglas:
                    regex, mensaje = reglas[tipo]
                    if not re.fullmatch(regex, valor):
                        # Agrega el error específicamente al campo 'identificacion'
                        self.add_error('identificacion', mensaje)
        
            return cleaned_data
        
class VehiculoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Configura cómo se muestran los clientes en el select
        if 'id_cliente' in self.fields:
            self.fields['id_cliente'].label_from_instance = (
                lambda obj: f"{obj.id} - {obj.nombre}"  
            )
            self.fields['id_cliente'].widget.attrs.update({
                'class': 'form-control foreign-key-field',
                'autofocus': True
            })
        
    class Meta:
        model = Vehiculo
        exclude = ['estado']
        fields = '__all__'
        widgets = {
            'id_cliente': Select(
                attrs={
                    'class': 'form-control foreign-key-field',
                }
            ),
            'placa': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese la placa del vehiculo (ej: ABC123) o (A1C234)',
                }
            ),
            'modelo_vehiculo': TextInput(  # ← CORRECTO: coincide con el modelo
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el modelo del vehiculo (ej: 2024)',
                }
            ),
            'marca_vehiculo': TextInput(  # ← CORRECTO: coincide con el modelo
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese la marca del vehiculo',
                }
            ),
            'color': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el color del vehiculo',
                }
            ),
        }
        error_messages = {
            'id_cliente': {
                'required': 'El cliente es obligatorio',
            },
            'placa': {
                'required': 'La placa del vehiculo es obligatoria',
                'unique': 'Ya existe un vehiculo con esa placa',
            },
            'modelo_vehiculo': {  # ← CORRECTO
                'required': 'El modelo de vehiculo es obligatorio',
                'invalid': 'El modelo debe tener 4 dígitos',
            },
            'marca_vehiculo': {  # ← CORRECTO
                'required': 'La marca del vehiculo es obligatoria',
            },
            'color': {
                'required': 'El color del vehiculo es obligatorio',
            },
        }
        
        
class EntradaVehiculoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fecha_ingreso'].widget.attrs['autofocus'] = True

        # Label bonito para el select de vehículo
        self.fields['id_vehiculo'].queryset = Vehiculo.objects.filter(estado=True)
        self.fields['id_vehiculo'].label_from_instance = (
            lambda v: f"{v.placa} — {v.marca_vehiculo} {v.modelo_vehiculo} ({v.color})"
        )
        self.fields['id_vehiculo'].empty_label = "Seleccione un vehículo"

        self.fields['id_cliente'].queryset = Cliente.objects.filter(estado=True)
        self.fields['id_cliente'].label_from_instance = (
            lambda c: f"{c.nombre} — {c.identificacion}"
        )
        self.fields['id_cliente'].empty_label = "Seleccione un cliente"
        self.fields['id_cliente'].required = False  

        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')

    class Meta:
        model = EntradaVehiculo
        exclude = ['estado']
        fields = ['id_vehiculo', 'id_cliente', 'fecha_ingreso', 'hora_ingreso']
        widgets = {
            'id_vehiculo': Select(attrs={'class': 'form-control', 'id': 'id_id_vehiculo'}),
            'id_cliente':  Select(attrs={'class': 'form-control', 'id': 'id_id_cliente'}),
            'fecha_ingreso': DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
            }),
            'hora_ingreso': TimeInput(attrs={
                'type': 'time',
                'class': 'form-control',
            }),
        }
        error_messages = {
            'id_vehiculo':  {'required': 'El vehículo es obligatorio.'},
            'fecha_ingreso': {'required': 'La fecha de ingreso es obligatoria.'},
            'hora_ingreso':  {'required': 'La hora de ingreso es obligatoria.'},
        }
        
class SalidaVehiculoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fecha_salida'].widget.attrs['autofocus'] = True
        
    class Meta:
        model = SalidaVehiculo
        exclude = ['estado']
        fields = '__all__'
        widgets = {
            'id_salida':Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            
            'fecha_salida':DateInput(
                attrs={
                    'type': 'date',
                    'placeholder':'Ingrese la fecha de salida',
                }
            ),
            'hora_salida':TimeInput(
                attrs={
                    'type': 'time',
                    'placeholder':'Ingrese la hora de salida',
                }
            )
        }
        error_messages = {
            'id_salida': {
                'required': 'El id de salida es obligatorio',
            },
            'id_vehiculo': {
                'required': 'El id del vehiculo es obligatorio',
            },
            'id_cliente': {
                'required': 'El id del cliente es obligatorio',
            },
            'diagnostico': {
                'required': 'El diagnostico del vehiculo es obligatorio',
            },
            'fecha_salida': {
                'required': 'La fecha de salida del vehiculo es obligatoria',
            },
            'hora_salida': {
                'required': 'La hora de salida del vehiculo es obligatoria',
            },
        }
        

    
        
# -----------Formulario modelo informe------------------    
# En apy/forms.py
class InformeForm(forms.ModelForm):
    class Meta:
        model = Informes
        exclude = ['estado']
        # Sacamos 'detalle_servicio' e 'id_empleado' de aquí
        fields = ['tipo_informe', 'diagnostico_final']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Solo aplicamos estilos a lo que queda
        self.fields['tipo_informe'].widget.attrs.update({'class': 'form-select'})
        self.fields['diagnostico_final'].widget.attrs.update({
            'class': 'form-control', 
            'placeholder': 'Escriba el diagnóstico detallado aquí...'
        })
      
# -----------Formulario modelo pago servicios publicos------------------        
class PagoServiciosForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if 'monto' in self.fields:
            self.fields['monto'].widget.attrs['autofocus'] = True
            
        if 'servicio' in self.fields:
            choices = list(self.fields['servicio'].choices)[1:] 
            self.fields['servicio'].choices = [("", "Seleccione el servicio")] + choices
            
    class Meta:
        model = PagoServiciosPublicos
        exclude = ['estado']
        fields = '__all__'
        widgets = {
            'servicio': Select(
                attrs={
                    'placeholder': 'Seleccione el servicio',
                }
            ),
            'monto': NumberInput(
                attrs={
                    'placeholder': 'Ingrese el monto del pago de servicio publico',
                    'step': '0.01'
                }
            )
        }
        error_messages = {
            'servicio': {
                'required': 'Debe seleccionar un servicio',
            },
            'monto': {
                'required': 'El monto de pago es obligatorio',
            },
         } 
        
# -----------Formulario modelo pagos------------------    
class PagoForm(forms.ModelForm):
    class Meta:
        model  = Pagos
        exclude = ['estado']
        fields = ['proveedor', 'fecha', 'tipo_pago']
        widgets = {
            'proveedor': forms.Select(attrs={'class': 'form-control'}),
            'fecha':     forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'tipo_pago': forms.Select(attrs={'class': 'form-control'}),
        }
        error_messages = {
            'fecha': {
                'required': 'La fecha del pago es obligatoria',
            },
            'tipo_pago': {
                'required': 'El tipo de pago es obligatorio',
            },
        } 


# ── Form base para DetallePago (reutilizado por los 3 formsets) ──
class DetallePagoRepuestoForm(forms.ModelForm):
    """Solo muestra el campo repuesto."""
    class Meta:
        model  = DetallePago
        fields = ['repuesto', 'cantidad', 'precio_unitario']
        widgets = {
            'repuesto':        forms.Select(attrs={'class': 'form-control'}),
            'cantidad':        forms.NumberInput(attrs={'class': 'form-control cantidad-repuesto', 'min': '1'}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control precio-repuesto', 'min': '0'}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.tipo_item = 'Repuesto'   # forzamos el tipo
        instance.insumo      = None
        instance.herramienta = None
        if commit:
            instance.save()
        return instance


class DetallePagoInsumoForm(forms.ModelForm):
    """Muestra el campo insumo y la unidad de medida."""
    
    # Campo adicional para mostrar la unidad actual del insumo (solo lectura)
    unidad_actual = forms.CharField(
        required=False, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly', 'style': 'background-color:#f8f9fa;'}),
        label="Unidad del insumo"
    )
    
    class Meta:
        model  = DetallePago
        fields = ['insumo', 'unidad', 'cantidad', 'precio_unitario']
        widgets = {
            'insumo':          forms.Select(attrs={'class': 'form-control insumo-select', 'data-placeholder': 'Seleccione un insumo'}),
            'unidad':          forms.Select(attrs={'class': 'form-control unidad-select'}),
            'cantidad':        forms.NumberInput(attrs={'class': 'form-control cantidad-insumo', 'min': '1', 'step': '0.01'}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control precio-insumo', 'min': '0'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si estamos editando un detalle existente, mostrar la unidad guardada
        if self.instance and self.instance.pk and self.instance.insumo:
            self.fields['unidad_actual'].initial = self.instance.get_unidad_display()
            # Pre-seleccionar la unidad guardada
            self.fields['unidad'].initial = self.instance.unidad

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.tipo_item   = 'Insumo'
        instance.repuesto    = None
        instance.herramienta = None
        if commit:
            instance.save()
        return instance


class DetallePagoHerramientaForm(forms.ModelForm):
    """Solo muestra el campo herramienta."""
    class Meta:
        model  = DetallePago
        fields = ['herramienta', 'cantidad', 'precio_unitario']
        widgets = {
            'herramienta':     forms.Select(attrs={'class': 'form-control'}),
            'cantidad':        forms.NumberInput(attrs={'class': 'form-control cantidad-herramienta', 'min': '1'}),
            'precio_unitario': forms.NumberInput(attrs={'class': 'form-control precio-herramienta', 'min': '0'}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.tipo_item = 'Herramienta'
        instance.repuesto  = None
        instance.insumo    = None
        if commit:
            instance.save()
        return instance


# ── Los tres formsets ──
DetallePagoRepuestoFormSet = inlineformset_factory(
    Pagos,
    DetallePago,
    form=DetallePagoRepuestoForm,
    extra=1,
    can_delete=True,
    # Filtramos solo los detalles de tipo Repuesto al editar
)

DetallePagoInsumoFormSet = inlineformset_factory(
    Pagos,
    DetallePago,
    form=DetallePagoInsumoForm,
    extra=1,
    can_delete=True,
)

DetallePagoHerramientaFormSet = inlineformset_factory(
    Pagos,
    DetallePago,
    form=DetallePagoHerramientaForm,
    extra=1,
    can_delete=True,
)

 #------- formulario Gastos -------     
        
class GastosForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = Gastos
        exclude = ['estado']
        fields = ['tipo_gastos', 'monto', 'fecha', 'descripcion', 'id_pagos_servicios']
        widgets = {
            'fecha': DateInput(attrs={'type': 'date'}),
            'monto': NumberInput(attrs={'type': 'number', 'step': '0.01', 'placeholder': 'Ingrese el monto del gasto'}),
            'descripcion': TextInput(attrs={'placeholder': 'Ej: Pago de arriendo o papelería'}),
            'tipo_gastos': Select(attrs={'class': 'form-select'}),
            'id_pagos_servicios': Select(attrs={'class': 'form-select'}),
        }
        error_messages = {
            'monto': {
                'required': 'El monto del gasto es obligatorio',
                'invalid': 'El monto debe ser un número válido (entero o decimal)',
            },
            'descripcion': {
                'required': 'La descripcion del gasto es obligatorio',
            },
            'tipo_gastos': {
                'required': 'El tipo de gasto es obligatorio',
            },
            'id_pagos_servicios': {
                'required': 'El id del pago de servicios es obligatorio',
            },
            'fecha': {
                'required': 'La fecha del gasto es obligatoria',
            },
        }
#-----formularo Marca ---------------        
class MarcaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs['autofocus'] = True
        
    class Meta:
        model = Marca
        exclude = ['estado']
        fields = '__all__'
        widgets = {
            'nombre':TextInput(
                attrs={
                    'placeholder':'Ingrese el nombre de la marca',
                }
            ),
            'tipo':Select(
                attrs={
                    'placeholder':'Ingrese el tipo de la marca',
                }
            ),
         
       } 
        
        error_messages = {
            'nombre': {
                'required': 'El nombre de marca es obligatorio',
            },
            'tipo': {
                'required': 'El tipo de marca es obligatoria',
            },
        }
    
   #------- formulario Caja ---------------
class CajaForm(ModelForm): 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tipo_movimiento'].widget.attrs['autofocus'] = True
        
    class Meta:
        model = Caja
        exclude = ['estado']
        fields = '__all__'
        widgets = {
            'tipo_movimiento':Select(
                attrs={
                    'placeholder':'Ingrese el tipo de movimiento',
                }
            ),
            'monto':NumberInput(
                attrs={
                    'placeholder':'Ingrese el monto del movimiento',
                }
            ),
            'fecha':DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date' ,
                }
            ),
            'hora':TimeInput(
                attrs={
                    'class': 'form-control',
                    'type': 'time' ,
                }
            ),
        }       
        error_messages = {
            'tipo_mantenimiento': {
                'required': 'El tipo de mantenimiento es obligatorio',
            },
            'monto': {
                'required': 'El monto es obligatorio',
            },
            'fecha': {
                'required': 'La fecha es obligatoria',
            },
            'hora': {
                'required': 'La hora es obligatoria',
            },
        }  
       
         
class HerramientaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['stock'].initial = None
        self.fields['nombre'].widget.attrs['autofocus'] = True
        
    class Meta:
        model = Herramienta
        exclude = ['stock_minimo', 'estado'] 
        fields = '__all__'
        widgets = {
            'nombre':TextInput(
                attrs={
                    'placeholder':'Ingrese el nombre de la herramienta',
                }
            ),
             'color':TextInput(
                attrs={
                    'placeholder':'Ingrese el color de la herramienta',
                }
            ),
            'tipo':Select(
                attrs={
                    'placeholder':'Ingrese el tipo de herramienta',
                }
            ), 
            
            'id_marca':Select(
                attrs={
                    'placeholder':'Ingrese la marca de herramientas',
                }
            ),
            'stock':NumberInput(
                attrs={
                    'placeholder':'Ingrese el stock de herramientas',
                },
            )
        }
        error_messages = {
            'nombre': {
                'required': 'El nombre de la herramienta es obligatorio',
            },
            'color': {
                'required': 'Es color de la herramienta es obligatorio',
            },
            'tipo': {
                'required': 'El tipo de herramienta es obligatorio',
            },
            
            'id_marca': {
                'required': 'El id de la marca es obligatoria',
            },
            'stock': {
                'required': 'El stock de la herramienta es obligatorio',
            },
            
        }
        def clean_stock(self):
            stock = self.cleaned_data.get('stock')
            if stock is not None and stock <= 0:
                raise forms.ValidationError("La cantidad debe ser mayor a 0.")
            return stock

class TipoMantenimientoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs['autofocus'] = True
        
    class Meta:
        model = TipoMantenimiento
        exclude = ['estado']
        fields = ['nombre', 'descripcion']
        widgets = {
            'nombre':TextInput(
                attrs={
                    'placeholder':'Ingrese el nombre del tipo de mantenimiento',
                }
            ),
            'descripcion':TextInput(
                attrs={
                    'placeholder':'Ingrese la descripcion del tipo de mantenimiento',
                }
            ),
        }  
        error_messages = {
            'nombre': {
                'required': 'El nombre del tipo de mantenimiento es obligatorio',
            },
            'descripcion': {
                'required': 'La descripcion del tipo de mantenimiento es obligatorio',
            },
        }

class InsumoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_marca'].widget.attrs['autofocus'] = True
        
    class Meta:
        model = Insumos
        fields = '__all__'
        exclude = ['stock_minimo', 'estado'] 
        widgets = {
            'id_marca':Select(
                attrs={
                    'placeholder':'Ingrese la descripcion del insumo',
                }
            ),
            'nombre':TextInput(
                attrs={
                    'placeholder':'Ingrese el nombre del insumo',
                }
            ),
            'costo':NumberInput(
                attrs={
                    'placeholder':'Ingrese el costo del insumo',
                }
            ),
            'stock':NumberInput(
                attrs={
                    'placeholder':'Ingrese la cantidad del insumo',
                }
            ),
            'cantidad':Select(
                attrs={
                    'placeholder':'Ingrese la unidad de medida del insumo',
                }
            ),
            'stock_minimo':NumberInput(
                attrs={
                    'placeholder':'Ingrese el stock mínimo del insumo',
                }
            ),
        }
        error_messages = {
            'id_marca': {
                'required': 'El id de la marca es obligatoria',
            },
            'nombre': {
                'required': 'El nombre del insumo es obligatorio',
            },
            'costo': {
                'required': 'El costo del insumo es obligatorio',
            },
            'stock': {
                'required': 'El stock de insumo es obligatorio',
            },
            'cantidad': {
                'required': 'La unidad de medida del insumo es obligatoria',
            },
        }
        

class RepuestoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['stock'].initial = None
        # Primer campo en recibir foco
        self.fields['id_marca'].widget.attrs['autofocus'] = True
        # Aplica form-control a todos los campos automáticamente
        for field_name, field in self.fields.items():
            existing = field.widget.attrs.get('class', '')
            if 'form-control' not in existing:
                field.widget.attrs['class'] = f'{existing} form-control'.strip()

    class Meta:
        model = Repuesto
        exclude = ['estado']
        fields = ['id_marca', 'nombre', 'categoria','stock', 'stock_minimo', 'precio_unitario']
        widgets = {
            'id_marca': Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            'nombre': TextInput(
                attrs={
                    'placeholder': 'Ej: Filtro de aceite',
                    'autocomplete': 'off',
                }
            ),
            'categoria': Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            
            'precio_unitario': NumberInput(
                attrs={
                    'placeholder': '0',
                    'min': '0',
                    'step': '0.01',
                    'class': 'form-control precio-unitario',
                }
            ),
            'stock': NumberInput(
                attrs={
                    'placeholder': '0',
                    'min': '0',
                }
            ),
            'stock_minimo': NumberInput(
                attrs={
                    'placeholder': '1',
                    'min': '0',
                }
            ),
            
        }
        error_messages = {
            'id_marca':    {'required': 'La marca es obligatoria.'},
            'nombre':      {'required': 'El nombre del repuesto es obligatorio.'},
            'categoria':   {'required': 'La categoría es obligatoria.'},
            'precio_unitario': {'required': 'El precio unitario es obligatorio.'},
            'stock':       {'required': 'El stock inicial es obligatorio.'},
            'stock_minimo':{'required': 'El stock mínimo es obligatorio.'},
        }
        def clean_precio(self):
            precio = self.data.get('precio')
            if precio:
            # quitar puntos o comas de miles
                precio = precio.replace('.', '').replace(',', '')
                try:
                    return int(precio)
                except (ValueError, InvalidOperation):
                    raise forms.ValidationError(
                    "Ingrese un número válido (ej: 3600 o 3.600 o 3,600)"
                    )
            return 0
        
        def clean_stock(self):
            stock = self.cleaned_data.get('stock')
            if stock is not None and stock <= 0:
                raise forms.ValidationError("La cantidad debe ser mayor a 0.")
            return stock
        
class NominaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        # Mostramos el nombre real del empleado en el select
        self.fields['empleado'].label_from_instance = lambda obj: f"{obj.user.first_name} {obj.user.last_name}"

    class Meta:
        model = Nomina
        exclude = ['estado']
        fields = ['empleado', 'monto', 'fecha_pago']
        widgets = {
            'fecha_pago': DateInput(attrs={'type': 'date'}),
            'monto': NumberInput(attrs={'placeholder': 'Total pagado al empleado'}),
        }    
        
class   NominaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['empleado'].widget.attrs['autofocus'] = True
        
    class Meta:
        model = Nomina
        exclude = ['estado']
        fields = '__all__'
        widgets = {
            
            'empleado':Select(
                attrs={
                    'class': 'form-control',
                }
            )
,            
            'monto':NumberInput(
             attrs={
                  'placeholder':'Ingrese el monto del empleado',
                }
            ),
            
            'fecha_pago':DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date' ,
                }
            ),
           
            
        }
        error_messages = {
            
            'monto': {
                'required': 'El monto es obligatorio',
            },
            'fecha_pago': {
                'required': 'La fecha de pago de la nomina es obligatoria',
            },
            'id_empleado': {
                'required': 'El id del empleado es obligatorio',
            }
        }            