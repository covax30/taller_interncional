from dataclasses import fields 
from django.forms import *

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
        
# -----------Formulario modelo administrador------------------
class AdministradorForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs['autofocus'] = True
        
    class Meta:
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
                }
            ),
            'telefono':TextInput(
                attrs={
                    'placeholder':'Ingrese el telefono del administrador',
                    'type': 'tel'
                }
            ),
            'fecha_ingreso':DateInput(
                attrs={
                    'placeholder':'Ingrese la fecha de ingreso del administrador',
                    'type': 'date'
                }
            )
        }
        
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
                attrs={
                    'class': 'form-control',
                }
            ),
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
                }
            )
        }