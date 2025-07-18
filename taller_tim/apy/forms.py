from dataclasses import fields 
from django.forms import *

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
            'tipo':TextInput(
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
            )
        }
        
class InsumoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs['autofocus'] = True
        
    class Meta:
        model = Insumos
        fields = '__all__'
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
            'tipo':TextInput(
                attrs={
                    'placeholder':'Ingrese el tipo de insumo',
                }
            ),
            'stock':NumberInput(
                attrs={
                    'placeholder':'Ingrese la cantidad del insumo',
                }
            ),
        }

class RepuestoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs['autofocus'] = True
        
    class Meta:
        model = Repuesto
        fields = '__all__'
        widgets = {
            'id_marca':Select(
                attrs={
                    'placeholder':'Ingrese la marca del repuesto',
                }
            ),
            'categoria':TextInput(
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
            'precio':NumberInput(
                attrs={
                    'placeholder':'Ingrese el precio del repuesto',
                }
            ),
            
        }