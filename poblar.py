import os
import django
import random
import sys
from datetime import date
from faker import Faker

# 1. CONFIGURACIÓN DE DJANGO
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taller.settings')
django.setup()

# 2. IMPORTACIÓN DE MODELOS
from apy.models import (
    Marca, Cliente, Vehiculo, EntradaVehiculo, SalidaVehiculo, 
    TipoMantenimiento, Repuesto, Herramienta, Insumos, Profile,
    PagoServiciosPublicos, Proveedores, Gastos, DetalleServicio,
    Informes, Factura, Caja, Empresa
)
from django.contrib.auth.models import User

fake = Faker('es_CO')

def poblar_todo(n=10):
    print(f"🚀 Iniciando poblado de {n} registros por tabla...")

    # --- ENTIDADES INDEPENDIENTES ---
    
    # Empresa (Mínimo 1 para las llaves foráneas)
    empresa_principal, _ = Empresa.objects.get_or_create(
        nit="74.187366-2",
        defaults={
            'nombre': "Taller Mecanica Diesel Internacional Arturo Patiño",
            'direccion': "calle 9 #32-37 Barrio La Isla",
            'telefono': "3118112714"
        }
    )

    # Marcas (Repuesto, Herramienta, Insumo, Vehiculo)
    tipos_marca = ['Repuesto', 'Herramienta', 'Insumo', 'Vehiculo']
    for t in tipos_marca:
        for _ in range(n):
            Marca.objects.get_or_create(nombre=fake.company()[:100], tipo=t)
    print("✅ Marcas creadas")

    # Clientes
    for _ in range(n):
        try:
            Cliente.objects.create(
                tipo=random.choice(['cliente particular', 'empresa']),
                nombre=fake.name(),
                identificacion=fake.unique.bothify(text='#########'), # 9 dígitos
                telefono=fake.bothify(text='3#########'),
                correo=fake.unique.email(),
                direccion=fake.address()
            )
        except Exception:
            pass
    print("✅ Clientes creados")

    # Usuarios y Perfiles (Mecánicos/Empleados)
    for _ in range(n):
        try:
            user = User.objects.create_user(username=fake.unique.user_name(), password='password123', last_login=fake.date_time())
            Profile.objects.create(
                user=user,
                identificacion=fake.bothify(text='#########'),
                telefono=fake.bothify(text='3#########'),
                direccion=fake.address()[:150]
            )
        except Exception:
            pass
    print("✅ Usuarios y Perfiles creados")

    # Tipos de Mantenimiento y Proveedores
    for i in range(n):
        try:
            TipoMantenimiento.objects.get_or_create(nombre=f"Mantenimiento {fake.word()} {i}")
            Proveedores.objects.create(
                nombre=fake.company(),
                telefono=fake.bothify(text='3#########'),
                tipo_identificacion='NIT',
                identificacion=fake.unique.bothify(text='#########-#'),
                correo=fake.unique.email()
            )
        except Exception:
            pass
    print("✅ Tipos de Mantenimiento y Proveedores creados")

    # --- ENTIDADES CON DEPENDENCIAS ---

    marcas_v = Marca.objects.filter(tipo='Vehiculo')
    marcas_r = Marca.objects.filter(tipo='Repuesto')
    marcas_i = Marca.objects.filter(tipo='Insumo')
    clientes = Cliente.objects.all()
    perfiles = Profile.objects.all()

    # Vehículos
    for _ in range(n):
        try:
            Vehiculo.objects.create(
                id_cliente=random.choice(clientes),
                placa=fake.unique.bothify(text='???###').upper(),
                modelo_vehiculo=str(random.randint(2010, 2025)),
                marca_vehiculo=random.choice(marcas_v).nombre,
                color="Blanco",
                estado=True
            )
        except Exception:
            pass
    print("✅ Vehículos creados")

    # Repuestos, Insumos y Herramientas
    vehiculos = Vehiculo.objects.all()
    for i in range(n):
        Repuesto.objects.create(
            id_marca=random.choice(marcas_r),
            nombre=f"Repuesto {fake.word()}",
            categoria=random.choice(['automotriz', 'industrial']),
            fabricante=fake.company(),
            estado=True
        )
        Insumos.objects.create(
            id_marca=random.choice(marcas_i),
            nombre=f"Insumo {fake.word()}",
            costo=random.randint(5000, 100000),
            cantidad=random.choice(['galon', 'litro', 'unidades'])
        )
        # Herramientas
        Herramienta.objects.create(
            nombre=f"Herramienta {fake.word()}",
            color="Rojo",
            tipo=random.choice(['manuales', 'eléctricas']),
            id_marca=random.choice(Marca.objects.filter(tipo='Herramienta'))
        )
    print("✅ Repuestos, Insumos y Herramientas creados")

    # --- FLUJO DE SERVICIO (Entrada -> Detalle -> Informe -> Factura) ---
    tipos_m = TipoMantenimiento.objects.all()
    for i in range(n):
        entrada = EntradaVehiculo.objects.create(fecha_ingreso=date.today(), hora_ingreso="08:00")
        vehi = random.choice(vehiculos)
        pfe = random.choice(perfiles)
        
        detalle = DetalleServicio.objects.create(
            id_vehiculo=vehi,
            cliente=vehi.id_cliente,
            id_entrada=entrada,
            empresa=empresa_principal,
            empleado=pfe.user,
            proceso='terminado'
        )

        Informes.objects.create(
            detalle_servicio=detalle,
            id_empleado=pfe,
            tipo_informe=random.choice(['Preventivo', 'Correctivo']),
            costo_mano_obra=random.randint(100000, 500000),
            diagnostico_final=fake.text()
        )

        Factura.objects.create(
            empresa=empresa_principal,
            cliente=vehi.id_cliente,
            empleado=pfe,
            detalle_servicio=detalle,
            orden_servicio='mantenimiento',
            metodo_pago='efectivo'
        )
    print("✅ Flujo de servicios completo (Informes y Facturas) creado")

    # Gastos, Caja y Servicios Públicos
    for _ in range(n):
        srv = PagoServiciosPublicos.objects.create(
            servicio=random.choice(['luz', 'agua', 'internet']),
            monto=random.randint(50000, 200000)
        )
        Gastos.objects.create(
            monto=srv.monto,
            descripcion="Pago mensual",
            tipo_gastos='costo fijo',
            id_pagos_servicios=srv
        )
        Caja.objects.create(
            tipo_movimiento=random.choice(['Ingreso', 'Gasto']),
            monto=random.randint(10000, 1000000),
            fecha=date.today(),
            hora="10:00"
        )
    print("✅ Gastos y movimientos de Caja creados")

if __name__ == '__main__':
    try:
        poblar_todo(200)
        print("\n⭐ ¡PROCESO COMPLETADO! 10 registros creados por tabla.")
    except Exception as e:
        print(f"\n❌ Error durante el poblado: {e}")