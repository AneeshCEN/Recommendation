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
-- Table structure for table `rank_data`
--

DROP TABLE IF EXISTS `rank_data`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rank_data` (
  `car_type` varchar(50) DEFAULT NULL,
  `type` varchar(50) DEFAULT NULL,
  `Gender` varchar(50) DEFAULT NULL,
  `Age` varchar(50) DEFAULT NULL,
  `AgeRank` varchar(50) DEFAULT NULL,
  `GenderRank` varchar(50) DEFAULT NULL,
  `FamilyRank` varchar(50) DEFAULT NULL,
  `StudentRank` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rank_data`
--

LOCK TABLES `rank_data` WRITE;
/*!40000 ALTER TABLE `rank_data` DISABLE KEYS */;
INSERT INTO `rank_data` VALUES ('Soul','Wagon','','50','3','','','9\r'),('Flex','Wagon','','50','7','','','\r'),('Camaro','Coupe','','22','3','','','3\r'),('Mustang','Coupe','','22','4','','','4\r'),('Civic','Coupe','','22','1','','','1\r'),('Traverse','SUV','','','','','5','\r'),('RAV4','SUV','Female','22','8','3','','8\r'),('Sorento','SUV','','','','','6','\r'),('Equinox','SUV','','22','9','','','9\r'),('CR-V','SUV','Female','22','6','2','','6\r'),('Escape','SUV','','','7','','','7\r'),('Tucson','SUV','Female','','','1','','\r'),('Sienna','Mini-Van','','','','','4','\r'),('Taurus','Sedan','','50','4','','','\r'),('Avalon','Sedan','','50','5','','','\r'),('Accord','Sedan','','50','2','','3','\r'),('Impala','Sedan','','50','1','','','\r'),('Camry','Sedan','','50','6','','','\r'),('Optima Hybrid','Sedan','','22','5','','','5\r'),('Sonata','Sedan','','','','','2','\r'),('Prius c','Hatchback','','22','2','','','2\r'),('Fit','Hatchback','','','','','1','\r');
/*!40000 ALTER TABLE `rank_data` ENABLE KEYS */;
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
