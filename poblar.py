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
    
def generar_entradas(n=10):
    vehiculos = Vehiculo.objects.all()
    if not vehiculos.exists():
        print("❌ Error: No hay vehículos para entradas.")
        return

    for _ in range(n):
        v = random.choice(vehiculos)
        # Usamos datetime.time para evitar el error de argumentos
        hora_ingreso = datetime.time(random.randint(7, 12), random.randint(0, 59))
        fecha_ingreso = datetime.date.today() - datetime.timedelta(days=random.randint(1, 10))
        
        EntradaVehiculo.objects.create(
            id_vehiculo=v,
            id_cliente=v.id_cliente,
            fecha_ingreso=fecha_ingreso,
            hora_ingreso=hora_ingreso
        )
    print(f"✅ {n} Entradas creadas.")

def generar_salidas(n=5):
    entradas = EntradaVehiculo.objects.all()
    if not entradas.exists():
        print("❌ Error: No hay entradas para generar salidas.")
        return

    for entrada in random.sample(list(entradas), min(len(entradas), n)):
        # La salida debe ser después de la entrada
        fecha_salida = entrada.fecha_ingreso + datetime.timedelta(days=random.randint(0, 2))
        hora_salida = datetime.time(random.randint(14, 18), 0)
        
        SalidaVehiculo.objects.get_or_create(
            id_vehiculo=entrada.id_vehiculo,
            id_cliente=entrada.id_cliente,
            defaults={
                'diagnostico': "Mantenimiento finalizado exitosamente.",
                'fecha_salida': fecha_salida,
                'hora_salida': hora_salida
            }
        )
    print(f"✅ {n} Salidas creadas.")
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
        generar_salidas(5)
        generar_entradas(10)
        print("¡Proceso finalizado con éxito!")
    except Exception as e:
        print(f"❌ Error durante el proceso: {e}")