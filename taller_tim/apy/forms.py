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
#------- formularios Yury--------        
        
#------- formulario Empleado -------        
        
class EmpleadoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs['autofocus'] = True
        
    class Meta:
        model = Empleado
        fields = '__all__'
        widgets = {
            'nombre':TextInput(
                attrs={
                    'placeholder':'Ingrese el nombre del empleado',
                }
            ),
            'telefono':TextInput(
                attrs={
                    'placeholder':'Ingrese el telefono del empleado',
                }
            ),
            'identificacion':TextInput(
                attrs={
                    'placeholder':'Ingrese la identificacion del empleado',
                }
            ),
            'correo':TextInput(
                attrs={
                    'placeholder':'Ingrese el correo del empleado',
                }
            ),
            'telefono':TextInput(
                attrs={
                    'placeholder':'Ingrese la direccion del empleado',
                }
            )
            
       }  
 #------- formulario Gastos -------     
        
class GastosForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['monto'].widget.attrs['autofocus'] = True
        
    class Meta:
        model = Gastos
        fields = '__all__'
        widgets = {
            'monto':TextInput(
                attrs={
                    'placeholder':'Ingrese el monto del gasto',
                }
            ),
            'descripcion':TextInput(
                attrs={
                    'placeholder':'Ingrese la descripcion del gasto',
                }
            ),
            'tipo_gastos':TextInput(
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
            'tipo':TextInput(
                attrs={
                    'placeholder':'Ingrese el tipo de la marca',
                }
            ),
         
       } 
        
#-----formularo Nomina ---------------
class   NominaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_empleado'].widget.attrs['autofocus'] = True
        
    class Meta:
        model = Nomina
        fields = '__all__'
        widgets = {
            'rol':TextInput(
                attrs={
                    'placeholder':'Ingrese rol del empleado',
                }
            ),
            'monto':TextInput(
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
           
            'id_empleado':Select(
                attrs={
                    'class': 'form-control',
                }
            )
        }
        
   #------- formulario Caja ---------------
class CajaForm(ModelForm): 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_admin'].widget.attrs['autofocus'] = True
        
    class Meta:
        model = Caja
        fields = '__all__'
        widgets = {
            'tipo_movimiento':TextInput(
                attrs={
                    'placeholder':'Ingrese el tipo de movimiento',
                }
            ),
            'monto':TextInput(
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
            'id_Factura':Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            'id_gasto':Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            'id_pagos':Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            
            'id_nomina':Select(
                attrs={
                    'class': 'form-control',
                }
            )
        }         
       