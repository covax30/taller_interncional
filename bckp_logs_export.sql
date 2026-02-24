-- MariaDB dump 10.19  Distrib 10.4.32-MariaDB, for Win64 (AMD64)
--
-- Host: localhost    Database: bckp_logs
-- ------------------------------------------------------
-- Server version	8.0.44

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

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
  `mensaje_error` longtext,
  `usuario_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `backup_module_backuplog_usuario_id_81022408` (`usuario_id`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `backup_module_backuplog`
--

LOCK TABLES `backup_module_backuplog` WRITE;
/*!40000 ALTER TABLE `backup_module_backuplog` DISABLE KEYS */;
INSERT INTO `backup_module_backuplog` VALUES (3,'2025-12-11 12:32:44.501930','2025-12-11 12:32:44.815152','Manual','Éxito',0.1,'D:\\Users\\User\\Desktop\\taller_interncional\\db_backups\\taller_internacional_backup_20251211_073244.sql',NULL,1),(4,'2025-12-11 12:32:46.474890','2025-12-11 12:32:46.770855','Manual','Éxito',0.1,'D:\\Users\\User\\Desktop\\taller_interncional\\db_backups\\taller_internacional_backup_20251211_073246.sql',NULL,1),(5,'2025-12-11 12:32:48.474390','2025-12-11 12:32:48.762283','Manual','Éxito',0.1,'D:\\Users\\User\\Desktop\\taller_interncional\\db_backups\\taller_internacional_backup_20251211_073248.sql',NULL,1),(6,'2025-12-11 12:35:27.317915','2025-12-11 12:35:30.977282','Manual','Éxito',0.1,'D:\\Users\\User\\Desktop\\taller_interncional\\db_backups\\taller_internacional_backup_20251211_073250.sql',NULL,1),(7,'2025-12-11 12:35:01.255907','2025-12-11 12:35:01.588667','Manual','Éxito',0.1,'D:\\Users\\User\\Desktop\\taller_interncional\\db_backups\\taller_internacional_backup_20251211_073501.sql',NULL,1),(8,'2025-12-11 12:35:03.983035','2025-12-11 12:35:04.284597','Manual','Éxito',0.1,'D:\\Users\\User\\Desktop\\taller_interncional\\db_backups\\taller_internacional_backup_20251211_073503.sql',NULL,1),(9,'2025-12-11 12:35:06.761116','2025-12-11 12:35:07.063035','Manual','Éxito',0.1,'D:\\Users\\User\\Desktop\\taller_interncional\\db_backups\\taller_internacional_backup_20251211_073506.sql',NULL,1),(10,'2025-12-11 12:35:08.692604','2025-12-11 12:35:08.950944','Manual','Éxito',0.1,'D:\\Users\\User\\Desktop\\taller_interncional\\db_backups\\taller_internacional_backup_20251211_073508.sql',NULL,1),(11,'2025-12-11 12:35:11.062101','2025-12-11 12:35:11.312650','Manual','Éxito',0.1,'D:\\Users\\User\\Desktop\\taller_interncional\\db_backups\\taller_internacional_backup_20251211_073511.sql',NULL,1),(12,'2025-12-11 12:36:38.577589','2025-12-11 12:36:41.887846','Manual','Éxito',0.1,'D:\\Users\\User\\Desktop\\taller_interncional\\db_backups\\taller_internacional_backup_20251211_073513.sql',NULL,1),(13,'2025-12-11 12:36:16.035562','2025-12-11 12:36:16.332759','Manual','Éxito',0.1,'D:\\Users\\User\\Desktop\\taller_interncional\\db_backups\\taller_internacional_backup_20251211_073616.sql',NULL,1),(14,'2025-12-11 16:41:34.189025','2025-12-11 16:41:37.286385','Manual','Éxito',0.1,'D:\\Users\\User\\Desktop\\taller_interncional\\db_backups\\taller_internacional_backup_20251211_073617.sql',NULL,1),(15,'2025-12-11 12:36:19.668983','2025-12-11 12:36:19.921734','Manual','Éxito',0.1,'D:\\Users\\User\\Desktop\\taller_interncional\\db_backups\\taller_internacional_backup_20251211_073619.sql',NULL,1),(16,'2025-12-11 12:36:21.531661','2025-12-11 12:36:21.789712','Manual','Éxito',0.1,'D:\\Users\\User\\Desktop\\taller_interncional\\db_backups\\taller_internacional_backup_20251211_073621.sql',NULL,1),(17,'2025-12-11 12:36:23.513993','2025-12-11 12:36:23.791646','Manual','Éxito',0.1,'D:\\Users\\User\\Desktop\\taller_interncional\\db_backups\\taller_internacional_backup_20251211_073623.sql',NULL,1),(18,'2025-12-11 12:58:16.655567','2025-12-11 12:58:16.981843','Manual','Éxito',0.1,'D:\\Users\\User\\Desktop\\taller_interncional\\db_backups\\taller_internacional_backup_20251211_075816.sql',NULL,1),(19,'2025-12-11 16:39:39.691905','2025-12-11 16:39:40.313199','Manual','Éxito',0.1,'D:\\Users\\User\\Desktop\\taller_interncional\\db_backups\\taller_internacional_backup_20251211_113939.sql',NULL,1),(20,'2025-12-11 16:47:34.979070','2025-12-11 16:47:37.501455','Manual','Éxito',0.1,'D:\\Users\\User\\Desktop\\taller_interncional\\db_backups\\taller_internacional_backup_20251211_114716.sql',NULL,1),(21,'2025-12-11 16:47:45.292345','2025-12-11 16:47:45.281440','Externo','Éxito',0.10146522521972656,'D:\\Users\\User\\Desktop\\taller_interncional\\db_backups\\EXTERNAL_taller_internacional_backup_20251211_114716_8e1d7f.sql',NULL,1),(22,'2025-12-12 16:00:25.539722','2025-12-12 16:00:28.960988','Manual','Éxito',0.1,'D:\\Users\\User\\Desktop\\taller_interncional\\db_backups\\taller_internacional_backup_20251212_110015.sql',NULL,1),(23,'2025-12-15 12:11:33.634517','2025-12-15 12:11:34.407723','Manual','Éxito',0.1,'D:\\Users\\User\\Desktop\\taller_interncional\\db_backups\\taller_internacional_backup_20251215_071133.sql',NULL,1),(24,'2025-12-15 12:11:37.259168','2025-12-15 12:11:37.520737','Manual','Éxito',0.1,'D:\\Users\\User\\Desktop\\taller_interncional\\db_backups\\taller_internacional_backup_20251215_071137.sql',NULL,1),(25,'2025-12-15 12:11:40.155524','2025-12-15 12:11:40.437028','Manual','Éxito',0.1,'D:\\Users\\User\\Desktop\\taller_interncional\\db_backups\\taller_internacional_backup_20251215_071140.sql',NULL,1),(27,'2025-12-15 15:21:15.480238','2025-12-15 15:21:18.742114','Manual','Éxito',0.1,'D:\\Users\\User\\Desktop\\taller_interncional\\db_backups\\taller_internacional_backup_20251215_071144.sql',NULL,1),(30,'2026-02-03 15:07:43.774647','2026-02-03 15:07:47.389566','Manual','Éxito',0.1,'D:\\Users\\User\\Desktop\\taller_interncional\\db_backups\\taller_internacional_backup_20251216_070337.sql',NULL,1),(31,'2026-02-03 15:13:44.790656','2026-02-03 15:13:48.344313','Externo','Éxito',0.1015625,'D:\\Users\\User\\Desktop\\taller_interncional\\db_backups\\EXTERNAL_taller_internacional_backup_20251216_070337 (1)_223284.sql',NULL,1),(32,'2026-02-04 11:40:19.715582','2026-02-04 11:40:23.438820','Manual','Éxito',0.1,'D:\\Users\\User\\Desktop\\taller_interncional\\db_backups\\taller_internacional_backup_20260204_063810.sql',NULL,1);
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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `backup_module_configuracionrespaldo`
--

LOCK TABLES `backup_module_configuracionrespaldo` WRITE;
/*!40000 ALTER TABLE `backup_module_configuracionrespaldo` DISABLE KEYS */;
INSERT INTO `backup_module_configuracionrespaldo` VALUES (1,'semanal','03:00:00.000000');
/*!40000 ALTER TABLE `backup_module_configuracionrespaldo` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-12-11 12:26:19.885843'),(2,'auth','0001_initial','2025-12-11 12:26:19.905602'),(3,'backup_module','0001_initial','2025-12-11 12:26:20.015046');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-02-04  7:25:50
