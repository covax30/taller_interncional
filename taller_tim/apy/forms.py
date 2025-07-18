from dataclasses import fields 
from django.forms import *
from django.forms import DateInput
from django.forms import TimeInput
from django.forms import ModelForm
from django.forms import TextInput, Select

from apy.models import *

class FacturaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_cliente'].widget.attrs['autofocus'] = True
        
    class Meta:
        model = Factura
        fields = '__all__'
        widgets = {
            'tipo_pago':TextInput(
                attrs={
                    'placeholder':'Ingrese el tipo de pago',
                }
            ),
            'id_cliente':Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            'id_vehiculo':Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            'id_tipo_mantenimiento':Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            'servicio_prestado':TextInput(
                attrs={
                    'placeholder':'Ingrese el servicio prestado',
                }
            ),
            'nombre_empresa':TextInput(
                attrs={
                    'placeholder':'Ingrese el nombre de la empresa',
                }
            ),
            'direccion_empresa':TextInput(
                attrs={
                    'placeholder':'Ingrese la direccion de la empresa',
                }
            ),
            'id_empleado':Select(
                attrs={
                    'class': 'form-control',
                }
            )
        }
        
        
        
class ProveedorForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs['autofocus'] = True
        
    class Meta:
        model = Proveedores
        fields = '__all__'
        widgets = {
            'nombre':TextInput(
                attrs={
                    'placeholder':'Ingrese el nombre del proveedor',
                }
            ),
            'telefono':TextInput(
                attrs={
                    'placeholder':'Ingrese el telefono del proveedor',
                }
            ),
            'correo':TextInput(
                attrs={
                    'placeholder':'Ingrese el correo del proveedor',
                }
            )
        }
        
# ------------------- FORMS STEVEN -------------------    

class ClienteForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs['autofocus'] = True
        
    class Meta:
        model = Cliente
        fields = '__all__'
        widgets = {
            'id_cliente':Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            'id_operacion':Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            'nombre':TextInput(
                attrs={
                    'placeholder':'Ingrese el nombre del cliente',
                }
            ),
            'documento':TextInput(
                attrs={
                    'placeholder':'Ingrese el documento del cliente',
                }
            ),
            'telefono':TextInput(
                attrs={
                    'placeholder':'Ingrese el telefono del cliente',
                }
            ),
            'correo':TextInput(
                attrs={
                    'placeholder':'Ingrese el correo del cliente',
                }
            ),
            'fecha_operacion':DateInput(
                attrs={
                    'type': 'date',
                    'placeholder': 'Ingrese la fecha de operacion',
                }
            ),
            'monto':TextInput(
                attrs={
                    'placeholder':'Ingrese el monto del cliente',
                }
            )
        }
        
class VehiculoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['placa'].widget.attrs['autofocus'] = True
        
    class Meta:
        model = Vehiculo
        fields = '__all__'
        widgets = {
            'id_vehiculo':Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            'id_cliente':Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            'placa':TextInput(
                attrs={
                    'placeholder':'Ingrese la placa del vehiculo',
                }
            ),
            'modelo_vehiculo':TextInput(
                attrs={
                    'placeholder':'Ingrese el modelo del vehiculo',
                }
            ),
            'marca_vehiculo':TextInput(
                attrs={
                    'placeholder':'Ingrese la marca del vehiculo',
                }
            ),
            'color':TextInput(
                attrs={
                    'placeholder':'Ingrese el color del vehiculo',
                }
            ),
        }
        
class EntradaVehiculoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_vehiculo'].widget.attrs['autofocus'] = True
        
    class Meta:
        model = EntradaVehiculo
        fields = '__all__'
        widgets = {
            'id_entrada':Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            'id_vehiculo':Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            'id_cliente':Select(
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
        
class SalidaVehiculoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_vehiculo'].widget.attrs['autofocus'] = True
        
    class Meta:
        model = SalidaVehiculo
        fields = '__all__'
        widgets = {
            'id_salida':Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            'id_vehiculo':Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            'id_cliente':Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            'diagnostico':TextInput(
                attrs={
                    'placeholder':'Ingrese el diagnóstico del vehículo',
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
        
class CompraForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_proveedor'].widget.attrs['autofocus'] = True
        
    class Meta:
        model = Compra
        fields = '__all__'
        widgets = {
            'id_factura_compra':Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            'id_compra':Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            'id_proveedor':Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            'fecha_compra':TextInput(
                attrs={
                    'placeholder':'Ingrese la fecha de compra',
                }
            ),
            'hora_compra':TextInput(
                attrs={
                    'placeholder':'Ingrese la hora de compra',
                }
            )
        }