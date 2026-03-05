import os
import django
import random
import sys
from datetime import date, timedelta
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
    Informes, Factura, Caja, Empresa, Module, Permission,
    Pagos, DetallePago, Nomina, Mantenimiento, DetalleRepuesto,
    DetalleTipoMantenimiento, DetalleInsumos, AlertaStock
)
from backup_module.models import ConfiguracionRespaldo, BackupLog
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
            Marca.objects.get_or_create(nombre=f"{fake.company()[:90]} {random.randint(1,999)}", tipo=t)
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
            TipoMantenimiento.objects.get_or_create(
                nombre=f"Mantenimiento {fake.word()} {i}",
                defaults={'descripcion': fake.sentence()}
            )
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

    # Permisos y Módulos
    for i in range(5):
        try:
            mod, _ = Module.objects.get_or_create(name=f"Modulo_{fake.word()}_{i}", description=fake.sentence())
            users = User.objects.all()
            if users.exists():
                Permission.objects.create(
                    user=random.choice(users),
                    module=mod,
                    view=True,
                    add=random.choice([True, False]),
                    change=random.choice([True, False]),
                    delete=random.choice([True, False])
                )
        except Exception:
            pass
    print("✅ Módulos y Permisos creados")

    # --- ENTIDADES CON DEPENDENCIAS ---

    marcas_v = Marca.objects.filter(tipo='Vehiculo')
    marcas_r = Marca.objects.filter(tipo='Repuesto')
    marcas_i = Marca.objects.filter(tipo='Insumo')
    marcas_h = Marca.objects.filter(tipo='Herramienta')
    clientes = Cliente.objects.all()
    perfiles = Profile.objects.all()
    tipos_m = TipoMantenimiento.objects.all()

    # Vehículos
    for _ in range(n):
        try:
            if clientes.exists() and marcas_v.exists():
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
    for i in range(n):
        try:
            if marcas_r.exists():
                Repuesto.objects.create(
                    id_marca=random.choice(marcas_r),
                    nombre=f"Repuesto {fake.word()} {i}",
                    categoria=random.choice(['automotriz', 'industrial']),
                    fabricante=fake.company(),
                    estado=True
                )
            if marcas_i.exists():
                Insumos.objects.create(
                    id_marca=random.choice(marcas_i),
                    nombre=f"Insumo {fake.word()} {i}",
                    costo=random.randint(5000, 100000),
                    cantidad_medida=random.choice(['galon', 'litro', 'unidades']),
                    stock_minimo=5
                )
            if marcas_h.exists():
                Herramienta.objects.create(
                    nombre=f"Herramienta {fake.word()} {i}",
                    color="Rojo",
                    tipo=random.choice(['manuales', 'eléctricas']),
                    id_marca=random.choice(marcas_h)
                )
        except Exception:
            pass
    print("✅ Repuestos, Insumos y Herramientas creados")

    # --- FLUJO DE SERVICIO (Entrada -> Detalle -> Informe -> Factura) ---
    vehiculos = Vehiculo.objects.all()
    for i in range(n):
        try:
            if vehiculos.exists() and perfiles.exists():
                vehi = random.choice(vehiculos)
                pfe = random.choice(perfiles)
                
                entrada = EntradaVehiculo.objects.create(
                    id_vehiculo=vehi,
                    id_cliente=vehi.id_cliente,
                    fecha_ingreso=date.today() - timedelta(days=random.randint(0, 30)),
                    hora_ingreso="08:00"
                )
                
                detalle = DetalleServicio.objects.create(
                    id_vehiculo=vehi,
                    cliente=vehi.id_cliente,
                    id_entrada=entrada,
                    empresa=empresa_principal,
                    empleado=pfe.user,
                    proceso='terminado'
                )

                # Detalles específicos del servicio
                if Repuesto.objects.exists():
                    DetalleRepuesto.objects.create(
                        detalle_servicio=detalle,
                        id_repuesto=random.choice(Repuesto.objects.all()),
                        cantidad=random.randint(1, 3),
                        precio_unitario=random.randint(50000, 200000)
                    )
                
                if Insumos.objects.exists():
                    DetalleInsumos.objects.create(
                        detalle_servicio=detalle,
                        id_insumos=random.choice(Insumos.objects.all()),
                        cantidad=random.randint(1, 5),
                        precio_unitario=random.randint(10000, 50000)
                    )

                if tipos_m.exists():
                    DetalleTipoMantenimiento.objects.create(
                        detalle_servicio=detalle,
                        id_tipo_mantenimiento=random.choice(tipos_m),
                        empleado=pfe,
                        precio_unitario=random.randint(100000, 300000)
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
        except Exception as e:
            # print(f"Error en flujo: {e}")
            pass
    print("✅ Flujo de servicios completo (Detalles, Informes y Facturas) creado")

    # Mantenimientos independientes
    for _ in range(n):
        try:
            if vehiculos.exists() and perfiles.exists() and tipos_m.exists():
                Mantenimiento.objects.create(
                    fallas=fake.sentence(),
                    procesos=fake.word(),
                    id_vehiculo=random.choice(vehiculos),
                    id_empleado=random.choice(perfiles),
                    id_tipo_mantenimiento=random.choice(tipos_m)
                )
        except Exception:
            pass
    print("✅ Mantenimientos creados")

    # Pagos (Egresos/Compras)
    proveedores = Proveedores.objects.all()
    for _ in range(n):
        try:
            if proveedores.exists():
                pago = Pagos.objects.create(
                    proveedor=random.choice(proveedores),
                    metodo_pago=random.choice(['efectivo', 'transferencia']),
                    monto_total=0
                )
                # Agregar detalles al pago
                DetallePago.objects.create(
                    pago=pago,
                    tipo=random.choice(['Repuesto', 'Insumo', 'Herramienta']),
                    descripcion=fake.word(),
                    cantidad=random.randint(1, 10),
                    precio_unitario=random.randint(1000, 50000)
                )
                pago.recalcular_total()
                pago.save()
        except Exception:
            pass
    print("✅ Pagos y Detalles de Pago creados")

    # Nomina
    for _ in range(n):
        try:
            if perfiles.exists():
                Nomina.objects.create(
                    empleado=random.choice(perfiles),
                    monto=random.randint(1000000, 3000000),
                    fecha_pago=date.today()
                )
        except Exception:
            pass
    print("✅ Nóminas creadas")

    # Gastos, Caja y Servicios Públicos
    nominas = Nomina.objects.all()
    for _ in range(n):
        try:
            srv = PagoServiciosPublicos.objects.create(
                servicio=random.choice(['luz', 'agua', 'gas', 'internet']),
                monto=random.randint(50000, 200000)
            )
            Gastos.objects.create(
                monto=srv.monto,
                descripcion="Pago mensual de servicio",
                tipo_gastos='costo fijo',
                id_pagos_servicios=srv,
                nomina=random.choice(nominas) if nominas.exists() else None
            )
            Caja.objects.create(
                tipo_movimiento=random.choice(['Ingreso', 'Gasto', 'Nomina']),
                monto=random.randint(10000, 1000000),
                fecha=date.today(),
                descripcion=fake.sentence()[:255]
            )
        except Exception:
            pass
    print("✅ Gastos y movimientos de Caja creados")

    # Alertas de Stock
    for _ in range(5):
        try:
            AlertaStock.objects.create(
                nombre_item=fake.word(),
                tipo=random.choice(['Repuesto', 'Insumo', 'Herramienta']),
                stock_actual=random.randint(1, 4),
                stock_minimo=5,
                nivel='Critico'
            )
        except Exception:
            pass
    print("✅ Alertas de Stock creadas")

    # --- RESPALDOS ---
    try:
        ConfiguracionRespaldo.objects.get_or_create(frecuencia='semanal', hora_ejecucion='03:00:00')
        for _ in range(5):
            BackupLog.objects.create(
                tipo=random.choice(['Manual', 'Automático']),
                estado='Éxito',
                tamaño_mb=random.uniform(1.0, 50.0),
                ruta_archivo=f"/backups/db_{fake.bothify(text='####')}.sql",
                fecha_fin=timezone.now() if 'timezone' in globals() else None
            )
    except Exception:
        pass
    print("✅ Configuración y Logs de Respaldo creados")

if __name__ == '__main__':
    try:
        # Importar timezone al final si es necesario para evitar problemas de circularidad o setup
        from django.utils import timezone
        poblar_todo(50) # Limitado a 50 por tabla
        print("\n⭐ ¡PROCESO COMPLETADO! Registros creados en todas las tablas.")
    except Exception as e:
        print(f"\n❌ Error durante el poblado: {e}")