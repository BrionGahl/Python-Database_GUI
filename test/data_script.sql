USE `brion_cs430`;
-- Host: localhost    Database: cs430
-- ------------------------------------------------------
-- Server version	8.0.26

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Dumping data for table `courses`
--

LOCK TABLES `courses` WRITE;
/*!40000 ALTER TABLE `courses` DISABLE KEYS */;
INSERT INTO `courses` VALUES ('500','Data Structures','Monday/Wednesday/Friday 09:00:00','ENGA404',200,15),('501','Theory of Programming Languages','Tuesday/Thursday 14:00:00','ENGA202',201,15),('502','Introduction to Biology','Monday/Wednesday/Friday 15:00:00','LAW171',202,65),('503','Plant Taxonomy','Monday/Wednesday/Friday 00:00:00','LSII418',203,20),('504a','Organic Chemistry','Monday/Wednesday/Friday 00:00:00','LSII202',204,15),('504b','Organic Chemistry','Monday/Wednesday/Friday 09:00:00','LSII202',204,15),('505','Introduction to Chemistry','Monday/Wednesday/Friday 14:00:00','LSII100',205,40),('506','Physics I','Tuesday/Thursday 08:00:00','NCK400',206,20),('507','Physics II','Monday/Wednesday/Friday 15:00:00','NCK410',207,20),('508a','Calculus I','Monday/Wednesday/Friday 14:00:00','NCK200',208,20),('508b','Calculus I','Monday/Wednesday/Friday 00:00:00','NCK200',208,20),('509','Calculus II','Monday/Wednesday/Friday 16:00:00','NCK300',209,20),('510','Analysis of Minerals','Tuesday/Thursday 09:00:00','LSI100',210,10),('511','Analysis of Minerals II','Tuesday/Thursday 15:00:00','LSI120',211,10),('512','Introduction to Business','Monday/Wednesday/Friday 10:00:00','REHN010',212,25),('513','Business Law','Tuesday/Thursday 00:00:00','REHN101',213,10),('514','United States History','Tuesday/Thursday 13:00:00','LAW181',214,60),('515','Latin American History','Monday/Wednesday/Friday 15:00:00','LAW191',215,60),('516','English I','Monday/Wednesday/Friday 00:00:00','WHAM100',216,15),('517','English II','Monday/Wednesday/Friday 00:00:00','WHAM201',217,15),('518','Introduction to Logic','Tuesday/Thursday 00:00:00','WHAM123',218,20),('519','European Philosophy','Monday/Wednesday/Friday 16:00:00','LAW171',219,30);
/*!40000 ALTER TABLE `courses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `department`
--

LOCK TABLES `department` WRITE;
/*!40000 ALTER TABLE `department` DISABLE KEYS */;
INSERT INTO `department` VALUES (400,'Computer Science'),(401,'Biology'),(402,'Chemistry'),(403,'Physics'),(404,'Mathematics'),(405,'Geology'),(406,'Business'),(407,'History'),(408,'English'),(409,'Philosophy');
/*!40000 ALTER TABLE `department` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `enrolled`
--

LOCK TABLES `enrolled` WRITE;
/*!40000 ALTER TABLE `enrolled` DISABLE KEYS */;
INSERT INTO `enrolled` VALUES (100,'500',NULL,NULL,NULL),(100,'502',NULL,NULL,NULL),(100,'508b',NULL,NULL,NULL),(100,'516',NULL,NULL,NULL),(101,'500',NULL,NULL,NULL),(101,'502',NULL,NULL,NULL),(101,'508b',NULL,NULL,NULL),(101,'513',NULL,NULL,NULL),(102,'502',NULL,NULL,NULL),(102,'503',NULL,NULL,NULL),(102,'508b',NULL,NULL,NULL),(102,'517',NULL,NULL,NULL),(103,'503',NULL,NULL,NULL),(103,'508a',NULL,NULL,NULL),(103,'508b',NULL,NULL,NULL),(103,'513',NULL,NULL,NULL),(103,'518',NULL,NULL,NULL),(104,'504b',NULL,NULL,NULL),(104,'507',NULL,NULL,NULL),(104,'509',NULL,NULL,NULL),(104,'513',NULL,NULL,NULL),(105,'509',NULL,NULL,NULL),(105,'511',NULL,NULL,NULL),(105,'513',NULL,NULL,NULL),(105,'517',NULL,NULL,NULL),(106,'507',NULL,NULL,NULL),(106,'508a',NULL,NULL,NULL),(106,'512',NULL,NULL,NULL),(106,'513',NULL,NULL,NULL),(107,'504a',NULL,NULL,NULL),(107,'508b',NULL,NULL,NULL),(107,'513',NULL,NULL,NULL),(107,'515',NULL,NULL,NULL),(107,'517',NULL,NULL,NULL),(108,'506',NULL,NULL,NULL),(108,'513',NULL,NULL,NULL),(108,'516',NULL,NULL,NULL),(109,'508b',NULL,NULL,NULL),(109,'511',NULL,NULL,NULL),(109,'513',NULL,NULL,NULL),(110,'513',NULL,NULL,NULL),(111,'513',NULL,NULL,NULL);
/*!40000 ALTER TABLE `enrolled` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `faculty`
--

LOCK TABLES `faculty` WRITE;
/*!40000 ALTER TABLE `faculty` DISABLE KEYS */;
INSERT INTO `faculty` VALUES (200,'Renaldo Buss',400),(201,'Donald Pye',400),(202,'James Cox',401),(203,'Caroline Aguirre',401),(204,'Joseph Banks',402),(205,'Jeffrey Lewis',402),(206,'Wilbert Moreno',403),(207,'Jason Bradley',403),(208,'Robert Coster',404),(209,'Rosie Bower',404),(210,'Laura Cantrell',405),(211,'Katherine Siegel',405),(212,'Shiela Cushing',406),(213,'Mark Bridges',406),(214,'Janeen Koopman',407),(215,'Brad Richards',407),(216,'Robin Alexander',408),(217,'Thelma Laroche',408),(218,'Stephen Doty',409),(219,'Jasmine Harrison',409);
/*!40000 ALTER TABLE `faculty` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `staff`
--

LOCK TABLES `staff` WRITE;
/*!40000 ALTER TABLE `staff` DISABLE KEYS */;
INSERT INTO `staff` VALUES (300,'Alice Penny',400),(301,'George Richards',400),(302,'Deborah Jones',401),(303,'Kenneth Pettie',401),(304,'Dorothy Williams',402),(305,'Rosa Ashby',402),(306,'Gregory Avila',403),(307,'Darren Nguyen',403),(308,'Joanna Kulas',404),(309,'Oleta Duca',404),(310,'Frank Wright',405),(311,'Alice Hammon',405),(312,'James Lemaster',406),(313,'James Boyett',406),(314,'Sandra Roberts',407),(315,'Pat Figueroa',407),(316,'Maurice Harvell',408),(317,'Tanya Kelley',408),(318,'Annie Goodwin',409),(319,'Max Baltz',409);
/*!40000 ALTER TABLE `staff` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `student`
--

LOCK TABLES `student` WRITE;
/*!40000 ALTER TABLE `student` DISABLE KEYS */;
INSERT INTO `student` VALUES (100,'Darlene Vang','Computer Science','Freshman',18),(101,'David Burch','Biology','Sophomore',19),(102,'Vanessa Cobble','Chemistry','Junior',20),(103,'Laura Polizzi','Physics','Senior',21),(104,'Jesse Engles','Mathematics','Master',26),(105,'Joseph Moses','Geology','PhD',29),(106,'Joy StClair','Business','Freshman',23),(107,'Terri Gardiner','History','Sophomore',25),(108,'Calvin Joyner','English','Junior',24),(109,'Paul Williams','Philosophy','Senior',32),(110,'Alma Gardner','Computer Science','Senior',22),(111,'Sara Cruz','Biology','Junior',21),(112,'Ed Holbrook','Chemistry','PhD',27),(113,'Carla Stone','Physics','Freshman',22),(114,'Vera Rhee','Mathematics','Freshman',21),(115,'William Samuels','Geology','Sophomore',23),(116,'Alex Simon','Business','Senior',23),(117,'Charles Brewer','History','Sophomore',24),(118,'Kate Lino','English','Master',26),(119,'Helen Foster','Philosophy','Senior',32);
/*!40000 ALTER TABLE `student` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
