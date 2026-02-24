<<<<<<< HEAD
from datetime import date, datetime, timedelta
import os
from time import time
import django
import random
import sys
from faker import Faker

# 1. CONFIGURACIÓN DE RUTAS
# Añadimos la ruta actual al sistema para que encuentre el módulo 'taller'
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Cambiamos 'taller_interncional' por 'taller' (el nombre real de tu proyecto)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taller.settings')
django.setup()

# 2. IMPORTACIÓN DE TUS MODELOS
from apy.models import EntradaVehiculo, Insumos, Marca, Empleado, Cliente, Repuesto, SalidaVehiculo, TipoMantenimiento, Vehiculo

fake = Faker('es_ES')

def poblar_marcas():
    tipos = ['Repuesto', 'Herramienta', 'Insumo', 'Vehiculo']
    for t in tipos:
        for _ in range(2):
            Marca.objects.get_or_create(
                nombre=fake.company()[:100], # Limitamos a 100 caracteres
                tipo=t,
                estado=True
            )
    print("✅ Marcas creadas")

def poblar_empleados(n=5):
    for _ in range(n):
        Empleado.objects.create(
            nombre=fake.name(),
            telefono=str(random.randint(10000000, 99999999)), # 8 dígitos
            identificacion=str(random.randint(10000000, 99999999)),
            Correo=fake.unique.email(),
            direccion=fake.address()[:255],
            estado=True
        )
    print(f"✅ {n} Empleados creados")

def poblar_clientes(n=10):
    for _ in range(n):
        tipo = random.choice(['cliente particular', 'empresa'])
        # Generamos una identificación que pase tu validador (7 a 10 dígitos)
        ident = str(random.randint(10000000, 999999999)) 
        
        Cliente.objects.create(
            tipo=tipo,
            nombre=fake.name() if tipo == 'cliente particular' else fake.company(),
            identificacion=ident,
            telefono=str(random.randint(3000000000, 3209999999))[:20],
            correo=fake.unique.email(),
            direccion=fake.address(),
            estado=True
        )
    print(f"✅ {n} Clientes creados")
    
    
def generar_tipos_mantenimiento():
    tipos = [
        ('Preventivo', 'Mantenimiento regular para evitar fallos.'),
        ('Correctivo', 'Reparación de fallos una vez ocurridos.'),
        ('Predictivo', 'Basado en el estado del equipo.'),
    ]
    
    for nombre, desc in tipos:
        # get_or_create evita errores si ya existen en la BD
        obj, created = TipoMantenimiento.objects.get_or_create(
            nombre=nombre,
            defaults={'descripcion': desc, 'estado': True}
        )
        if created:
            print(f"✅ Tipo creado: {nombre}")
        else:
            print(f"ℹ️ El tipo '{nombre}' ya existía.")
    
def generar_insumos(n=10):
    marcas = Marca.objects.all()
    
    if not marcas.exists():
        print("❌ Error: Necesitas crear Marcas antes de generar Insumos.")
        return

    opciones_unidad = ['galon', 'litro', 'mililitro', 'unidades']

    for _ in range(n):
        Insumos.objects.create(
            id_marca=random.choice(marcas), # Instancia real de Marca
            costo=random.randint(10000, 500000), # Entero (no string)
            stock=random.randint(5, 100),
            cantidad=random.choice(opciones_unidad),
            estado=True
        )
    
    print(f"✅ {n} Insumos creados con éxito.")
def generar_repuestos(n=15):
    marcas = Marca.objects.all()
    
    if not marcas.exists():
        print("❌ Error: No hay Marcas para asociar a los Repuestos.")
        return

    categorias = ['automotriz', 'industrial']
    repuestos_nombres = ['Filtro de Aceite', 'Bujía', 'Pastilla de Freno', 'Correa de Distribución', 'Rodamiento', 'Válvula Solenoide']

    for _ in range(n):
        Repuesto.objects.create(
            id_marca=random.choice(marcas),
            nombre=random.choice(repuestos_nombres) + " " + fake.word().capitalize(),
            categoria=random.choice(categorias),
            fabricante=fake.company(),
            stock=random.randint(1, 200),
            ubicacion=f"Pasillo {random.choice(['A', 'B', 'C'])}-{random.randint(1, 10)}",
            # Asegúrate que el precio cumpla con tu 'validar_monto' (ej. > 0)
            precio=random.randint(50000, 2000000), 
            estado=True
        )
    print(f"✅ {n} Repuestos creados con éxito.")
    
def generar_vehiculos(n=10):
    clientes = Cliente.objects.all()
    
    if not clientes.exists():
        print("❌ Error: No hay Clientes para asignar vehículos.")
        return

    marcas_autos = ['Toyota', 'Chevrolet', 'Mazda', 'Renault', 'Kia', 'Nissan']
    colores = ['Blanco', 'Negro', 'Gris Plata', 'Rojo', 'Azul']

    for _ in range(n):
        # Generamos una placa aleatoria: 3 letras y 3 números (Ej: ABC123)
        letras = "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=3))
        numeros = "".join(random.choices("0123456789", k=3))
        placa_gen = f"{letras}{numeros}"

        try:
            Vehiculo.objects.create(
                id_cliente=random.choice(clientes),
                placa=placa_gen,
                modelo_vehiculo=str(random.randint(2000, 2025)), # 4 dígitos para el año
                marca_vehiculo=random.choice(marcas_autos),
                color=random.choice(colores),
                estado=True
            )
        except Exception as e:
            print(f"⚠️ No se pudo crear el vehículo {placa_gen}: {e}")
            
    print(f"✅ {n} Vehículos creados con éxito.")
    

if __name__ == '__main__':
    print("Iniciando poblado de datos...")
    try:
        poblar_marcas()
        poblar_empleados(5)
        poblar_clientes(10)
        generar_tipos_mantenimiento()
        generar_insumos(10)
        generar_repuestos(15)
        generar_vehiculos(10)
        
        print("¡Proceso finalizado con éxito!")
    except Exception as e:
        print(f"❌ Error durante el proceso: {e}")
=======
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
>>>>>>> erick
