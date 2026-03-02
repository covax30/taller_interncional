from genericpath import exists
from pyexpat.errors import messages
from django import forms
from django.forms import ModelForm, Select, NumberInput, DateInput, TimeInput, TextInput, EmailInput
from django.forms import inlineformset_factory
from decimal import Decimal, InvalidOperation
# apy/forms.py (Asegúrate de importar esto)
from django.contrib.auth.hashers import make_password
from django import forms  # Asegúrate de usar la importación estándar de forms
from django.contrib.auth.models import User, Permission  # Importación de modelos de Django
from django.core.exceptions import ValidationError
from .models import Profile,DetalleServicio
from .validators import solo_letras_validator, ComplexPasswordValidator, telefono_validator
from django.contrib.auth.password_validation import validate_password

from apy.models import *
        

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
            'autofocus': True
        })
        
    class Meta:
        model = DetalleTipoMantenimiento
        fields = ['id_tipo_mantenimiento', 'cantidad', 'precio_unitario']
        widgets = {
            
            'id_tipo_mantenimiento': Select(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el tipo de mantenimiento',
                }
            ),
            'cantidad': NumberInput(
                attrs={
                    'placeholder': 'Ingrese la cantidad',
                    'class': 'form-control',
                    'min': '1'
                }
            ),
            'precio_unitario': NumberInput(
                attrs={
                    'placeholder': 'Ingrese el precio unitario',
                    'step': '0.01',
                    'class': 'form-control',
                }
            ),  
        }
        error_messages = {
                
            'id_tipo_mantenimiento': {
                'required': 'El tipo de mantenimiento es obligatorio',
            },
            'cantidad': {
                'required': 'La cantidad es obligatoria',
            },
            'precio_unitario': {
                'required': 'El precio unitario es obligatorio',
            }
        }

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
class RegistroUsuarioForm(forms.ModelForm):
    # --- CAMPOS EXTRA QUE NO ESTÁN EN EL MODELO USER ---
    old_password = forms.CharField(
        label='Contraseña Antigua',
        widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña actual'}),
        required=False
    )
    
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'}),
        strip=False,
        required=True
    )
    
    password2 = forms.CharField(
        label='Confirmar Contraseña',
        widget=forms.PasswordInput(attrs={'placeholder': 'Repita la contraseña'}),
        strip=False,
        required=True
    )
    
    role = forms.ChoiceField(
        label='Rol',
        choices=[('normal', 'Empleado'), ('admin', 'Gerente')],
        widget=forms.Select(),
        required=True
    )
    
    tipo_identificacion = forms.ChoiceField(
        label='Tipo de Documento',
        choices=Profile.TIPO_DOC_CHOICES, # Asegúrate que existan en el modelo Profile
        widget=forms.Select()
    )

    identificacion = forms.CharField(
        label='Identificación', 
        required=True,
        widget=forms.TextInput()
    )
    
    direccion = forms.CharField(
        label='Dirección', 
        required=False, 
        widget=forms.TextInput()
    )
    
    telefono = forms.CharField(
        label='Teléfono', 
        required=False, 
        widget=forms.TextInput()
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # 1. Ajuste de obligatoriedad si es edición
        if self.instance and self.instance.pk:
            self.fields['password'].required = False
            self.fields['password2'].required = False
            
            # 2. Sincronizar Rol con is_superuser
            if self.instance.is_superuser:
                self.initial['role'] = 'admin'
            else:
                self.initial['role'] = 'normal'
            
            # 3. Cargar datos del Perfil relacionados
            try:
                perfil = self.instance.profile
                self.initial.update({
                    'tipo_identificacion': perfil.tipo_identificacion,
                    'identificacion': perfil.identificacion,
                    'direccion': perfil.direccion,
                    'telefono': perfil.telefono,
                })
            except (Profile.DoesNotExist, AttributeError):
                pass

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if first_name:
            try:
                solo_letras_validator(first_name)
            except ValidationError:
                raise forms.ValidationError("El nombre solo debe contener letras.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if last_name:
            try:
                solo_letras_validator(last_name)
            except ValidationError:
                raise forms.ValidationError("El apellido solo debe contener letras.")
        return last_name

    def clean_identificacion(self):
        identificacion = self.cleaned_data.get('identificacion')
        tipo = self.cleaned_data.get('tipo_identificacion')
        
        # Validar duplicados excluyendo al propio usuario
        qs = Profile.objects.filter(identificacion=identificacion)
        if self.instance and self.instance.pk:
            qs = qs.exclude(user=self.instance)
        
        if qs.exists():
            raise ValidationError("Este número de identificación ya está registrado.")
            
        # Ejecutar validación lógica de negocio (formato según tipo)
        if tipo and identificacion:
            try:
                validar_por_tipo(identificacion, tipo)
            except ValidationError as e:
                raise ValidationError(e.message)
                
        return identificacion
    
    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if telefono:
            try:
                # Llamamos al validador que creamos arriba
                telefono_validator(telefono)
            except ValidationError as e:
                raise forms.ValidationError(e.message)
        return telefono

    def clean_password(self):
        password = self.cleaned_data.get('password')
        # Si es edición y está vacío, no se cambia
        if not password and self.instance and self.instance.pk:
            return None # Importante devolver None para saber que no cambia
        
        # Validadores de Django (Complexity, length, etc)
        if password:
            validate_password(password, self.instance)
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        old_password = cleaned_data.get("old_password")
        role = cleaned_data.get('role')

        # VALIDACIÓN: Contraseña Antigua
        if self.instance and self.instance.pk and old_password:
            if not self.instance.check_password(old_password):
                self.add_error('old_password', "La contraseña actual no es correcta.")

        # VALIDACIÓN: Nueva contraseña coincidente
        if password and password != password2:
            self.add_error('password2', "Las nuevas contraseñas no coinciden.")

        # VALIDACIÓN: Protección último Administrador
        if self.instance and self.instance.pk and self.instance.is_superuser:
            if role == 'normal':
                admins_activos = User.objects.filter(is_superuser=True).count()
                if admins_activos <= 1:
                    raise forms.ValidationError("Error: No puedes quitarte el rol de Admin porque eres el único en el sistema.")
        
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        
        # Guardar nueva contraseña si se proporcionó
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        
        # Asignación de permisos según Rol
        role = self.cleaned_data.get('role')
        if role == 'admin':
            user.is_superuser = True
            user.is_staff = True
        else:
            user.is_superuser = False 
            user.is_staff = True # Permitir login al sistema como empleado
        
        if commit:
            user.save()
            # Guardar o actualizar datos de Perfil
            Profile.objects.update_or_create(
                user=user,
                defaults={
                    'tipo_identificacion': self.cleaned_data.get('tipo_identificacion'),
                    'identificacion': self.cleaned_data.get('identificacion'),
                    'direccion': self.cleaned_data.get('direccion'),
                    'telefono': self.cleaned_data.get('telefono'),
                }
            )
        return user


# 1. Formulario para editar el modelo User 
class PerfilUsuarioForm(forms.ModelForm):
    first_name = forms.CharField(required=True, label="Nombres")
    last_name = forms.CharField(required=True, label="Apellidos")
    email = forms.EmailField(required=True, label="Correo Electrónico")
    class Meta:
        model = User
        # Solo campos nativos de User
        fields = ['first_name', 'last_name', 'email', 'username'] 
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'required': 'required'})
        self.fields['last_name'].widget.attrs.update({'required': 'required'})
        placeholder_map = {
            'first_name': 'Tu nombre',
            'last_name': 'Tu apellido',
            'username': 'Nombre de Usuario',
            'email': 'ejemplo@dominio.com',
        }
        for name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': placeholder_map.get(name, field.label) 
            })
            
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name:
            raise forms.ValidationError("El nombre no puede estar vacío.")
        solo_letras_validator(first_name)
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name:
            raise forms.ValidationError("El apellido no puede estar vacío.")
        solo_letras_validator(last_name)
        return last_name
            
    # Lógica de limpieza para email...
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Este correo electrónico ya está registrado.")
        return email

# 2. Formulario para editar el modelo Profile
class ProfileForm(forms.ModelForm):
    telefono = forms.CharField(required=True, label='Número de Teléfono')
    direccion = forms.CharField(required=True, label='Dirección de Residencia')
    imagen_clear = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    
    class Meta:
        model = Profile
        fields = ['tipo_identificacion', 'identificacion', 'direccion', 'telefono', 'imagen']      
        labels = {
            'identificacion': 'Número de Identificación',
            'direccion': 'Dirección de Residencia',
            'telefono': 'Número de Teléfono',
            'imagen': 'Imagen de Perfil',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholder_map = {
            'identificacion': 'Ingrese su documento de identidad',
            'direccion': 'Calle, Carrera, Ciudad...',
            'telefono': 'Número de Teléfono (Ej: 3000000000)',
        }
        
        for name, field in self.fields.items():
            if name != 'imagen':
                field.widget.attrs.update({
                    'class': 'form-control',
                    'placeholder': placeholder_map.get(name, '')
                })
    
    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if telefono:
            telefono_validator(telefono) # Usamos tu validador externo
        return telefono

    def clean_direccion(self):
        direccion = self.cleaned_data.get('direccion')
        if not direccion or len(direccion.strip()) < 5:
            raise forms.ValidationError("Por favor, ingresa una dirección válida y completa.")
        return direccion
    
    def clean_identificacion(self):
        identificacion = self.cleaned_data.get('identificacion')
        tipo = self.cleaned_data.get('tipo_identificacion')
        
        if not identificacion:
            raise ValidationError("El número de identificación es obligatorio.")
             
        # Validar duplicados
        qs = Profile.objects.filter(identificacion=identificacion)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        
        if qs.exists():
            raise ValidationError("Este número de identificación ya está registrado.")
            
        if tipo and identificacion:
            validar_por_tipo(identificacion, tipo) # Tu validador externo
                
        return identificacion
    
class ClienteForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs['autofocus'] = True
        
    class Meta:
        model = Cliente
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
        fields = '__all__'
        widgets = {
            'id_cliente': Select(
                attrs={
                    'class': 'form-control foreign-key-field',  # ← Solo una clase
                }
            ),
            'placa': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese la placa del vehiculo (ej: ABC123) o (A1C234)',
                }
            ),
            'modelo_vehiculo': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese el modelo del vehiculo (ej: 2024)',
                }
            ),
            'marca_vehiculo': TextInput(
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
            'modelo_vehiculo': {
                'required': 'El modelo de vehiculo es obligatorio',
            },
            'marca_vehiculo': {
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
        
    class Meta:
        model = EntradaVehiculo
        fields = '__all__'
        widgets = {
            'id_entrada':Select(
                attrs={
                    'class': 'form-control',
                }
            ),
          
            'fecha_ingreso':DateInput(
                attrs={
                    'type': 'date',
                    'placeholder':'Ingrese la fecha de ingreso',
                }
            ),
            'hora_ingreso':TimeInput(
                attrs={
                    'type': 'time',
                    'placeholder':'Ingrese la hora de ingreso',
                }
            ),
        }
        error_messages = {
            'id_entrada': {
                'required': 'El id de entrada es obligatorio',
            },
            'id_vehiculo': {
                'required': 'El id del vehiculo es obligatorio',
            },
            'id_cliente': {
                'required': 'El id del cliente es obligatorio',
            },
            'fecha_ingreso': {
                'required': 'La fecha de ingreso del vehiculo es obligatoria',
            },
            'hora_ingreso': {
                'required': 'La hora de ingreso del vehiculo es obligatoria',
            },
        }
        
class SalidaVehiculoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fecha_salida'].widget.attrs['autofocus'] = True
        
    class Meta:
        model = SalidaVehiculo
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
class InformeForm(forms.ModelForm):
    class Meta:
        model = Informes
        fields = ['detalle_servicio', 'id_empleado', 'tipo_informe', 'costo_mano_obra', 'diagnostico_final']
        widgets = {
            'detalle_servicio': forms.Select(attrs={'class': 'form-control select2'}),
            'id_empleado': forms.Select(attrs={'class': 'form-control'}),
            'tipo_informe': forms.Select(attrs={'class': 'form-control'}),
            'costo_mano_obra': forms.NumberInput(attrs={'class': 'form-control'}),
            'diagnostico_final': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtro: Solo servicios terminados que no tengan informe
        self.fields['detalle_servicio'].queryset = DetalleServicio.objects.filter(
            proceso='terminado', 
            informes__isnull=True
        )
        error_messages = {
            'repuestos_usados': {
                'required': 'Los repuestos usados son obligatorios',
            },
            'costo_mano_obra': {
                'required': 'El costo de mano de obra es obligatorio',
            },
            'fecha': {
                'required': 'La fecha es obligatoria',
            },
            'hora': {
                'required': 'La hora es obligatoria',
            },
            'id_repuesto': {
                'required': 'El id del repuesto es obligatorio',
            },
            'id_empleado': {
                'required': 'El id del empleado es obligatorio',
            },
            'id_tipo_mantenimiento': {
                'required': 'El id de tipo de mantenimiento es obligatorio',
            },
            'tipo_informe': {
                'required': 'El tipo de informe es obligatorio',
            },
            'id_mantenimiento': {
                'required': 'El id de mantenimiento es obligatorio',
            },
        }
   
   
      
# -----------Formulario modelo pago servicios publicos------------------        
class PagoServiciosForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add safety check to prevent KeyError
        if 'monto' in self.fields:
            self.fields['monto'].widget.attrs['autofocus'] = True
            
        if 'servicio' in self.fields:
            choices = list(self.fields['servicio'].choices)[1:] 
            self.fields['servicio'].choices = [("", "Seleccione el servicio")] + choices
            
    class Meta:
        model = PagoServiciosPublicos
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
class PagosForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tipo_pago'].widget.attrs['autofocus'] = True
        
        
    class Meta:
        model = Pagos
        fields = '__all__'
        widgets = {
            'tipo_pago':TextInput(
                attrs={
                    'placeholder':'Ingrese el tipo de pago',
                }
            ),
            'fecha':DateInput(
                attrs={
                    'placeholder':'Ingrese la fecha de la creacion del pago',
                    'type': 'date'
                }
            ),
            'hora':TimeInput(
                attrs={
                    'placeholder':'Ingrese la hora de la creacion del pago',
                    'type': 'time'
                }
            ),
            'monto':NumberInput(
                attrs={
                    'placeholder':'Ingrese el monto del pago',
                    'step': '0.01',
                    'min': '0'
                }
            ),
            'id_proveedor':Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            'id_admin':Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            'id_herramienta':Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            'id_insumos':Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            'id_repuestos':Select(
                attrs={
                    'class': 'form-control',
                }
            ),
        }
        error_messages = {
            'tipo_pago': {
                'required': 'El tipo de pago es obligatorio',
            },
            'fecha': {
                'required': 'La fecha es obligatoria',
            },
            'hora': {
                'required': 'La hora es obligatoria',
            },
            'monto': {
                'required': 'El monto es obligatorio',
            },
            'id_proveedor': {
                'required': 'El id del proveedor es obligatorio',
            },
            'id_admin': {
                'required': 'El id del administrador es obligatorio',
            },
            'id_herramienta': {
                'required': 'El id de las herramientas es obligatorio',
            },
            'id_insumos': {
                'required': 'El id de los insumos es obligatorio',
            },
            'id_repuestos': {
                'required': 'El id de los repuestos es obligatorio',
            },
        }
   
        
#------- formularios Yury--------        
 #------- formulario Gastos -------     
        
class GastosForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['monto'].widget.attrs['autofocus'] = True
        
    class Meta:
        model = Gastos
        fields = '__all__'
        widgets = {
            'monto': NumberInput(
                attrs={
                    'placeholder': 'Ingrese el monto del gasto',
                    'min': '99',
                    'step': '0.01'        # permite decimales
                }
            ),
            'descripcion':TextInput(
                attrs={
                    'placeholder':'Ingrese la descripcion del gasto',
                }
            ),
            'tipo_gastos':Select(
                attrs={
                    'placeholder':'Ingrese el tipo de gasto ',
                }
            ),
            'id_pagos_servicios':Select(
                attrs={
                    'class': 'form-control',
                }
            )
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
        }
#-----formularo Marca ---------------        
class MarcaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs['autofocus'] = True
        
    class Meta:
        model = Marca
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
                'required': 'E tipo de marca es obligatoria',
            },
        }
    
   #------- formulario Caja ---------------
class CajaForm(ModelForm): 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tipo_movimiento'].widget.attrs['autofocus'] = True
        
    class Meta:
        model = Caja
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
            
            'id_admin':Select(
                attrs={
                    'class': 'form-control',
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
            'id_admin': {
                'required': 'El id del administrador es obligatorio',
            },
        }  
       
        
class MantenimientoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fallas'].widget.attrs['autofocus'] = True
        
    class Meta:
        model = Mantenimiento
        fields = '__all__'
        widgets = {
            'fallas':TextInput(
                attrs={
                    'placeholder':'Ingrese las fallas',
                }
            ),
            'procesos':TextInput(
                attrs={
                    'placeholder':'Ingrese los procesos',
                }
            ),
            'id_vehiculo':Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            'id_empleado':Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            'id_tipo_mantenimiento':Select(
                attrs={
                    'class': 'form-control',
                }
            )
        }
        error_messages = {
            'fallas': {
                'required': 'Es obligatorio registrar las fallas encontradas',
            },
            'procesos': {
                'required': 'Es obligatorio registrar los procesos realizados al vehiculo',
            },
            'id_vehiculo': {
                'required': 'El id del vehiculo es obligatorio',
            },
            'id_empleado': {
                'required': 'El id del empleado es obligatorio',
            },
            'id_tipo_mantenimiento': {
                'required': 'El id del tipo de mantenimiento es obligatorio',
            }
        }
        
         
class HerramientaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs['autofocus'] = True
        
    class Meta:
        model = Herramienta
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
            'material':TextInput(
                attrs={
                    'placeholder':'Ingrese el material de la herramienta',
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
            'material': {
                'required': 'El material de la herramienta es obligatorio',
            },
            'id_marca': {
                'required': 'El id de la marca es obligatoria',
            },
            'stock': {
                'required': 'El stock de la herramienta es obligatorio',
            }
        }

class TipoMantenimientoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs['autofocus'] = True
        
    class Meta:
        model = TipoMantenimiento
        fields = '__all__'
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
        widgets = {
            'id_marca':Select(
                attrs={
                    'placeholder':'Ingrese la descripcion del insumo',
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
        }
        error_messages = {
            'id_marca': {
                'required': 'El id de la marca es obligatoria',
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
            'tipo': {
                'required': 'El tipo de insumo es obligatorio',
            },
            'stock': {
                'required': 'El stock de insumo es obligatorio',
            },
        }

class RepuestoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_marca'].widget.attrs['autofocus'] = True
        
    class Meta:
        model = Repuesto
        fields = '__all__'
        widgets = {
            'id_marca':Select(
                attrs={
                    'placeholder':'Ingrese la marca del repuesto',
                    'class': 'form-select',
                    'data-bs-toggle': 'modal',
                    'data-bs-target': '#modalMarca'
                }
            ),
            'nombre':TextInput(
                attrs={
                    'placeholder':'Ingrese el nombre de el repuesto',
                }   
            ),
            'categoria':Select(
                attrs={
                    'placeholder':'Ingrese la categoria del repuesto',
                }
            ),
            'fabricante':TextInput(
                attrs={
                    'placeholder':'Ingrese el nombre del fabricante',
                }
            ),
            'stock':NumberInput(
                attrs={
                    'placeholder':'Ingrese el stock del repuesto',
                }
            ),
            'ubicacion':TextInput(
                attrs={
                    'placeholder':'Ingrese la ubicacion del repuesto',
                }
            ),
            'precio': TextInput(
                attrs={'placeholder': 'Ingrese el precio del repuesto'}
            ),
        }
        error_messages = {
            'id_marca': {
                'required': 'El id de la marca obligatoria',
            },
            'nombre': {
                'required': 'El nombre del repuesto es obligatorio',
            },
            'categoria': {
                'required': 'El nombre de la categoria es obligatoria',
            },
            'fabricante': {
                'required': 'El nombre del fabricate es obligatorio',
            },
            'stock': {
                'required': 'El stock del repuesto es obligatorio',
            },
            'ubicacion': {
                'required': 'La ubicacion del repuesto es obligatoria',
            },
            'precio': {
                'required': 'El precio del repuesto es obligatorio',
            }
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