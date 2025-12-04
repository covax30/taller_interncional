from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apy.models import (
    TipoMantenimiento, Marca, Repuesto, Herramienta, Insumos,
    Cliente, Vehiculo, EntradaVehiculo, SalidaVehiculo,
    Administrador, PagoServiciosPublicos, Proveedores, Gastos,
    Empleado, Mantenimiento, Informes, Nomina, Pagos,
    DetalleServicio, DetalleRepuesto, DetalleTipoMantenimiento, DetalleInsumos,
    Empresa, Factura, Compra, Caja, Module, Permission
)
from django.utils import timezone
import random
from datetime import datetime, timedelta
from decimal import Decimal

class Command(BaseCommand):
    help = 'Carga datos de prueba completos para toda la aplicación APY'
    
    def handle(self, *args, **options):
        self.stdout.write('🚀 Iniciando carga de datos de prueba para Taller Internacional...')
        
        # Limpiar datos existentes (opcional, comentar si quieres mantener)
        # self.limpiar_datos()
        
        # 1. Usuario y permisos
        admin_user = self.crear_superusuario()
        
        # 2. Módulos y permisos
        self.crear_modulos_y_permisos(admin_user)
        
        # 3. Empresa (solo una)
        empresa = self.crear_empresa()
        
        # 4. Tipos de mantenimiento
        tipos_mantenimiento = self.crear_tipos_mantenimiento()
        
        # 5. Marcas
        marcas = self.crear_marcas()
        
        # 6. Repuestos
        repuestos = self.crear_repuestos(marcas)
        
        # 7. Herramientas
        herramientas = self.crear_herramientas(marcas)
        
        # 8. Insumos
        insumos = self.crear_insumos(marcas)
        
        # 9. Administradores
        administradores = self.crear_administradores()
        
        # 10. Empleados
        empleados = self.crear_empleados()
        
        # 11. Clientes
        clientes = self.crear_clientes()
        
        # 12. Vehículos
        vehiculos = self.crear_vehiculos(clientes)
        
        # 13. Entradas y salidas de vehículos
        entradas_vehiculos = self.crear_entradas_vehiculos(vehiculos, clientes)
        salidas_vehiculos = self.crear_salidas_vehiculos(vehiculos, clientes)
        
        # 14. Proveedores
        proveedores = self.crear_proveedores()
        
        # 15. Pagos de servicios públicos
        servicios_publicos = self.crear_pagos_servicios()
        
        # 16. Gastos
        gastos = self.crear_gastos(servicios_publicos)
        
        # 17. Mantenimientos
        mantenimientos = self.crear_mantenimientos(vehiculos, empleados, tipos_mantenimiento)
        
        # 18. Informes
        informes = self.crear_informes(repuestos, empleados, mantenimientos)
        
        # 19. Nóminas
        nominas = self.crear_nominas(empleados)
        
        # 20. Pagos
        pagos = self.crear_pagos(proveedores, administradores, herramientas, insumos, repuestos, nominas)
        
        # 21. Detalles de servicio (lo más importante)
        detalles_servicios = self.crear_detalles_servicio(vehiculos, repuestos, tipos_mantenimiento, insumos)
        
        # 22. Facturas
        facturas = self.crear_facturas(empresa, detalles_servicios, empleados, clientes)
        
        # 23. Compras
        compras = self.crear_compras(facturas, proveedores)
        
        # 24. Caja
        cajas = self.crear_caja(administradores, facturas)
        
        self.stdout.write(self.style.SUCCESS('✅ ¡Datos de prueba cargados exitosamente!'))
        self.mostrar_resumen()
    
    def limpiar_datos(self):
        """Opcional: Limpiar datos existentes"""
        confirm = input("⚠️  ¿Desea eliminar todos los datos existentes? [s/N]: ")
        if confirm.lower() == 's':
            for model in [
                Factura, Compra, Caja, DetalleServicio, DetalleRepuesto,
                DetalleTipoMantenimiento, DetalleInsumos, Informes, Mantenimiento,
                Nomina, Pagos, Gastos, PagoServiciosPublicos, EntradaVehiculo,
                SalidaVehiculo, Vehiculo, Cliente, Empleado, Administrador,
                Proveedores, Insumos, Herramienta, Repuesto, Marca, TipoMantenimiento,
                Empresa, Permission, Module
            ]:
                count = model.objects.count()
                model.objects.all().delete()
                if count > 0:
                    self.stdout.write(f"  - Eliminados {count} registros de {model.__name__}")
    
    def crear_superusuario(self):
        if not User.objects.filter(username='admin').exists():
            user = User.objects.create_superuser(
                username='admin',
                email='admin@tallerinternacional.com',
                password='admin123',
                first_name='Administrador',
                last_name='Principal'
            )
            self.stdout.write(self.style.SUCCESS('✓ Superusuario creado: admin / admin123'))
            return user
        else:
            self.stdout.write('✓ Superusuario ya existe')
            return User.objects.get(username='admin')
    
    def crear_modulos_y_permisos(self, user):
        modulos_data = [
            {'name': 'Clientes', 'description': 'Gestión de clientes'},
            {'name': 'Vehículos', 'description': 'Gestión de vehículos'},
            {'name': 'Facturación', 'description': 'Gestión de facturas'},
            {'name': 'Inventario', 'description': 'Gestión de inventario'},
            {'name': 'Mantenimiento', 'description': 'Gestión de mantenimientos'},
            {'name': 'Empleados', 'description': 'Gestión de empleados'},
            {'name': 'Reportes', 'description': 'Generación de reportes'},
            {'name': 'Caja', 'description': 'Gestión de caja'},
        ]
        
        for data in modulos_data:
            modulo, created = Module.objects.get_or_create(
                name=data['name'],
                defaults=data
            )
            
            # Dar todos los permisos al admin
            perm, perm_created = Permission.objects.get_or_create(
                user=user,
                module=modulo,
                defaults={'view': True, 'add': True, 'change': True, 'delete': True}
            )
            
            if created:
                self.stdout.write(f"✓ Módulo creado: {data['name']}")
    
    def crear_empresa(self):
        empresa, created = Empresa.objects.get_or_create(
            nombre="Taller Mecanica Diesel Internacional Arturo Patiño",
            defaults={
                'nit': '74.187366-2',
                'direccion': 'calle 9 #32-37 Barrio La Isla',
                'telefono': '3118112714 - 3133342841',
                'estado': True
            }
        )
        if created:
            self.stdout.write('✓ Empresa principal creada')
        return empresa
    
    def crear_tipos_mantenimiento(self):
        tipos = [
            {'nombre': 'Cambio de Aceite', 'descripcion': 'Cambio de aceite y filtro'},
            {'nombre': 'Alineación', 'descripcion': 'Alineación de dirección'},
            {'nombre': 'Balanceo', 'descripcion': 'Balanceo de ruedas'},
            {'nombre': 'Frenos', 'descripcion': 'Revisión y cambio de sistema de frenos'},
            {'nombre': 'Suspensión', 'descripcion': 'Revisión de sistema de suspensión'},
            {'nombre': 'Motor', 'descripcion': 'Revisión general de motor'},
            {'nombre': 'Transmisión', 'descripcion': 'Mantenimiento de transmisión'},
            {'nombre': 'Electrico', 'descripcion': 'Revisión sistema eléctrico'},
        ]
        
        objetos = []
        for tipo in tipos:
            obj, created = TipoMantenimiento.objects.get_or_create(
                nombre=tipo['nombre'],
                defaults=tipo
            )
            objetos.append(obj)
            if created:
                self.stdout.write(f"✓ Tipo mantenimiento: {tipo['nombre']}")
        
        return objetos
    
    def crear_marcas(self):
        marcas_data = [
            {'nombre': 'Toyota', 'tipo': 'Vehiculo'},
            {'nombre': 'Mazda', 'tipo': 'Vehiculo'},
            {'nombre': 'Ford', 'tipo': 'Vehiculo'},
            {'nombre': 'Chevrolet', 'tipo': 'Vehiculo'},
            {'nombre': 'Bosch', 'tipo': 'Repuesto'},
            {'nombre': 'ACDelco', 'tipo': 'Repuesto'},
            {'nombre': 'Stanley', 'tipo': 'Herramienta'},
            {'nombre': 'Truper', 'tipo': 'Herramienta'},
            {'nombre': 'Castrol', 'tipo': 'Insumo'},
            {'nombre': 'Mobil', 'tipo': 'Insumo'},
        ]
        
        marcas = []
        for data in marcas_data:
            obj, created = Marca.objects.get_or_create(
                nombre=data['nombre'],
                defaults=data
            )
            marcas.append(obj)
            if created:
                self.stdout.write(f"✓ Marca creada: {data['nombre']} ({data['tipo']})")
        
        return marcas
    
    def crear_repuestos(self, marcas):
        repuestos_data = [
            {'nombre': 'Filtro de Aceite', 'categoria': 'automotriz', 'fabricante': 'Bosch', 'stock': 50, 'ubicacion': 'Estante A1', 'precio': 25000},
            {'nombre': 'Pastillas de Freno', 'categoria': 'automotriz', 'fabricante': 'ACDelco', 'stock': 30, 'ubicacion': 'Estante B2', 'precio': 85000},
            {'nombre': 'Batería 12V', 'categoria': 'automotriz', 'fabricante': 'Bosch', 'stock': 15, 'ubicacion': 'Estante C3', 'precio': 320000},
            {'nombre': 'Amortiguadores', 'categoria': 'automotriz', 'fabricante': 'ACDelco', 'stock': 20, 'ubicacion': 'Estante D4', 'precio': 180000},
            {'nombre': 'Correa de Distribución', 'categoria': 'automotriz', 'fabricante': 'Bosch', 'stock': 25, 'ubicacion': 'Estante E5', 'precio': 75000},
            {'nombre': 'Bujías', 'categoria': 'automotriz', 'fabricante': 'ACDelco', 'stock': 100, 'ubicacion': 'Estante F6', 'precio': 15000},
            {'nombre': 'Filtro de Aire', 'categoria': 'automotriz', 'fabricante': 'Bosch', 'stock': 40, 'ubicacion': 'Estante G7', 'precio': 35000},
            {'nombre': 'Radiador', 'categoria': 'automotriz', 'fabricante': 'ACDelco', 'stock': 10, 'ubicacion': 'Estante H8', 'precio': 450000},
        ]
        
        repuestos = []
        marcas_repuesto = [m for m in marcas if m.tipo == 'Repuesto']
        
        for i, data in enumerate(repuestos_data):
            marca = marcas_repuesto[i % len(marcas_repuesto)]
            obj, created = Repuesto.objects.get_or_create(
                nombre=data['nombre'],
                defaults={
                    **data,
                    'id_marca': marca
                }
            )
            repuestos.append(obj)
            if created:
                self.stdout.write(f"✓ Repuesto creado: {data['nombre']} - ${data['precio']:,.0f}")
        
        return repuestos
    
    def crear_herramientas(self, marcas):
        herramientas_data = [
            {'nombre': 'Juego de Llaves Mixtas', 'color': 'Plateado', 'tipo': 'manuales', 'material': 'Acero', 'stock': 10},
            {'nombre': 'Taladro Percutor', 'color': 'Negro/Amarillo', 'tipo': 'eléctricas', 'material': 'Plástico/Metal', 'stock': 5},
            {'nombre': 'Gato Hidráulico', 'color': 'Rojo', 'tipo': 'manuales', 'material': 'Acero', 'stock': 8},
            {'nombre': 'Multímetro Digital', 'color': 'Negro', 'tipo': 'de medición', 'material': 'Plástico', 'stock': 12},
            {'nombre': 'Compresor de Aire', 'color': 'Azul', 'tipo': 'neumáticas', 'material': 'Acero', 'stock': 3},
            {'nombre': 'Llave de Tuercas', 'color': 'Plateado', 'tipo': 'manuales', 'material': 'Acero', 'stock': 15},
        ]
        
        herramientas = []
        marcas_herramienta = [m for m in marcas if m.tipo == 'Herramienta']
        
        for i, data in enumerate(herramientas_data):
            marca = marcas_herramienta[i % len(marcas_herramienta)]
            obj, created = Herramienta.objects.get_or_create(
                nombre=data['nombre'],
                defaults={
                    **data,
                    'id_marca': marca
                }
            )
            herramientas.append(obj)
            if created:
                self.stdout.write(f"✓ Herramienta creada: {data['nombre']}")
        
        return herramientas
    
    def crear_insumos(self, marcas):
        insumos_data = [
            {'costo': 45000, 'stock': 20, 'cantidad': 'litro'},
            {'costo': 38000, 'stock': 15, 'cantidad': 'litro'},
            {'costo': 12000, 'stock': 50, 'cantidad': 'unidades'},
            {'costo': 8000, 'stock': 30, 'cantidad': 'litro'},
            {'costo': 25000, 'stock': 25, 'cantidad': 'litro'},
        ]
        
        insumos = []
        marcas_insumo = [m for m in marcas if m.tipo == 'Insumo']
        nombres_insumos = ['Aceite Sintético', 'Aceite Mineral', 'Filtros Pack', 'Líquido de Frenos', 'Anticongelante']
        
        for i, data in enumerate(insumos_data):
            marca = marcas_insumo[i % len(marcas_insumo)]
            obj, created = Insumos.objects.get_or_create(
                id_marca=marca,
                cantidad=data['cantidad'],
                defaults=data
            )
            insumos.append(obj)
            if created:
                self.stdout.write(f"✓ Insumo creado: {marca.nombre} - ${data['costo']:,.0f}")
        
        return insumos
    
    def crear_administradores(self):
        admins_data = [
            {'nombre': 'Arturo', 'apellidos': 'Patiño', 'identificacion': 12345678, 'edad': 45, 
             'correo': 'arturo@taller.com', 'telefono': 3001234567, 'fecha_ingreso': '2020-01-15'},
            {'nombre': 'María', 'apellidos': 'González', 'identificacion': 87654321, 'edad': 38, 
             'correo': 'maria@taller.com', 'telefono': 3102345678, 'fecha_ingreso': '2021-03-20'},
        ]
        
        admins = []
        for data in admins_data:
            obj, created = Administrador.objects.get_or_create(
                identificacion=data['identificacion'],
                defaults=data
            )
            admins.append(obj)
            if created:
                self.stdout.write(f"✓ Administrador creado: {data['nombre']} {data['apellidos']}")
        
        return admins
    
    def crear_empleados(self):
        empleados_data = [
            {'nombre': 'Carlos Rodríguez', 'telefono': '3101234567', 'identificacion': '1001234567',
             'Correo': 'carlos@taller.com', 'direccion': 'Calle 100 # 15-20'},
            {'nombre': 'Ana Martínez', 'telefono': '3202345678', 'identificacion': '1002345678',
             'Correo': 'ana@taller.com', 'direccion': 'Carrera 50 # 80-30'},
            {'nombre': 'Pedro Gómez', 'telefono': '3153456789', 'identificacion': '1003456789',
             'Correo': 'pedro@taller.com', 'direccion': 'Diagonal 45 # 20-10'},
            {'nombre': 'Laura Sánchez', 'telefono': '3184567890', 'identificacion': '1004567890',
             'Correo': 'laura@taller.com', 'direccion': 'Av. Boyacá # 25-40'},
            {'nombre': 'José Ramírez', 'telefono': '3125678901', 'identificacion': '1005678901',
             'Correo': 'jose@taller.com', 'direccion': 'Calle 72 # 10-15'},
        ]
        
        empleados = []
        for data in empleados_data:
            obj, created = Empleado.objects.get_or_create(
                identificacion=data['identificacion'],
                defaults=data
            )
            empleados.append(obj)
            if created:
                self.stdout.write(f"✓ Empleado creado: {data['nombre']}")
        
        return empleados
    
    def crear_clientes(self):
        clientes_data = [
            {'tipo': 'cliente particular', 'nombre': 'Juan Pérez', 'identificacion': '800123456',
             'telefono': '3001234567', 'correo': 'juan.perez@email.com', 'direccion': 'Carrera 15 # 85-20'},
            {'tipo': 'cliente particular', 'nombre': 'María González', 'identificacion': '800234567',
             'telefono': '3102345678', 'correo': 'maria.gonzalez@email.com', 'direccion': 'Calle 72 # 10-15'},
            {'tipo': 'empresa', 'nombre': 'Empresa Logística S.A.', 'identificacion': '9001234567',
             'telefono': '6017654321', 'correo': 'contacto@empresalogistica.com', 'direccion': 'Av. Boyacá # 25-40'},
            {'tipo': 'cliente particular', 'nombre': 'Roberto Fernández', 'identificacion': '800345678',
             'telefono': '3153456789', 'correo': 'roberto@email.com', 'direccion': 'Diagonal 45 # 20-30'},
            {'tipo': 'empresa', 'nombre': 'Taxi Express Ltda.', 'identificacion': '9002345678',
             'telefono': '6019876543', 'correo': 'info@taxiexpress.com', 'direccion': 'Calle 80 # 12-50'},
            {'tipo': 'cliente particular', 'nombre': 'Sofía Martínez', 'identificacion': '800456789',
             'telefono': '3184567890', 'correo': 'sofia@email.com', 'direccion': 'Calle 100 # 45-60'},
            {'tipo': 'empresa', 'nombre': 'Transportes Rápidos S.A.S.', 'identificacion': '9003456789',
             'telefono': '6018765432', 'correo': 'contacto@transportesrapidos.com', 'direccion': 'Av. Caracas # 30-25'},
        ]
        
        clientes = []
        for data in clientes_data:
            obj, created = Cliente.objects.get_or_create(
                identificacion=data['identificacion'],
                defaults=data
            )
            clientes.append(obj)
            if created:
                self.stdout.write(f"✓ Cliente creado: {data['nombre']} ({data['tipo']})")
        
        return clientes
    
    def crear_vehiculos(self, clientes):
        vehiculos_data = [
            {'placa': 'ABC123', 'modelo_vehiculo': '2020', 'marca_vehiculo': 'Toyota', 'color': 'Blanco'},
            {'placa': 'DEF456', 'modelo_vehiculo': '2021', 'marca_vehiculo': 'Mazda', 'color': 'Rojo'},
            {'placa': 'GHI789', 'modelo_vehiculo': '2019', 'marca_vehiculo': 'Chevrolet', 'color': 'Azul'},
            {'placa': 'JKL012', 'modelo_vehiculo': '2022', 'marca_vehiculo': 'Ford', 'color': 'Negro'},
            {'placa': 'MNO345', 'modelo_vehiculo': '2020', 'marca_vehiculo': 'Toyota', 'color': 'Gris'},
            {'placa': 'PQR678', 'modelo_vehiculo': '2021', 'marca_vehiculo': 'Mazda', 'color': 'Plateado'},
            {'placa': 'STU901', 'modelo_vehiculo': '2018', 'marca_vehiculo': 'Chevrolet', 'color': 'Verde'},
            {'placa': 'VWX234', 'modelo_vehiculo': '2023', 'marca_vehiculo': 'Ford', 'color': 'Blanco'},
        ]
        
        vehiculos = []
        for i, data in enumerate(vehiculos_data):
            cliente = clientes[i % len(clientes)]
            obj, created = Vehiculo.objects.get_or_create(
                placa=data['placa'],
                defaults={
                    **data,
                    'id_cliente': cliente
                }
            )
            vehiculos.append(obj)
            if created:
                self.stdout.write(f"✓ Vehículo creado: {data['placa']} - {data['marca_vehiculo']} {data['color']}")
        
        return vehiculos
    
    def crear_entradas_vehiculos(self, vehiculos, clientes):
        entradas = []
        for i, vehiculo in enumerate(vehiculos):
            fecha = timezone.now().date() - timedelta(days=random.randint(1, 30))
            hora = timezone.now().time().replace(
                hour=random.randint(7, 17),
                minute=random.randint(0, 59)
            )
            
            obj = EntradaVehiculo.objects.create(
                id_vehiculo=vehiculo,
                id_cliente=vehiculo.id_cliente,
                fecha_ingreso=fecha,
                hora_ingreso=hora
            )
            entradas.append(obj)
        
        self.stdout.write(f"✓ {len(entradas)} entradas de vehículos creadas")
        return entradas
    
    def crear_salidas_vehiculos(self, vehiculos, clientes):
        salidas = []
        diagnosticos = [
            'Cambio de aceite completado',
            'Alineación y balanceo realizado',
            'Frenos reparados',
            'Motor revisado y ajustado',
            'Sistema eléctrico reparado',
            'Transmisión revisada',
            'Suspensión ajustada',
            'Mantenimiento preventivo completado'
        ]
        
        for i, vehiculo in enumerate(vehiculos):
            fecha = timezone.now().date() - timedelta(days=random.randint(0, 29))
            hora = timezone.now().time().replace(
                hour=random.randint(14, 19),
                minute=random.randint(0, 59)
            )
            
            obj = SalidaVehiculo.objects.create(
                id_vehiculo=vehiculo,
                id_cliente=vehiculo.id_cliente,
                diagnostico=random.choice(diagnosticos),
                fecha_salida=fecha,
                hora_salida=hora
            )
            salidas.append(obj)
        
        self.stdout.write(f"✓ {len(salidas)} salidas de vehículos creadas")
        return salidas
    
    def crear_proveedores(self):
        proveedores_data = [
            {'nombre': 'Autopartes S.A.', 'telefono': '6011234567', 'correo': 'contacto@autopartes.com'},
            {'nombre': 'Herramientas Industriales Ltda.', 'telefono': '6012345678', 'correo': 'ventas@herramientas.com'},
            {'nombre': 'Lubricantes del Valle', 'telefono': '6013456789', 'correo': 'info@lubricantes.com'},
            {'nombre': 'Repuestos Nacionales', 'telefono': '6014567890', 'correo': 'servicio@repuestos.com'},
        ]
        
        proveedores = []
        for data in proveedores_data:
            obj, created = Proveedores.objects.get_or_create(
                nombre=data['nombre'],
                defaults=data
            )
            proveedores.append(obj)
            if created:
                self.stdout.write(f"✓ Proveedor creado: {data['nombre']}")
        
        return proveedores
    
    def crear_pagos_servicios(self):
        servicios_data = [
            {'servicio': 'luz', 'monto': 350000},
            {'servicio': 'agua', 'monto': 120000},
            {'servicio': 'gas', 'monto': 85000},
            {'servicio': 'internet', 'monto': 180000},
        ]
        
        servicios = []
        for data in servicios_data:
            obj, created = PagoServiciosPublicos.objects.get_or_create(
                servicio=data['servicio'],
                defaults=data
            )
            servicios.append(obj)
            if created:
                self.stdout.write(f"✓ Pago servicio creado: {data['servicio']} - ${data['monto']:,.0f}")
        
        return servicios
    
    def crear_gastos(self, servicios_publicos):
        gastos_data = [
            {'monto': 150000, 'descripcion': 'Compra de materiales de oficina', 'tipo_gastos': 'costo fijo'},
            {'monto': 280000, 'descripcion': 'Publicidad mensual', 'tipo_gastos': 'costo variable'},
            {'monto': 500000, 'descripcion': 'Reparación de equipo', 'tipo_gastos': 'costo directo'},
            {'monto': 75000, 'descripcion': 'Capacitación personal', 'tipo_gastos': 'costo variable'},
        ]
        
        gastos = []
        for i, data in enumerate(gastos_data):
            servicio = servicios_publicos[i % len(servicios_publicos)]
            obj = Gastos.objects.create(
                monto=data['monto'],
                descripcion=data['descripcion'],
                tipo_gastos=data['tipo_gastos'],
                id_pagos_servicios=servicio
            )
            gastos.append(obj)
        
        self.stdout.write(f"✓ {len(gastos)} gastos creados")
        return gastos
    
    def crear_mantenimientos(self, vehiculos, empleados, tipos_mantenimiento):
        mantenimientos = []
        fallas = [
            'Ruido en los frenos',
            'Fuga de aceite',
            'Problemas de dirección',
            'Falla eléctrica',
            'Sobrecalentamiento',
            'Vibración al frenar',
            'Pérdida de potencia',
            'Humo del escape'
        ]
        
        procesos = [
            'Diagnóstico completo',
            'Reparación estándar',
            'Reemplazo de piezas',
            'Ajuste y calibración',
            'Limpieza y mantenimiento',
            'Prueba de funcionamiento'
        ]
        
        for i in range(15):  # Crear 15 mantenimientos
            obj = Mantenimiento.objects.create(
                fallas=random.choice(fallas),
                procesos=random.choice(procesos),
                id_vehiculo=random.choice(vehiculos),
                id_empleado=random.choice(empleados),
                id_tipo_mantenimiento=random.choice(tipos_mantenimiento)
            )
            mantenimientos.append(obj)
        
        self.stdout.write(f"✓ {len(mantenimientos)} mantenimientos creados")
        return mantenimientos
    
    def crear_informes(self, repuestos, empleados, mantenimientos):
        informes = []
        tipos_informe = ['Técnico', 'Financiero', 'Calidad', 'Seguridad']
        
        for i in range(10):  # Crear 10 informes
            fecha = timezone.now().date() - timedelta(days=random.randint(1, 60))
            hora = timezone.now().time().replace(
                hour=random.randint(8, 16),
                minute=random.randint(0, 59)
            )
            
            obj = Informes.objects.create(
                repuestos_usados=random.choice(['Filtros, Bujías', 'Pastillas, Aceite', 'Amortiguadores', 'Batería']),
                costo_mano_obra=random.randint(80000, 250000),
                fecha=fecha,
                hora=hora,
                id_repuesto=random.choice(repuestos),
                id_empleado=random.choice(empleados),
                tipo_informe=random.choice(tipos_informe),
                id_mantenimiento=random.choice(mantenimientos)
            )
            informes.append(obj)
        
        self.stdout.write(f"✓ {len(informes)} informes creados")
        return informes
    
    def crear_nominas(self, empleados):
        nominas = []
        
        for empleado in empleados:
            for _ in range(2):  # 2 nóminas por empleado
                fecha = timezone.now().date() - timedelta(days=random.randint(15, 90))
                monto = random.randint(1200000, 2800000)
                
                obj = Nomina.objects.create(
                    rol='empleado',
                    monto=monto,
                    fecha_pago=fecha,
                    id_empleado=empleado
                )
                nominas.append(obj)
        
        self.stdout.write(f"✓ {len(nominas)} nóminas creadas")
        return nominas
    
    def crear_pagos(self, proveedores, administradores, herramientas, insumos, repuestos, nominas):
        pagos = []
        
        for i in range(20):  # Crear 20 pagos
            fecha = timezone.now().date() - timedelta(days=random.randint(1, 90))
            hora = timezone.now().time().replace(
                hour=random.randint(9, 17),
                minute=random.randint(0, 59)
            )
            
            obj = Pagos.objects.create(
                tipo_pago=random.choice(['Efectivo', 'Transferencia', 'Tarjeta']),
                fecha=fecha,
                hora=hora,
                monto=random.randint(50000, 500000),
                id_proveedor=random.choice(proveedores),
                id_admin=random.choice(administradores),
                id_herramienta=random.choice(herramientas),
                id_insumos=random.choice(insumos),
                id_repuesto=random.choice(repuestos),
                id_nomina=random.choice(nominas) if nominas and random.choice([True, False]) else None
            )
            pagos.append(obj)
        
        self.stdout.write(f"✓ {len(pagos)} pagos creados")
        return pagos
    
    def crear_detalles_servicio(self, vehiculos, repuestos, tipos_mantenimiento, insumos):
        detalles = []
        
        for i in range(25):  # Crear 25 detalles de servicio
            vehiculo = random.choice(vehiculos)
            
            # Crear detalle de servicio principal
            detalle_servicio = DetalleServicio.objects.create(
                id_vehiculo=vehiculo,
                estado=random.choice(['pendiente', 'en_proceso', 'completado'])
            )
            
            # Agregar repuestos al detalle (1-3 repuestos)
            for _ in range(random.randint(1, 3)):
                repuesto = random.choice(repuestos)
                DetalleRepuesto.objects.create(
                    detalle_servicio=detalle_servicio,
                    id_repuesto=repuesto,
                    cantidad=random.randint(1, 4),
                    precio_unitario=repuesto.precio
                )
            
            # Agregar tipos de mantenimiento (1-2 tipos)
            for _ in range(random.randint(1, 2)):
                tipo = random.choice(tipos_mantenimiento)
                DetalleTipoMantenimiento.objects.create(
                    detalle_servicio=detalle_servicio,
                    id_tipo_mantenimiento=tipo,
                    cantidad=1,
                    precio_unitario=random.randint(50000, 300000)
                )
            
            # Agregar insumos (0-2 insumos)
            for _ in range(random.randint(0, 2)):
                insumo = random.choice(insumos)
                DetalleInsumos.objects.create(
                    detalle_servicio=detalle_servicio,
                    id_insumos=insumo,
                    cantidad=random.randint(1, 3),
                    precio_unitario=insumo.costo
                )
            
            detalles.append(detalle_servicio)
        
        self.stdout.write(f"✓ {len(detalles)} detalles de servicio creados")
        return detalles
    
    def crear_facturas(self, empresa, detalles_servicios, empleados, clientes):
        facturas = []
        
        for i, detalle in enumerate(detalles_servicios[:15]):  # 15 facturas
            fecha = timezone.now().date() - timedelta(days=random.randint(0, 30))
            
            factura = Factura.objects.create(
                id_empresa=empresa,
                Fecha=fecha,
                id_Detalles_servicios=detalle,
                id_empleado=random.choice(empleados),
                id_cliente=detalle.id_vehiculo.id_cliente,
                metodo_pago=random.choice(['efectivo', 'transferencia'])
            )
            facturas.append(factura)
        
        self.stdout.write(f"✓ {len(facturas)} facturas creadas")
        return facturas
    
    def crear_compras(self, facturas, proveedores):
        compras = []
        
        for factura in facturas[:10]:  # 10 compras
            fecha = factura.Fecha - timedelta(days=random.randint(1, 7))
            hora = timezone.now().time().replace(
                hour=random.randint(8, 16),
                minute=random.randint(0, 59)
            )
            
            compra = Compra.objects.create(
                id_factura_compra=factura,
                id_proveedor=random.choice(proveedores),
                fecha_compra=fecha,
                hora_compra=hora
            )
            compras.append(compra)
        
        self.stdout.write(f"✓ {len(compras)} compras creadas")
        return compras
    
    def crear_caja(self, administradores, facturas):
        movimientos = []
        tipos = ['Ingreso', 'Gasto', 'Venta', 'Compra']
        
        for i in range(30):  # 30 movimientos de caja
            tipo = random.choice(tipos)
            monto = random.randint(50000, 2000000)
            fecha = timezone.now().date() - timedelta(days=random.randint(0, 90))
            hora = timezone.now().time().replace(
                hour=random.randint(8, 18),
                minute=random.randint(0, 59)
            )
            
            # Solo algunas facturas tienen movimiento de caja
            factura = random.choice(facturas) if facturas and tipo in ['Venta', 'Compra'] else None
            
            movimiento = Caja.objects.create(
                tipo_movimiento=tipo,
                monto=monto,
                fecha=fecha,
                hora=hora,
                id_admin=random.choice(administradores),
                id_Factura=factura
            )
            movimientos.append(movimiento)
        
        self.stdout.write(f"✓ {len(movimientos)} movimientos de caja creados")
        return movimientos
    
    def mostrar_resumen(self):
        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS('📊 RESUMEN DE DATOS CARGADOS'))
        self.stdout.write('='*60)
        
        models_summary = [
            (User, 'Usuarios'),
            (Module, 'Módulos'),
            (Permission, 'Permisos'),
            (Empresa, 'Empresas'),
            (TipoMantenimiento, 'Tipos Mantenimiento'),
            (Marca, 'Marcas'),
            (Repuesto, 'Repuestos'),
            (Herramienta, 'Herramientas'),
            (Insumos, 'Insumos'),
            (Administrador, 'Administradores'),
            (Empleado, 'Empleados'),
            (Cliente, 'Clientes'),
            (Vehiculo, 'Vehículos'),
            (EntradaVehiculo, 'Entradas Vehículos'),
            (SalidaVehiculo, 'Salidas Vehículos'),
            (Proveedores, 'Proveedores'),
            (PagoServiciosPublicos, 'Pagos Servicios'),
            (Gastos, 'Gastos'),
            (Mantenimiento, 'Mantenimientos'),
            (Informes, 'Informes'),
            (Nomina, 'Nóminas'),
            (Pagos, 'Pagos'),
            (DetalleServicio, 'Detalles Servicio'),
            (DetalleRepuesto, 'Detalles Repuesto'),
            (DetalleTipoMantenimiento, 'Detalles Mantenimiento'),
            (DetalleInsumos, 'Detalles Insumos'),
            (Factura, 'Facturas'),
            (Compra, 'Compras'),
            (Caja, 'Movimientos Caja'),
        ]
        
        for model, nombre in models_summary:
            count = model.objects.count()
            self.stdout.write(f"  {nombre:25} : {count:3} registros")
        
        self.stdout.write('='*60)
        self.stdout.write(self.style.SUCCESS('🎉 ¡Base de datos lista para pruebas!'))
        self.stdout.write('\n🔑 Credenciales de acceso:')
        self.stdout.write('   Usuario: admin')
        self.stdout.write('   Contraseña: admin123')
        self.stdout.write('\n🌐 Accede a: http://127.0.0.1:8000/admin/')