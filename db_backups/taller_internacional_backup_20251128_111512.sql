-- MariaDB dump 10.19  Distrib 10.4.32-MariaDB, for Win64 (AMD64)
--
-- Host: localhost    Database: taller_internacional
-- ------------------------------------------------------
-- Server version	8.0.44

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `apy_administrador`
--

DROP TABLE IF EXISTS `apy_administrador`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `apy_administrador` (
  `id_admin` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `apellidos` varchar(100) NOT NULL,
  `identificacion` int NOT NULL,
  `edad` int unsigned NOT NULL,
  `correo` varchar(254) NOT NULL,
  `telefono` int NOT NULL,
  `fecha_ingreso` date NOT NULL,
  PRIMARY KEY (`id_admin`),
  UNIQUE KEY `identificacion` (`identificacion`),
  UNIQUE KEY `correo` (`correo`),
  CONSTRAINT `apy_administrador_chk_1` CHECK ((`edad` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `apy_administrador`
--

LOCK TABLES `apy_administrador` WRITE;
/*!40000 ALTER TABLE `apy_administrador` DISABLE KEYS */;
/*!40000 ALTER TABLE `apy_administrador` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `apy_caja`
--

DROP TABLE IF EXISTS `apy_caja`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `apy_caja` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `tipo_movimiento` varchar(20) NOT NULL,
  `monto` int NOT NULL,
  `fecha` date NOT NULL,
  `hora` time(6) NOT NULL,
  `id_admin_id` int NOT NULL,
  `id_Factura_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `apy_caja_id_admin_id_6c6ac021_fk_apy_administrador_id_admin` (`id_admin_id`),
  KEY `apy_caja_id_Factura_id_76dda90e_fk_apy_factura_id` (`id_Factura_id`),
  CONSTRAINT `apy_caja_id_admin_id_6c6ac021_fk_apy_administrador_id_admin` FOREIGN KEY (`id_admin_id`) REFERENCES `apy_administrador` (`id_admin`),
  CONSTRAINT `apy_caja_id_Factura_id_76dda90e_fk_apy_factura_id` FOREIGN KEY (`id_Factura_id`) REFERENCES `apy_factura` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `apy_caja`
--

LOCK TABLES `apy_caja` WRITE;
/*!40000 ALTER TABLE `apy_caja` DISABLE KEYS */;
/*!40000 ALTER TABLE `apy_caja` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `apy_cliente`
--

DROP TABLE IF EXISTS `apy_cliente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `apy_cliente` (
  `id_cliente` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `documento` bigint NOT NULL,
  `telefono` bigint NOT NULL,
  `correo` varchar(100) NOT NULL,
  `fecha_operacion` date NOT NULL,
  `monto` int NOT NULL,
  PRIMARY KEY (`id_cliente`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `apy_cliente`
--

LOCK TABLES `apy_cliente` WRITE;
/*!40000 ALTER TABLE `apy_cliente` DISABLE KEYS */;
/*!40000 ALTER TABLE `apy_cliente` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `apy_compra`
--

DROP TABLE IF EXISTS `apy_compra`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `apy_compra` (
  `id_compra` int NOT NULL AUTO_INCREMENT,
  `fecha_compra` date NOT NULL,
  `hora_compra` time(6) NOT NULL,
  `id_factura_compra_id` bigint NOT NULL,
  `id_proveedor_id` int NOT NULL,
  PRIMARY KEY (`id_compra`),
  KEY `apy_compra_id_factura_compra_id_4f38666e_fk_apy_factura_id` (`id_factura_compra_id`),
  KEY `apy_compra_id_proveedor_id_f52289b4_fk_apy_prove` (`id_proveedor_id`),
  CONSTRAINT `apy_compra_id_factura_compra_id_4f38666e_fk_apy_factura_id` FOREIGN KEY (`id_factura_compra_id`) REFERENCES `apy_factura` (`id`),
  CONSTRAINT `apy_compra_id_proveedor_id_f52289b4_fk_apy_prove` FOREIGN KEY (`id_proveedor_id`) REFERENCES `apy_proveedores` (`id_proveedor`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `apy_compra`
--

LOCK TABLES `apy_compra` WRITE;
/*!40000 ALTER TABLE `apy_compra` DISABLE KEYS */;
/*!40000 ALTER TABLE `apy_compra` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `apy_empleado`
--

DROP TABLE IF EXISTS `apy_empleado`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `apy_empleado` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `telefono` varchar(15) NOT NULL,
  `identificacion` varchar(20) NOT NULL,
  `Correo` varchar(254) NOT NULL,
  `direccion` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `identificacion` (`identificacion`),
  UNIQUE KEY `Correo` (`Correo`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `apy_empleado`
--

LOCK TABLES `apy_empleado` WRITE;
/*!40000 ALTER TABLE `apy_empleado` DISABLE KEYS */;
INSERT INTO `apy_empleado` VALUES (1,'jose','1233456677','1234567890','sdfs@sdf.sff','dffaedw');
/*!40000 ALTER TABLE `apy_empleado` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `apy_entradavehiculo`
--

DROP TABLE IF EXISTS `apy_entradavehiculo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `apy_entradavehiculo` (
  `id_entrada` int NOT NULL AUTO_INCREMENT,
  `fecha_ingreso` date NOT NULL,
  `hora_ingreso` time(6) NOT NULL,
  `id_cliente_id` int NOT NULL,
  `id_vehiculo_id` int NOT NULL,
  PRIMARY KEY (`id_entrada`),
  KEY `apy_entradavehiculo_id_cliente_id_d4d71a31_fk_apy_clien` (`id_cliente_id`),
  KEY `apy_entradavehiculo_id_vehiculo_id_f2a383df_fk_apy_vehic` (`id_vehiculo_id`),
  CONSTRAINT `apy_entradavehiculo_id_cliente_id_d4d71a31_fk_apy_clien` FOREIGN KEY (`id_cliente_id`) REFERENCES `apy_cliente` (`id_cliente`),
  CONSTRAINT `apy_entradavehiculo_id_vehiculo_id_f2a383df_fk_apy_vehic` FOREIGN KEY (`id_vehiculo_id`) REFERENCES `apy_vehiculo` (`id_vehiculo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `apy_entradavehiculo`
--

LOCK TABLES `apy_entradavehiculo` WRITE;
/*!40000 ALTER TABLE `apy_entradavehiculo` DISABLE KEYS */;
/*!40000 ALTER TABLE `apy_entradavehiculo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `apy_factura`
--

DROP TABLE IF EXISTS `apy_factura`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `apy_factura` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `tipo_pago` varchar(45) NOT NULL,
  `servicio_prestado` varchar(45) NOT NULL,
  `nombre_empresa` varchar(45) NOT NULL,
  `direccion_empresa` varchar(45) NOT NULL,
  `monto` int NOT NULL,
  `id_cliente_id` int NOT NULL,
  `id_empleado_id` bigint NOT NULL,
  `id_tipo_mantenimiento_id` int NOT NULL,
  `id_vehiculo_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `apy_factura_id_vehiculo_id_8eb86e31_fk_apy_vehiculo_id_vehiculo` (`id_vehiculo_id`),
  KEY `apy_factura_id_cliente_id_312f0d53_fk_apy_cliente_id_cliente` (`id_cliente_id`),
  KEY `apy_factura_id_empleado_id_0bd784d5_fk_apy_empleado_id` (`id_empleado_id`),
  KEY `apy_factura_id_tipo_mantenimient_14d61ec4_fk_apy_tipom` (`id_tipo_mantenimiento_id`),
  CONSTRAINT `apy_factura_id_cliente_id_312f0d53_fk_apy_cliente_id_cliente` FOREIGN KEY (`id_cliente_id`) REFERENCES `apy_cliente` (`id_cliente`),
  CONSTRAINT `apy_factura_id_empleado_id_0bd784d5_fk_apy_empleado_id` FOREIGN KEY (`id_empleado_id`) REFERENCES `apy_empleado` (`id`),
  CONSTRAINT `apy_factura_id_tipo_mantenimient_14d61ec4_fk_apy_tipom` FOREIGN KEY (`id_tipo_mantenimiento_id`) REFERENCES `apy_tipomantenimiento` (`id`),
  CONSTRAINT `apy_factura_id_vehiculo_id_8eb86e31_fk_apy_vehiculo_id_vehiculo` FOREIGN KEY (`id_vehiculo_id`) REFERENCES `apy_vehiculo` (`id_vehiculo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `apy_factura`
--

LOCK TABLES `apy_factura` WRITE;
/*!40000 ALTER TABLE `apy_factura` DISABLE KEYS */;
/*!40000 ALTER TABLE `apy_factura` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `apy_gastos`
--

DROP TABLE IF EXISTS `apy_gastos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `apy_gastos` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `monto` int NOT NULL,
  `descripcion` longtext NOT NULL,
  `tipo_gastos` varchar(100) NOT NULL,
  `id_pagos_servicios_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `apy_gastos_id_pagos_servicios_i_bbe5c1bc_fk_apy_pagos` (`id_pagos_servicios_id`),
  CONSTRAINT `apy_gastos_id_pagos_servicios_i_bbe5c1bc_fk_apy_pagos` FOREIGN KEY (`id_pagos_servicios_id`) REFERENCES `apy_pagoserviciospublicos` (`id_servicio`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `apy_gastos`
--

LOCK TABLES `apy_gastos` WRITE;
/*!40000 ALTER TABLE `apy_gastos` DISABLE KEYS */;
/*!40000 ALTER TABLE `apy_gastos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `apy_herramienta`
--

DROP TABLE IF EXISTS `apy_herramienta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `apy_herramienta` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `color` varchar(100) NOT NULL,
  `tipo` varchar(100) NOT NULL,
  `material` varchar(100) NOT NULL,
  `stock` int NOT NULL,
  `id_marca_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `apy_herramienta_id_marca_id_34bf6ec4_fk_apy_marca_id` (`id_marca_id`),
  CONSTRAINT `apy_herramienta_id_marca_id_34bf6ec4_fk_apy_marca_id` FOREIGN KEY (`id_marca_id`) REFERENCES `apy_marca` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `apy_herramienta`
--

LOCK TABLES `apy_herramienta` WRITE;
/*!40000 ALTER TABLE `apy_herramienta` DISABLE KEYS */;
/*!40000 ALTER TABLE `apy_herramienta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `apy_informes`
--

DROP TABLE IF EXISTS `apy_informes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `apy_informes` (
  `id_informe` int NOT NULL AUTO_INCREMENT,
  `repuestos_usados` longtext NOT NULL,
  `costo_mano_obra` int NOT NULL,
  `fecha` date NOT NULL,
  `hora` time(6) NOT NULL,
  `tipo_informe` varchar(100) NOT NULL,
  `id_empleado_id` bigint NOT NULL,
  `id_mantenimiento_id` bigint NOT NULL,
  `id_repuesto_id` bigint NOT NULL,
  PRIMARY KEY (`id_informe`),
  KEY `apy_informes_id_empleado_id_4936ab55_fk_apy_empleado_id` (`id_empleado_id`),
  KEY `apy_informes_id_mantenimiento_id_778e2b52_fk_apy_mante` (`id_mantenimiento_id`),
  KEY `apy_informes_id_repuesto_id_535836d9_fk_apy_repuesto_id` (`id_repuesto_id`),
  CONSTRAINT `apy_informes_id_empleado_id_4936ab55_fk_apy_empleado_id` FOREIGN KEY (`id_empleado_id`) REFERENCES `apy_empleado` (`id`),
  CONSTRAINT `apy_informes_id_mantenimiento_id_778e2b52_fk_apy_mante` FOREIGN KEY (`id_mantenimiento_id`) REFERENCES `apy_mantenimiento` (`id`),
  CONSTRAINT `apy_informes_id_repuesto_id_535836d9_fk_apy_repuesto_id` FOREIGN KEY (`id_repuesto_id`) REFERENCES `apy_repuesto` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `apy_informes`
--

LOCK TABLES `apy_informes` WRITE;
/*!40000 ALTER TABLE `apy_informes` DISABLE KEYS */;
/*!40000 ALTER TABLE `apy_informes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `apy_insumos`
--

DROP TABLE IF EXISTS `apy_insumos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `apy_insumos` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `costo` int NOT NULL,
  `stock` int NOT NULL,
  `cantidad` varchar(20) NOT NULL,
  `id_marca_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `apy_insumos_id_marca_id_418b7293_fk_apy_marca_id` (`id_marca_id`),
  CONSTRAINT `apy_insumos_id_marca_id_418b7293_fk_apy_marca_id` FOREIGN KEY (`id_marca_id`) REFERENCES `apy_marca` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `apy_insumos`
--

LOCK TABLES `apy_insumos` WRITE;
/*!40000 ALTER TABLE `apy_insumos` DISABLE KEYS */;
/*!40000 ALTER TABLE `apy_insumos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `apy_mantenimiento`
--

DROP TABLE IF EXISTS `apy_mantenimiento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `apy_mantenimiento` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `fallas` longtext NOT NULL,
  `procesos` varchar(50) NOT NULL,
  `id_empleado_id` bigint NOT NULL,
  `id_tipo_mantenimiento_id` int NOT NULL,
  `id_vehiculo_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `apy_mantenimiento_id_vehiculo_id_3cf63cf3_fk_apy_vehic` (`id_vehiculo_id`),
  KEY `apy_mantenimiento_id_empleado_id_5bb62a67_fk_apy_empleado_id` (`id_empleado_id`),
  KEY `apy_mantenimiento_id_tipo_mantenimient_3745607e_fk_apy_tipom` (`id_tipo_mantenimiento_id`),
  CONSTRAINT `apy_mantenimiento_id_empleado_id_5bb62a67_fk_apy_empleado_id` FOREIGN KEY (`id_empleado_id`) REFERENCES `apy_empleado` (`id`),
  CONSTRAINT `apy_mantenimiento_id_tipo_mantenimient_3745607e_fk_apy_tipom` FOREIGN KEY (`id_tipo_mantenimiento_id`) REFERENCES `apy_tipomantenimiento` (`id`),
  CONSTRAINT `apy_mantenimiento_id_vehiculo_id_3cf63cf3_fk_apy_vehic` FOREIGN KEY (`id_vehiculo_id`) REFERENCES `apy_vehiculo` (`id_vehiculo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `apy_mantenimiento`
--

LOCK TABLES `apy_mantenimiento` WRITE;
/*!40000 ALTER TABLE `apy_mantenimiento` DISABLE KEYS */;
/*!40000 ALTER TABLE `apy_mantenimiento` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `apy_marca`
--

DROP TABLE IF EXISTS `apy_marca`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `apy_marca` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `tipo` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `apy_marca`
--

LOCK TABLES `apy_marca` WRITE;
/*!40000 ALTER TABLE `apy_marca` DISABLE KEYS */;
/*!40000 ALTER TABLE `apy_marca` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `apy_module`
--

DROP TABLE IF EXISTS `apy_module`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `apy_module` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `apy_module`
--

LOCK TABLES `apy_module` WRITE;
/*!40000 ALTER TABLE `apy_module` DISABLE KEYS */;
/*!40000 ALTER TABLE `apy_module` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `apy_nomina`
--

DROP TABLE IF EXISTS `apy_nomina`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `apy_nomina` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `rol` varchar(100) NOT NULL,
  `monto` int NOT NULL,
  `fecha_pago` date NOT NULL,
  `id_empleado_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `apy_nomina_id_empleado_id_169c0fb5_fk_apy_empleado_id` (`id_empleado_id`),
  CONSTRAINT `apy_nomina_id_empleado_id_169c0fb5_fk_apy_empleado_id` FOREIGN KEY (`id_empleado_id`) REFERENCES `apy_empleado` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `apy_nomina`
--

LOCK TABLES `apy_nomina` WRITE;
/*!40000 ALTER TABLE `apy_nomina` DISABLE KEYS */;
/*!40000 ALTER TABLE `apy_nomina` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `apy_pagos`
--

DROP TABLE IF EXISTS `apy_pagos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `apy_pagos` (
  `id_pago` int NOT NULL AUTO_INCREMENT,
  `tipo_pago` varchar(100) NOT NULL,
  `fecha` date NOT NULL,
  `hora` time(6) NOT NULL,
  `monto` int NOT NULL,
  `id_admin_id` int NOT NULL,
  `id_herramienta_id` bigint NOT NULL,
  `id_insumos_id` bigint NOT NULL,
  `id_nomina_id` bigint DEFAULT NULL,
  `id_proveedor_id` int NOT NULL,
  `id_repuestos_id` bigint NOT NULL,
  PRIMARY KEY (`id_pago`),
  KEY `apy_pagos_id_admin_id_a827a062_fk_apy_administrador_id_admin` (`id_admin_id`),
  KEY `apy_pagos_id_herramienta_id_53138c09_fk_apy_herramienta_id` (`id_herramienta_id`),
  KEY `apy_pagos_id_insumos_id_48036cd5_fk_apy_insumos_id` (`id_insumos_id`),
  KEY `apy_pagos_id_nomina_id_5994835f_fk_apy_nomina_id` (`id_nomina_id`),
  KEY `apy_pagos_id_proveedor_id_9456b11c_fk_apy_prove` (`id_proveedor_id`),
  KEY `apy_pagos_id_repuestos_id_db7c58e6_fk_apy_repuesto_id` (`id_repuestos_id`),
  CONSTRAINT `apy_pagos_id_admin_id_a827a062_fk_apy_administrador_id_admin` FOREIGN KEY (`id_admin_id`) REFERENCES `apy_administrador` (`id_admin`),
  CONSTRAINT `apy_pagos_id_herramienta_id_53138c09_fk_apy_herramienta_id` FOREIGN KEY (`id_herramienta_id`) REFERENCES `apy_herramienta` (`id`),
  CONSTRAINT `apy_pagos_id_insumos_id_48036cd5_fk_apy_insumos_id` FOREIGN KEY (`id_insumos_id`) REFERENCES `apy_insumos` (`id`),
  CONSTRAINT `apy_pagos_id_nomina_id_5994835f_fk_apy_nomina_id` FOREIGN KEY (`id_nomina_id`) REFERENCES `apy_nomina` (`id`),
  CONSTRAINT `apy_pagos_id_proveedor_id_9456b11c_fk_apy_prove` FOREIGN KEY (`id_proveedor_id`) REFERENCES `apy_proveedores` (`id_proveedor`),
  CONSTRAINT `apy_pagos_id_repuestos_id_db7c58e6_fk_apy_repuesto_id` FOREIGN KEY (`id_repuestos_id`) REFERENCES `apy_repuesto` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `apy_pagos`
--

LOCK TABLES `apy_pagos` WRITE;
/*!40000 ALTER TABLE `apy_pagos` DISABLE KEYS */;
/*!40000 ALTER TABLE `apy_pagos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `apy_pagoserviciospublicos`
--

DROP TABLE IF EXISTS `apy_pagoserviciospublicos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `apy_pagoserviciospublicos` (
  `servicio` varchar(20) NOT NULL,
  `id_servicio` int NOT NULL AUTO_INCREMENT,
  `monto` int NOT NULL,
  PRIMARY KEY (`id_servicio`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `apy_pagoserviciospublicos`
--

LOCK TABLES `apy_pagoserviciospublicos` WRITE;
/*!40000 ALTER TABLE `apy_pagoserviciospublicos` DISABLE KEYS */;
/*!40000 ALTER TABLE `apy_pagoserviciospublicos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `apy_permission`
--

DROP TABLE IF EXISTS `apy_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `apy_permission` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `view` tinyint(1) NOT NULL,
  `add` tinyint(1) NOT NULL,
  `change` tinyint(1) NOT NULL,
  `delete` tinyint(1) NOT NULL,
  `module_id` bigint NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `apy_permission_module_id_17c9325b_fk_apy_module_id` (`module_id`),
  KEY `apy_permission_user_id_53f1b237_fk_auth_user_id` (`user_id`),
  CONSTRAINT `apy_permission_module_id_17c9325b_fk_apy_module_id` FOREIGN KEY (`module_id`) REFERENCES `apy_module` (`id`),
  CONSTRAINT `apy_permission_user_id_53f1b237_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `apy_permission`
--

LOCK TABLES `apy_permission` WRITE;
/*!40000 ALTER TABLE `apy_permission` DISABLE KEYS */;
/*!40000 ALTER TABLE `apy_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `apy_proveedores`
--

DROP TABLE IF EXISTS `apy_proveedores`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `apy_proveedores` (
  `id_proveedor` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `telefono` varchar(20) NOT NULL,
  `correo` varchar(254) NOT NULL,
  PRIMARY KEY (`id_proveedor`),
  UNIQUE KEY `correo` (`correo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `apy_proveedores`
--

LOCK TABLES `apy_proveedores` WRITE;
/*!40000 ALTER TABLE `apy_proveedores` DISABLE KEYS */;
/*!40000 ALTER TABLE `apy_proveedores` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `apy_repuesto`
--

DROP TABLE IF EXISTS `apy_repuesto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `apy_repuesto` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `categoria` varchar(100) NOT NULL,
  `fabricante` varchar(100) NOT NULL,
  `stock` int NOT NULL,
  `ubicacion` varchar(100) NOT NULL,
  `precio` int NOT NULL,
  `id_marca_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `apy_repuesto_id_marca_id_5f9d858b_fk_apy_marca_id` (`id_marca_id`),
  CONSTRAINT `apy_repuesto_id_marca_id_5f9d858b_fk_apy_marca_id` FOREIGN KEY (`id_marca_id`) REFERENCES `apy_marca` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `apy_repuesto`
--

LOCK TABLES `apy_repuesto` WRITE;
/*!40000 ALTER TABLE `apy_repuesto` DISABLE KEYS */;
/*!40000 ALTER TABLE `apy_repuesto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `apy_salidavehiculo`
--

DROP TABLE IF EXISTS `apy_salidavehiculo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `apy_salidavehiculo` (
  `id_salida` int NOT NULL AUTO_INCREMENT,
  `diagnostico` varchar(100) NOT NULL,
  `fecha_salida` date NOT NULL,
  `hora_salida` time(6) NOT NULL,
  `id_cliente_id` int NOT NULL,
  `id_vehiculo_id` int NOT NULL,
  PRIMARY KEY (`id_salida`),
  KEY `apy_salidavehiculo_id_cliente_id_14ff222e_fk_apy_clien` (`id_cliente_id`),
  KEY `apy_salidavehiculo_id_vehiculo_id_3ec761cd_fk_apy_vehic` (`id_vehiculo_id`),
  CONSTRAINT `apy_salidavehiculo_id_cliente_id_14ff222e_fk_apy_clien` FOREIGN KEY (`id_cliente_id`) REFERENCES `apy_cliente` (`id_cliente`),
  CONSTRAINT `apy_salidavehiculo_id_vehiculo_id_3ec761cd_fk_apy_vehic` FOREIGN KEY (`id_vehiculo_id`) REFERENCES `apy_vehiculo` (`id_vehiculo`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `apy_salidavehiculo`
--

LOCK TABLES `apy_salidavehiculo` WRITE;
/*!40000 ALTER TABLE `apy_salidavehiculo` DISABLE KEYS */;
/*!40000 ALTER TABLE `apy_salidavehiculo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `apy_tipomantenimiento`
--

DROP TABLE IF EXISTS `apy_tipomantenimiento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `apy_tipomantenimiento` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  `descripcion` longtext,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `apy_tipomantenimiento`
--

LOCK TABLES `apy_tipomantenimiento` WRITE;
/*!40000 ALTER TABLE `apy_tipomantenimiento` DISABLE KEYS */;
/*!40000 ALTER TABLE `apy_tipomantenimiento` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `apy_vehiculo`
--

DROP TABLE IF EXISTS `apy_vehiculo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `apy_vehiculo` (
  `id_vehiculo` int NOT NULL AUTO_INCREMENT,
  `placa` varchar(10) NOT NULL,
  `modelo_vehiculo` varchar(4) NOT NULL,
  `marca_vehiculo` varchar(100) NOT NULL,
  `color` varchar(100) NOT NULL,
  `id_cliente_id` int NOT NULL,
  PRIMARY KEY (`id_vehiculo`),
  UNIQUE KEY `placa` (`placa`),
  KEY `apy_vehiculo_id_cliente_id_692bca9a_fk_apy_cliente_id_cliente` (`id_cliente_id`),
  CONSTRAINT `apy_vehiculo_id_cliente_id_692bca9a_fk_apy_cliente_id_cliente` FOREIGN KEY (`id_cliente_id`) REFERENCES `apy_cliente` (`id_cliente`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `apy_vehiculo`
--

LOCK TABLES `apy_vehiculo` WRITE;
/*!40000 ALTER TABLE `apy_vehiculo` DISABLE KEYS */;
/*!40000 ALTER TABLE `apy_vehiculo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=133 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add administrador',7,'add_administrador'),(26,'Can change administrador',7,'change_administrador'),(27,'Can delete administrador',7,'delete_administrador'),(28,'Can view administrador',7,'view_administrador'),(29,'Can add cliente',8,'add_cliente'),(30,'Can change cliente',8,'change_cliente'),(31,'Can delete cliente',8,'delete_cliente'),(32,'Can view cliente',8,'view_cliente'),(33,'Can add Configuración de Respaldo',9,'add_configuracionrespaldo'),(34,'Can change Configuración de Respaldo',9,'change_configuracionrespaldo'),(35,'Can delete Configuración de Respaldo',9,'delete_configuracionrespaldo'),(36,'Can view Configuración de Respaldo',9,'view_configuracionrespaldo'),(37,'Can add empleado',10,'add_empleado'),(38,'Can change empleado',10,'change_empleado'),(39,'Can delete empleado',10,'delete_empleado'),(40,'Can view empleado',10,'view_empleado'),(41,'Can add marca',11,'add_marca'),(42,'Can change marca',11,'change_marca'),(43,'Can delete marca',11,'delete_marca'),(44,'Can view marca',11,'view_marca'),(45,'Can add module',12,'add_module'),(46,'Can change module',12,'change_module'),(47,'Can delete module',12,'delete_module'),(48,'Can view module',12,'view_module'),(49,'Can add pago servicios publicos',13,'add_pagoserviciospublicos'),(50,'Can change pago servicios publicos',13,'change_pagoserviciospublicos'),(51,'Can delete pago servicios publicos',13,'delete_pagoserviciospublicos'),(52,'Can view pago servicios publicos',13,'view_pagoserviciospublicos'),(53,'Can add proveedores',14,'add_proveedores'),(54,'Can change proveedores',14,'change_proveedores'),(55,'Can delete proveedores',14,'delete_proveedores'),(56,'Can view proveedores',14,'view_proveedores'),(57,'Can add tipo mantenimiento',15,'add_tipomantenimiento'),(58,'Can change tipo mantenimiento',15,'change_tipomantenimiento'),(59,'Can delete tipo mantenimiento',15,'delete_tipomantenimiento'),(60,'Can view tipo mantenimiento',15,'view_tipomantenimiento'),(61,'Can add Registro de Respaldo',16,'add_backuplog'),(62,'Can change Registro de Respaldo',16,'change_backuplog'),(63,'Can delete Registro de Respaldo',16,'delete_backuplog'),(64,'Can view Registro de Respaldo',16,'view_backuplog'),(65,'Can add factura',17,'add_factura'),(66,'Can change factura',17,'change_factura'),(67,'Can delete factura',17,'delete_factura'),(68,'Can view factura',17,'view_factura'),(69,'Can add caja',18,'add_caja'),(70,'Can change caja',18,'change_caja'),(71,'Can delete caja',18,'delete_caja'),(72,'Can view caja',18,'view_caja'),(73,'Can add mantenimiento',19,'add_mantenimiento'),(74,'Can change mantenimiento',19,'change_mantenimiento'),(75,'Can delete mantenimiento',19,'delete_mantenimiento'),(76,'Can view mantenimiento',19,'view_mantenimiento'),(77,'Can add insumos',20,'add_insumos'),(78,'Can change insumos',20,'change_insumos'),(79,'Can delete insumos',20,'delete_insumos'),(80,'Can view insumos',20,'view_insumos'),(81,'Can add herramienta',21,'add_herramienta'),(82,'Can change herramienta',21,'change_herramienta'),(83,'Can delete herramienta',21,'delete_herramienta'),(84,'Can view herramienta',21,'view_herramienta'),(85,'Can add nomina',22,'add_nomina'),(86,'Can change nomina',22,'change_nomina'),(87,'Can delete nomina',22,'delete_nomina'),(88,'Can view nomina',22,'view_nomina'),(89,'Can add gastos',23,'add_gastos'),(90,'Can change gastos',23,'change_gastos'),(91,'Can delete gastos',23,'delete_gastos'),(92,'Can view gastos',23,'view_gastos'),(93,'Can add permission',24,'add_permission'),(94,'Can change permission',24,'change_permission'),(95,'Can delete permission',24,'delete_permission'),(96,'Can view permission',24,'view_permission'),(97,'Can add compra',25,'add_compra'),(98,'Can change compra',25,'change_compra'),(99,'Can delete compra',25,'delete_compra'),(100,'Can view compra',25,'view_compra'),(101,'Can add repuesto',26,'add_repuesto'),(102,'Can change repuesto',26,'change_repuesto'),(103,'Can delete repuesto',26,'delete_repuesto'),(104,'Can view repuesto',26,'view_repuesto'),(105,'Can add pagos',27,'add_pagos'),(106,'Can change pagos',27,'change_pagos'),(107,'Can delete pagos',27,'delete_pagos'),(108,'Can view pagos',27,'view_pagos'),(109,'Can add informes',28,'add_informes'),(110,'Can change informes',28,'change_informes'),(111,'Can delete informes',28,'delete_informes'),(112,'Can view informes',28,'view_informes'),(113,'Can add vehiculo',29,'add_vehiculo'),(114,'Can change vehiculo',29,'change_vehiculo'),(115,'Can delete vehiculo',29,'delete_vehiculo'),(116,'Can view vehiculo',29,'view_vehiculo'),(117,'Can add salida vehiculo',30,'add_salidavehiculo'),(118,'Can change salida vehiculo',30,'change_salidavehiculo'),(119,'Can delete salida vehiculo',30,'delete_salidavehiculo'),(120,'Can view salida vehiculo',30,'view_salidavehiculo'),(121,'Can add entrada vehiculo',31,'add_entradavehiculo'),(122,'Can change entrada vehiculo',31,'change_entradavehiculo'),(123,'Can delete entrada vehiculo',31,'delete_entradavehiculo'),(124,'Can view entrada vehiculo',31,'view_entradavehiculo'),(125,'Can add Configuración de Respaldo',32,'add_configuracionrespaldo'),(126,'Can change Configuración de Respaldo',32,'change_configuracionrespaldo'),(127,'Can delete Configuración de Respaldo',32,'delete_configuracionrespaldo'),(128,'Can view Configuración de Respaldo',32,'view_configuracionrespaldo'),(129,'Can add Registro de Respaldo',33,'add_backuplog'),(130,'Can change Registro de Respaldo',33,'change_backuplog'),(131,'Can delete Registro de Respaldo',33,'delete_backuplog'),(132,'Can view Registro de Respaldo',33,'view_backuplog');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$1000000$zyePLzrKKQnlx2Wj6GKlg1$SCcvM4Dd3uOw9EJXQaw6341OX0jdOlSyg+JSNjyWYVk=','2025-11-27 11:37:06.069531',1,'erick','','','erickcovisfero@gmail.com',1,1,'2025-10-31 16:17:51.142945');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `backup_module_backuplog`
--

DROP TABLE IF EXISTS `backup_module_backuplog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `backup_module_backuplog` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `fecha_inicio` datetime(6) NOT NULL,
  `fecha_fin` datetime(6) DEFAULT NULL,
  `tipo` varchar(10) NOT NULL,
  `estado` varchar(10) NOT NULL,
  `tamaño_mb` double DEFAULT NULL,
  `ruta_archivo` varchar(255) DEFAULT NULL,
  `usuario_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `backup_module_backuplog_usuario_id_81022408_fk_auth_user_id` (`usuario_id`),
  CONSTRAINT `backup_module_backuplog_usuario_id_81022408_fk_auth_user_id` FOREIGN KEY (`usuario_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `backup_module_backuplog`
--

LOCK TABLES `backup_module_backuplog` WRITE;
/*!40000 ALTER TABLE `backup_module_backuplog` DISABLE KEYS */;
INSERT INTO `backup_module_backuplog` VALUES (1,'2025-11-10 16:38:37.552988','2025-11-10 16:38:37.808826','Manual','Fallo',NULL,'D:\\Users\\User\\Desktop\\taller_interncional\\db_backups\\taller_internacional_backup_20251110_113837.sql',1),(2,'2025-11-10 16:52:06.846652','2025-11-10 16:52:06.897567','Manual','Fallo',NULL,'D:\\Users\\User\\Desktop\\taller_interncional\\db_backups\\taller_internacional_backup_20251110_115206.sql',1),(3,'2025-11-10 16:52:07.046195','2025-11-10 16:52:07.088350','Manual','Fallo',NULL,'D:\\Users\\User\\Desktop\\taller_interncional\\db_backups\\taller_internacional_backup_20251110_115207.sql',1),(4,'2025-11-11 11:56:15.841866','2025-11-11 11:56:15.934358','Manual','Fallo',NULL,'D:\\Users\\User\\Desktop\\taller_interncional\\db_backups\\taller_internacional_backup_20251111_065615.sql',1),(5,'2025-11-11 11:56:15.853297','2025-11-11 11:56:15.936927','Manual','Fallo',NULL,'D:\\Users\\User\\Desktop\\taller_interncional\\db_backups\\taller_internacional_backup_20251111_065615.sql',1),(6,'2025-11-11 12:03:33.041397','2025-11-11 12:03:33.079780','Automático','Fallo',NULL,'D:\\Users\\User\\Desktop\\taller_interncional\\db_backups\\taller_internacional_backup_20251111_070333.sql',NULL),(7,'2025-11-11 12:17:18.405742','2025-11-11 12:17:18.750267','Automático','Éxito',0.05,'D:\\Users\\User\\Desktop\\taller_interncional\\db_backups\\taller_internacional_backup_20251111_071718.sql',NULL),(8,'2025-11-11 12:19:03.851932','2025-11-11 12:19:03.980165','Manual','Éxito',0.05,'D:\\Users\\User\\Desktop\\taller_interncional\\db_backups\\taller_internacional_backup_20251111_071903.sql',1),(9,'2025-11-11 12:19:03.943381','2025-11-11 12:19:04.086049','Manual','Éxito',0.05,'D:\\Users\\User\\Desktop\\taller_interncional\\db_backups\\taller_internacional_backup_20251111_071903.sql',1),(10,'2025-11-11 12:19:29.428688','2025-11-11 12:19:29.584952','Manual','Éxito',0.05,'D:\\Users\\User\\Desktop\\taller_interncional\\db_backups\\taller_internacional_backup_20251111_071929.sql',1),(11,'2025-11-11 12:19:29.512206','2025-11-11 12:19:29.668178','Manual','Éxito',0.05,'D:\\Users\\User\\Desktop\\taller_interncional\\db_backups\\taller_internacional_backup_20251111_071929.sql',1),(12,'2025-11-11 14:34:00.718617','2025-11-11 14:34:01.044252','Manual','Éxito',0.05,'D:\\Users\\User\\Desktop\\taller_interncional\\db_backups\\taller_internacional_backup_20251111_093400.sql',1),(13,'2025-11-11 14:34:00.736212','2025-11-11 14:34:01.035459','Manual','Éxito',0.05,'D:\\Users\\User\\Desktop\\taller_interncional\\db_backups\\taller_internacional_backup_20251111_093400.sql',1),(14,'2025-11-11 15:24:16.204786','2025-11-11 15:24:16.629837','Manual','Éxito',0.05,'D:\\Users\\User\\Desktop\\taller_interncional\\db_backups\\taller_internacional_backup_20251111_102416.sql',1),(15,'2025-11-11 15:24:16.344204','2025-11-11 15:24:16.626239','Manual','Éxito',0.05,'D:\\Users\\User\\Desktop\\taller_interncional\\db_backups\\taller_internacional_backup_20251111_102416.sql',1),(16,'2025-11-11 15:36:32.930083','2025-11-11 15:36:33.253637','Manual','Éxito',0.05,'D:\\Users\\User\\Desktop\\taller_interncional\\db_backups\\taller_internacional_backup_20251111_103632.sql',1),(17,'2025-11-11 15:36:33.207436','2025-11-11 15:36:33.510317','Manual','Éxito',0.05,'D:\\Users\\User\\Desktop\\taller_interncional\\db_backups\\taller_internacional_backup_20251111_103633.sql',1),(18,'2025-11-11 15:37:17.997540','2025-11-11 15:37:18.296060','Manual','Éxito',0.05,'D:\\Users\\User\\Desktop\\taller_interncional\\db_backups\\taller_internacional_backup_20251111_103718.sql',1),(19,'2025-11-11 15:37:18.215994','2025-11-11 15:37:18.518218','Manual','Éxito',0.05,'D:\\Users\\User\\Desktop\\taller_interncional\\db_backups\\taller_internacional_backup_20251111_103718.sql',1),(20,'2025-11-11 15:37:57.761189','2025-11-11 15:37:57.966728','Manual','Éxito',0.05,'D:\\Users\\User\\Desktop\\taller_interncional\\db_backups\\taller_internacional_backup_20251111_103757.sql',1),(21,'2025-11-11 15:37:57.951068','2025-11-11 15:37:58.153252','Manual','Éxito',0.05,'D:\\Users\\User\\Desktop\\taller_interncional\\db_backups\\taller_internacional_backup_20251111_103757.sql',1),(22,'2025-11-11 15:44:51.580756','2025-11-11 15:44:51.805884','Manual','Éxito',0.05,'D:\\Users\\User\\Desktop\\taller_interncional\\db_backups\\taller_internacional_backup_20251111_104451.sql',1),(23,'2025-11-11 15:44:51.806527','2025-11-11 15:44:52.028402','Manual','Éxito',0.05,'D:\\Users\\User\\Desktop\\taller_interncional\\db_backups\\taller_internacional_backup_20251111_104451.sql',1),(24,'2025-11-12 14:43:19.294647','2025-11-12 14:43:19.720642','Manual','Éxito',0.05,'D:\\Users\\User\\Desktop\\taller_interncional\\db_backups\\taller_internacional_backup_20251112_094319.sql',1),(25,'2025-11-12 14:43:19.398158','2025-11-12 14:43:19.721648','Manual','Éxito',0.05,'D:\\Users\\User\\Desktop\\taller_interncional\\db_backups\\taller_internacional_backup_20251112_094319.sql',1),(26,'2025-11-13 16:27:37.987836',NULL,'Manual','En Proceso',NULL,NULL,1),(27,'2025-11-13 16:27:38.367825',NULL,'Manual','En Proceso',NULL,NULL,1),(28,'2025-11-26 12:28:26.868788',NULL,'Manual','En Proceso',NULL,NULL,1),(29,'2025-11-26 12:29:23.052420',NULL,'Manual','En Proceso',NULL,NULL,1),(30,'2025-11-26 12:34:34.276694','2025-11-26 12:34:34.557321','Manual','Éxito',0.05,'D:\\Users\\User\\Desktop\\taller_interncional\\db_backups\\taller_internacional_backup_20251126_073434.sql',1),(31,'2025-11-26 12:45:47.174479','2025-11-26 12:45:47.462137','Manual','Éxito',0.05,'D:\\Users\\User\\Desktop\\taller_interncional\\db_backups\\taller_internacional_backup_20251126_074547.sql',1),(32,'2025-11-26 12:59:26.214287','2025-11-26 12:59:26.499738','Manual','Éxito',0.05,'D:\\Users\\User\\Desktop\\taller_interncional\\db_backups\\taller_internacional_backup_20251126_075926.sql',1),(33,'2025-11-26 14:58:09.050066',NULL,'Manual','En Proceso',NULL,NULL,1),(34,'2025-11-27 11:39:08.895448',NULL,'Manual','En Proceso',NULL,NULL,1),(35,'2025-11-27 11:40:36.033004',NULL,'Manual','En Proceso',NULL,NULL,1),(36,'2025-11-28 16:15:12.887146',NULL,'Manual','En Proceso',NULL,NULL,1);
/*!40000 ALTER TABLE `backup_module_backuplog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `backup_module_configuracionrespaldo`
--

DROP TABLE IF EXISTS `backup_module_configuracionrespaldo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `backup_module_configuracionrespaldo` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `frecuencia` varchar(10) NOT NULL,
  `hora_ejecucion` time(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `backup_module_configuracionrespaldo`
--

LOCK TABLES `backup_module_configuracionrespaldo` WRITE;
/*!40000 ALTER TABLE `backup_module_configuracionrespaldo` DISABLE KEYS */;
/*!40000 ALTER TABLE `backup_module_configuracionrespaldo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(7,'apy','administrador'),(16,'apy','backuplog'),(18,'apy','caja'),(8,'apy','cliente'),(25,'apy','compra'),(9,'apy','configuracionrespaldo'),(10,'apy','empleado'),(31,'apy','entradavehiculo'),(17,'apy','factura'),(23,'apy','gastos'),(21,'apy','herramienta'),(28,'apy','informes'),(20,'apy','insumos'),(19,'apy','mantenimiento'),(11,'apy','marca'),(12,'apy','module'),(22,'apy','nomina'),(27,'apy','pagos'),(13,'apy','pagoserviciospublicos'),(24,'apy','permission'),(14,'apy','proveedores'),(26,'apy','repuesto'),(30,'apy','salidavehiculo'),(15,'apy','tipomantenimiento'),(29,'apy','vehiculo'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(33,'backup_module','backuplog'),(32,'backup_module','configuracionrespaldo'),(5,'contenttypes','contenttype'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-10-31 16:15:41.943191'),(2,'auth','0001_initial','2025-10-31 16:15:42.600574'),(3,'admin','0001_initial','2025-10-31 16:15:42.759049'),(4,'admin','0002_logentry_remove_auto_add','2025-10-31 16:15:42.765856'),(5,'admin','0003_logentry_add_action_flag_choices','2025-10-31 16:15:42.775609'),(6,'apy','0001_initial','2025-10-31 16:15:45.489970'),(7,'contenttypes','0002_remove_content_type_name','2025-10-31 16:15:45.615700'),(8,'auth','0002_alter_permission_name_max_length','2025-10-31 16:15:45.686675'),(9,'auth','0003_alter_user_email_max_length','2025-10-31 16:15:45.710996'),(10,'auth','0004_alter_user_username_opts','2025-10-31 16:15:45.720460'),(11,'auth','0005_alter_user_last_login_null','2025-10-31 16:15:45.776080'),(12,'auth','0006_require_contenttypes_0002','2025-10-31 16:15:45.779069'),(13,'auth','0007_alter_validators_add_error_messages','2025-10-31 16:15:45.786026'),(14,'auth','0008_alter_user_username_max_length','2025-10-31 16:15:45.860479'),(15,'auth','0009_alter_user_last_name_max_length','2025-10-31 16:15:45.944675'),(16,'auth','0010_alter_group_name_max_length','2025-10-31 16:15:45.969529'),(17,'auth','0011_update_proxy_permissions','2025-10-31 16:15:45.986102'),(18,'auth','0012_alter_user_first_name_max_length','2025-10-31 16:15:46.059081'),(19,'sessions','0001_initial','2025-10-31 16:15:46.096638'),(20,'backup_module','0001_initial','2025-11-10 12:29:49.887132');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('70sq6fswjldlkhtq66uzb9m93gtjducr','.eJxVjDsOwyAQBe9CHSEw5rMp0_sMCJYlOIlAMnYV5e6xJRdJ-2bmvZkP21r81mnxc2JXJtnld4sBn1QPkB6h3hvHVtdljvxQ-Ek7n1qi1-10_w5K6GWvyahxAJOcMwKiJbAKtLMkkWwSMucUclQ6jwAo0GYBliINWu5SRh3Z5wvXkjgD:1vOaJ8:FQLgqrhyTmketPpQhmmNhMl8cSLgCxJmT6V_mTlMqGU','2025-12-11 11:37:06.097858'),('ybwbzvt3fcw2ou0xjjr0u2a5vwt00aao','.eJxVjDsOwyAQBe9CHSEw5rMp0_sMCJYlOIlAMnYV5e6xJRdJ-2bmvZkP21r81mnxc2JXJtnld4sBn1QPkB6h3hvHVtdljvxQ-Ek7n1qi1-10_w5K6GWvyahxAJOcMwKiJbAKtLMkkWwSMucUclQ6jwAo0GYBliINWu5SRh3Z5wvXkjgD:1vJZvH:zgav8Z9xqwTX8LW9WoVEqvSQp9JyLKlDM09fqbNu-mM','2025-11-27 16:11:47.528380');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-11-28 11:15:13
