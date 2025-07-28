from dataclasses import fields 
from django.forms import *
from django.forms import DateInput
from django.forms import TimeInput
from django.forms import ModelForm
from django.forms import TextInput, Select

from apy.models import *

# -----------Formulario modelo factura------------------
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
        
# -----------Formulario modelo proveedor------------------        
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
            'correo':EmailInput(
                attrs={
                    'placeholder':'Ingrese el correo del proveedor',
                }
            )
        }
        
<<<<<<< HEAD
# ------------------- FORMS STEVEN -------------------    

class ClienteForm(ModelForm):
=======
# -----------Formulario modelo administrador------------------
class AdministradorForm(ModelForm):
>>>>>>> 3878fb8015073744e077a7b5bb9cf97fee5818e3
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs['autofocus'] = True
        
    class Meta:
<<<<<<< HEAD
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
=======
        model = Administrador
        fields = '__all__'
        widgets = {
            'nombre':TextInput(
                attrs={
                    'placeholder':'Ingrese el nombre del administrador',
                }
            ),
            'apellidos':TextInput(
                attrs={
                    'placeholder':'Ingrese los apellidos del administrador',
                }
            ),
            'identificacion':TextInput(
                attrs={
                    'placeholder':'Ingrese la identificacion del administrador',
                }
            ),
            'edad':NumberInput(
                attrs={
                    'placeholder':'Ingrese la edad del administrador',
                }
            ),
            'correo':EmailInput(
                attrs={
                    'placeholder':'Ingrese el correo del administrador',
>>>>>>> 3878fb8015073744e077a7b5bb9cf97fee5818e3
                }
            ),
            'telefono':TextInput(
                attrs={
<<<<<<< HEAD
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
=======
                    'placeholder':'Ingrese el telefono del administrador',
                    'type': 'tel'
>>>>>>> 3878fb8015073744e077a7b5bb9cf97fee5818e3
                }
            ),
            'fecha_ingreso':DateInput(
                attrs={
<<<<<<< HEAD
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
=======
                    'placeholder':'Ingrese la fecha de ingreso del administrador',
                    'type': 'date'
>>>>>>> 3878fb8015073744e077a7b5bb9cf97fee5818e3
                }
            )
        }
        
<<<<<<< HEAD
class CompraForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_proveedor'].widget.attrs['autofocus'] = True
        
    class Meta:
        model = Compra
        fields = '__all__'
        widgets = {
            'id_factura_compra':Select(
=======
# -----------Formulario modelo informe------------------    
class InformeForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tipo_informe'].widget.attrs['autofocus'] = True
        
    class Meta:
        model = Informes
        fields = '__all__'
        widgets = {
            'repuestos_usados':TextInput(
                attrs={
                    'placeholder':'Ingrese los nombres de los repuestos usados',
                }
            ),
            'costo_mano_obra':NumberInput(
                attrs={
                    'placeholder':'Ingrese el costo de mano de obra',
                    'step': '0.01'
                }
            ),
            'fecha':DateInput(
                attrs={
                    'placeholder':'Ingrese la fecha de la creacion del informe',
                    'type': 'date'
                }
            ),
            'hora':TimeInput(
                attrs={
                    'placeholder':'Ingrese la hora de la creacion del informe',
                    'type': 'time'
                }
            ),
            'id_repuesto':Select(
>>>>>>> 3878fb8015073744e077a7b5bb9cf97fee5818e3
                attrs={
                    'class': 'form-control',
                }
            ),
<<<<<<< HEAD
            'id_compra':Select(
                attrs={
                    'class': 'form-control',
                }
=======
            'tipo_informe':TextInput(
                attrs={
                    'placeholder':'Ingrese el tipo de informe',
                }
            ),
            'id_mantenimiento':Select(
                attrs={
                    'class': 'form-control',
                }
            )
        }
        
# -----------Formulario modelo pago servicios publicos------------------        
class PagoServiciosForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['monto'].widget.attrs['autofocus'] = True
        
    class Meta:
        model = PagoServiciosPublicos
        fields = '__all__'
        widgets = {
            'monto':NumberInput(
                attrs={
                    'placeholder':'Ingrese el monto del pago de servicio publico',
                    'step': '0.01'
                }
            )
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
>>>>>>> 3878fb8015073744e077a7b5bb9cf97fee5818e3
            ),
            'id_proveedor':Select(
                attrs={
                    'class': 'form-control',
                }
            ),
<<<<<<< HEAD
            'fecha_compra': DateInput(
                attrs={
                    'type': 'date',
                    'placeholder':'Ingrese la fecha de compra',
                }
            ),
            'hora_compra':TimeInput(
                attrs={
                    'type': 'time',
                    'placeholder':'Ingrese la hora de compra',
=======
            'id_admin':Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            'id_herramientas':Select(
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
>>>>>>> 3878fb8015073744e077a7b5bb9cf97fee5818e3
                }
            )
        }