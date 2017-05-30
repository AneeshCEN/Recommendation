-- MySQL dump 10.13  Distrib 5.6.23, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: gogo_car
-- ------------------------------------------------------
-- Server version	5.5.44-log

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
-- Table structure for table `location`
--

DROP TABLE IF EXISTS `location`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `location` (
  `make` varchar(50) DEFAULT NULL,
  `model` varchar(50) DEFAULT NULL,
  `state` varchar(50) DEFAULT NULL,
  `stateid` int(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `location`
--

LOCK TABLES `location` WRITE;
/*!40000 ALTER TABLE `location` DISABLE KEYS */;
INSERT INTO `location` VALUES ('Toyota','Camry','Alabama',1),('Ram','Pickup','Alaska',2),('Ram','Pickup','Arizona',3),('Ford','F-150','Arkansas',4),('Honda','Accord','California',5),('Toyota','Camry','Carolinas',6),('Subaru','Outback','Colorado',7),('Toyota','Corolla','Florida',8),('Toyota','Camry','Florida',8),('Toyota','Camry','Georgia',9),('Ford','F-150','Idaho',10),('Chevrolet','Silverado','Illinois',11),('Chevrolet','Silverado','Indiana',12),('Chevrolet','Silverado','Iowa',13),('Ford','F-150','Kansas',14),('Chevrolet','Silverado','Kentucky',15),('Ford','F-150','Louisiana',16),('Subaru','Outback','Maine',17),('Chevrolet','Silverado','Michigan',18),('Chevrolet','Silverado','Midwest',19),('Chevrolet','Silverado','Minnesota',20),('Ford','F-150','Mississippi',21),('Ram','Pickup','Montana',22),('Ford','F-150','Missouri,',23),('Ram','Pickup','Nevada',24),('Ford','F-150','Nebraska',25),('Honda','CR-V','Newyork',26),('Ford','F-150','New Mexico',27),('Chevrolet','Silverado','Ohio',28),('Ford','F-150','North Dakota',29),('Ford','F-150','Oklahoma',30),('Honda','CR-V','Rhode Island',31),('Ram','Pickup','Oregon',31),('Ford','F-150','Pennsylvania',32),('Ford','F-150','South Dakota',33),('Ford','F-150','Tennessee',34),('Subaru','Forester','United sates',35),('Ford','F-150','Texas',36),('GMC','SIERRA','Vermont',37),('Ford','F-150','Utah',38),('Subaru','Outback','Washington',39),('Chevrolet','Silverado','West Virginia',40),('Ford','F-150','Wyoming',41);
/*!40000 ALTER TABLE `location` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-08-01 10:37:16
