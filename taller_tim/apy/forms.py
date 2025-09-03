from dataclasses import fields 
from django.forms import *
from django.forms import DateInput
from django.forms import TimeInput
from django.forms import ModelForm
from django.forms import TextInput, Select
from decimal import Decimal, InvalidOperation

from apy.models import *

# -----------Formulario modelo factura------------------
class FacturaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tipo_pago'].widget.attrs['autofocus'] = True
        
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
            ),
            'monto':NumberInput(
                attrs={
                    'placeholder':'Ingrese el monto total del servicio prestado',
                }
            )
        }
        error_messages = {
            'id_operacion': {
                'required': 'El id de la operacion es obligatorio',
            },
            'tipo_pago':{
                    'required': 'El tipo de pago es obligatorio',
                },
            'id_cliente':{
                    'required': 'El id del cliente es obligatorio',
                },
            'id_vehiculo':{
                    'required': 'El id del vehiculo es obligatorio',
                },
            'id_tipo_mantenimiento':{
                    'required': 'El id de tipo de mantenimiento es obligatorio',
                },
            'servicio_prestado':{
                    'required': 'El servicio prestado es obligatorio',
                },
            'nombre_empresa':{
                    'required': 'El nombre de la empresa es obligatorio',
                },
            'direccion_empresa':{
                    'required': 'La direccion de la empresa es obligatoria',
                },
            'id_empleado':{
                    'required': 'El id del empleado es obligatorio',
                },
            'monto':{
                    'required': 'El monto es obligatorio',
                }

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
            'telefono':NumberInput(
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

class ClienteForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_operacion'].widget.attrs['autofocus'] = True
        
    class Meta:
        model = Cliente
        fields = '__all__'
        widgets = {
            'id_cliente':Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            'id_operacion':TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'nombre':TextInput(
                attrs={
                    'placeholder':'Ingrese el nombre del cliente',
                }
            ),
            'documento':NumberInput(
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
            'fecha_operacion':DateInput(
                attrs={
                    'type': 'date',
                    'placeholder': 'Ingrese la fecha de operacion',
                }
            ),
            'monto':NumberInput(
                attrs={
                    'placeholder':'Ingrese el monto del cliente',
                }
            )
        }
        error_messages = {
            'id_operacion': {
                'required': 'El id de la operacion es obligatorio',
            },
            'nombre': {
                'required': 'El nombre es obligatorio',
            },
            'documento': {
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
            'fecha_operacion': {
                'required': 'La fecha de operacion es obligatoria',
            },
            'monto': {
                'required': 'El monto es obligatorio',
            },
        }
        
class VehiculoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_cliente'].widget.attrs['autofocus'] = True
        
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
        error_messages = {
            'id_cliente': {
                'required': 'El id del cliente es obligatorio',
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
                    'placeholder':'Ingrese el telefono del administrador',
                    'type': 'tel'
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
        
class CompraForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_factura_compra'].widget.attrs['autofocus'] = True
        
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
                }
            )
        }
        error_messages = {
            'id_factura_compra': {
                'required': 'El id de la factura de compra es obligatorio',
            },
            'id_proveedor': {
                'required': 'El id del proveedor es obligatorio',
            },
            'fecha_compra': {
                'required': 'La fecha de la compra es obligatoria',
            },
            'hora_compra': {
                'required': 'La hora de la compra es obligatoria',
            },
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
            'identificacion':NumberInput(
                attrs={
                    'placeholder':'Ingrese la identificacion del administrador',
                    'pattern': '[0-9]+',
                    'title': 'Solo se permiten números',
                    'maxlength': '20'
                }
            ),
            'edad':NumberInput(
                attrs={
                    'placeholder':'Ingrese la edad del administrador',
                    'min': 1,
                    'max': 100
                }
            ),
            'correo':EmailInput(
                attrs={
                    'placeholder':'Ingrese el correo del administrador',
                }
            ),
            'telefono':NumberInput(
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
        error_messages = {
            'nombre': {
                'required': 'El nombre es obligatorio',
            },
            'apellidos': {
                'required': 'El apellido es obligatorio',
            },
            'identificacion': {
                'required': 'La identificación es obligatoria',
                'unique': 'Ya existe un administrador con esa identificación',
                'invalid': 'Por favor ingrese solo números en la identificación',
            },
            'edad': {
                'required': 'La edad es obligatoria',
                'invalid': 'Por favor ingrese solo números en la edad',
            },
            'correo': {
                'required': 'El correo es obligatorio',
                'invalid': 'El correo no tiene un formato válido',
                'unique': 'Ya existe un administrador con ese correo',
            },
            'telefono': {
                'required': 'El teléfono es obligatorio',
                'invalid': 'Por favor ingrese solo números en el telefono',
            },
            'fecha_ingreso': {
                'required': 'La fecha de ingreso es obligatoria',
            },
        }
        

    
        
# -----------Formulario modelo informe------------------    
class InformeForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['repuestos_usados'].widget.attrs['autofocus'] = True
        
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
            'id_empleado':Select(
                attrs={
                    'class': 'form-control',
                }
            ),
            'id_tipo_mantenimiento':Select(
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
            )
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
            'telefono':NumberInput(
                attrs={
                    'placeholder':'Ingrese el telefono del empleado',
                }
            ),
            'identificacion':NumberInput(
                attrs={
                    'placeholder':'Ingrese la identificacion del empleado',
                }
            ),
            'Correo':TextInput(
                attrs={
                    'placeholder':'Ingrese el correo del empleado',
                }
            ),
            'direccion':TextInput(
                attrs={
                    'placeholder':'Ingrese la direccion del empleado',
                }
            )
            
       }  
        error_messages = {
            'nombre': {
                'required': 'El nombre del empleado es obligatorio',
            },
            'telefono': {
                'required': 'El telefono del empleado es obligatorio',
            },
            'identificacion': {
                'required': 'La identificacion del empleado es obligatoria',
            },
            'Correo': {
                'required': 'El correo del empleado es obligatorio',
                'invalid': 'El correo no tiene un formato válido',
                'unique': 'Ya existe un administrador con ese correo',
            },
            'direccion': {
                'required': 'La direccion del empleado es obligatoria',
            },
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
            'tipo':TextInput(
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
        
#-----formularo Nomina ---------------
class   NominaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rol'].widget.attrs['autofocus'] = True
        
    class Meta:
        model = Nomina
        fields = '__all__'
        widgets = {
            'rol':TextInput(
                attrs={
                    'placeholder':'Ingrese rol del empleado',
                }
            ),
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
           
            'id_empleado':Select(
                attrs={
                    'class': 'form-control',
                }
            )
        }
        error_messages = {
            'rol': {
                'required': 'El rol es obligatorio',
            },
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
        
   #------- formulario Caja ---------------
class CajaForm(ModelForm): 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tipo_movimiento'].widget.attrs['autofocus'] = True
        
    class Meta:
        model = Caja
        fields = '__all__'
        widgets = {
            'tipo_movimiento':TextInput(
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
            'id_Factura': {
                'required': 'El id de la factura es obligatorio',
            },
            'id_gasto': {
                'required': 'El id del gasto es obligatorio',
            },
            'id_pagos': {
                'required': 'El id del pago es obligatorio',
            },
            'id_nomina': {
                'required': 'El id de la nomina es obligatorio',
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
                }
            ),
            'nombre':TextInput(
                attrs={
                    'placeholder':'Ingrese el nombre de el repuesto',
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