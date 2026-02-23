import os 
import django 
import random 
import sys 
from fake import Faker

sys.path.append(os.path.dirname(os.path.abspath(__file__))) 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taller.settings') 
django.setup()

from apy.models import ( Marca, Empleado, Cliente, Herramienta, Vehiculo, Gastos, Insumos, Caja, PagoServiciosPublicos )

fake = Faker('es_CO')

def poblar_clientes(n=10): 
    for _ in range(n): Cliente.objects.create( tipo=random.choice(['cliente particular', 'empresa']), nombre=fake.name(), identificacion=fake.unique.bothify(text='#########'), telefono=fake.bothify(text='3#########'), correo=fake.email(), direccion=fake.address(), estado=True ) print("✅ Clientes creados")

def poblar_marcas(): tipos = ['Repuesto', 'Herramienta', 'Insumo', 'Vehiculo'] for t in tipos: for _ in range(5): Marca.objects.get_or_create( nombre=fake.company()[:100], tipo=t, estado=True ) print("✅ Marcas creadas")

def poblar_insumos(n=15): marcas = Marca.objects.filter(tipo='Insumo') for _ in range(n): Insumos.objects.create( id_marca=random.choice(marcas) if marcas.exists() else None, costo=random.randint(5000, 50000), stock=random.randint(1, 100), cantidad=random.choice(['litro', 'galon', 'unidades']), estado=True ) print("✅ Insumos creados")

def poblar_vehiculos(n=10): marcas = Marca.objects.filter(tipo='Vehiculo') clientes = Cliente.objects.all() for _ in range(n): Vehiculo.objects.create( id_cliente=random.choice(clientes), placa=fake.unique.bothify(text='???###').upper(), modelo_vehiculo=str(random.randint(2000, 2025)), marca_vehiculo=random.choice(marcas).nombre if marcas.exists() else "Generica", color=fake.color_name(), estado=True ) print("✅ Vehiculos creados")

def poblar_gastos_y_caja(n=10): servicios = ['luz', 'agua', 'gas', 'internet'] for _ in range(n): monto = random.randint(20000, 500000) srv = PagoServiciosPublicos.objects.create( servicio=random.choice(servicios), monto=monto, estado=True ) Gastos.objects.create( monto=monto, descripcion=fake.sentence(), tipo_gastos='costo fijo', id_pagos_servicios=srv, estado=True ) Caja.objects.create( tipo_movimiento='Gasto', monto=monto, fecha=fake.date_this_year(), hora=fake.time(), estado=True ) print("✅ Gastos registrados")

def poblar_ingresos_caja(n=30): for _ in range(n): Caja.objects.create( tipo_movimiento='Ingreso', monto=random.randint(100000, 2000000), fecha=fake.date_this_year(), hora=fake.time(), estado=True ) print("✅ Ingresos creados")

if name == 'main': print("🚀 Iniciando poblado...") poblar_marcas() poblar_clientes(10) poblar_insumos(15) poblar_vehiculos(10) poblar_gastos_y_caja(10) poblar_ingresos_caja(40) 
print("⭐ ¡Proceso completado!")