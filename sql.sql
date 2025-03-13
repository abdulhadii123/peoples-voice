/*
SQLyog Community Edition- MySQL GUI v8.03 
MySQL - 5.5.5-10.4.10-MariaDB : Database - peoples_voice
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

CREATE DATABASE /*!32312 IF NOT EXISTS*/`peoples_voice` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `peoples_voice`;

/*Table structure for table `cctv` */

DROP TABLE IF EXISTS `cctv`;

CREATE TABLE `cctv` (
  `cctv_id` int(20) NOT NULL AUTO_INCREMENT,
  `camera_no` int(11) DEFAULT NULL,
  `pin_no` int(11) DEFAULT NULL,
  `location` varchar(30) DEFAULT NULL,
  `longitude` varchar(200) DEFAULT NULL,
  `latitude` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`cctv_id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*Data for the table `cctv` */

insert  into `cctv`(`cctv_id`,`camera_no`,`pin_no`,`location`,`longitude`,`latitude`) values (1,234,24,'kayalode','59.17730','11.74498');

/*Table structure for table `complaint` */

DROP TABLE IF EXISTS `complaint`;

CREATE TABLE `complaint` (
  `complaint_id` int(11) NOT NULL AUTO_INCREMENT,
  `complaint` varchar(30) DEFAULT NULL,
  `complaint_date` varchar(50) DEFAULT NULL,
  `reply` varchar(30) DEFAULT NULL,
  `reply_date` varchar(50) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`complaint_id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `complaint` */

/*Table structure for table `control_room_vehicle` */

DROP TABLE IF EXISTS `control_room_vehicle`;

CREATE TABLE `control_room_vehicle` (
  `vehicle_id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(50) DEFAULT NULL,
  `vehicle_no` int(11) DEFAULT NULL,
  `location` varchar(20) DEFAULT NULL,
  `phone` bigint(11) DEFAULT NULL,
  `police_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`vehicle_id`)
) ENGINE=MyISAM AUTO_INCREMENT=12 DEFAULT CHARSET=latin1;

/*Data for the table `control_room_vehicle` */

insert  into `control_room_vehicle`(`vehicle_id`,`email`,`vehicle_no`,`location`,`phone`,`police_id`) values (9,'kv9496598@gmail.com',78,'thalasherry',9876342510,2),(11,'fidhafathimapk2@gmail.com',987,'kannur',9895674321,3);

/*Table structure for table `crime_category` */

DROP TABLE IF EXISTS `crime_category`;

CREATE TABLE `crime_category` (
  `category_id` int(11) NOT NULL AUTO_INCREMENT,
  `crime_type` varchar(30) DEFAULT NULL,
  `description` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`category_id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

/*Data for the table `crime_category` */

insert  into `crime_category`(`category_id`,`crime_type`,`description`) values (1,'murder','Murder means when one person is killed by another person or a group of persons who have a pre-determined intention to end life of the former'),(3,'blackmail','rrrrrrrrrrrrrrrrrrrrrrrrrre');

/*Table structure for table `crime_record` */

DROP TABLE IF EXISTS `crime_record`;

CREATE TABLE `crime_record` (
  `record_id` int(11) NOT NULL AUTO_INCREMENT,
  `criminal_id` int(11) DEFAULT NULL,
  `records` varchar(50) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `category_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`record_id`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

/*Data for the table `crime_record` */

insert  into `crime_record`(`record_id`,`criminal_id`,`records`,`date`,`category_id`) values (1,1,'/static/pic/230115-160515.pdf','2023-01-15',1),(2,2,'/static/pic/230115-203943.pdf','2023-01-15',3),(3,2,'/static/pic/230115-204136.pdf','2023-01-15',1),(5,2,'/static/pic/230118-121609.pdf','2023-01-18',1);

/*Table structure for table `criminal` */

DROP TABLE IF EXISTS `criminal`;

CREATE TABLE `criminal` (
  `criminal_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(20) DEFAULT NULL,
  `dob` date DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `place` varchar(30) DEFAULT NULL,
  `post` varchar(20) DEFAULT NULL,
  `pin` int(11) DEFAULT NULL,
  `district` varchar(20) DEFAULT NULL,
  `image` varchar(100) DEFAULT NULL,
  `phone_no` varchar(11) DEFAULT NULL,
  `police_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`criminal_id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

/*Data for the table `criminal` */

insert  into `criminal`(`criminal_id`,`name`,`dob`,`gender`,`place`,`post`,`pin`,`district`,`image`,`phone_no`,`police_id`) values (1,'fidha','2002-06-30','FEMALE','kannur','talipparamb',672345,'Kannur','/static/pic/230115-124737.jpg','9887766554',2),(2,'fathima','2010-10-22','MALE','thalashery','talipparamb',567098,'Kannur','/static/pic/230115-203814.jpg','9887766554',3),(3,'hadi','2002-07-06','MALE','puthiyatheru','kannur',567095,'Kannur','/static/pic/230118-102644.jpg','9876543214',3);

/*Table structure for table `criminal_alert` */

DROP TABLE IF EXISTS `criminal_alert`;

CREATE TABLE `criminal_alert` (
  `criminal_alert_id` int(11) NOT NULL AUTO_INCREMENT,
  `criminal_id` int(11) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `time` varchar(20) DEFAULT NULL,
  `latitude` varchar(20) DEFAULT NULL,
  `longitude` varchar(20) DEFAULT NULL,
  `type` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`criminal_alert_id`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

/*Data for the table `criminal_alert` */

insert  into `criminal_alert`(`criminal_alert_id`,`criminal_id`,`date`,`user_id`,`time`,`latitude`,`longitude`,`type`) values (1,1,'2023-01-15',7,'15:14:02','11.8684329','75.3632153','user'),(3,2,'2023-01-18',1,'10:03:20','11.74498','59.17730','cctv'),(4,3,'2023-01-18',1,'10:26:40','11.74498','59.17730','cctv');

/*Table structure for table `emergency_alert` */

DROP TABLE IF EXISTS `emergency_alert`;

CREATE TABLE `emergency_alert` (
  `emergency_alert_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `date` varchar(200) DEFAULT NULL,
  `time` varchar(200) DEFAULT NULL,
  `latitude` varchar(20) DEFAULT NULL,
  `longitude` varchar(20) DEFAULT NULL,
  `status` varchar(40) DEFAULT NULL,
  PRIMARY KEY (`emergency_alert_id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `emergency_alert` */

insert  into `emergency_alert`(`emergency_alert_id`,`user_id`,`date`,`time`,`latitude`,`longitude`,`status`) values (1,7,'2023-01-15','14:46:55','11.8684337','75.3632148','jh');

/*Table structure for table `emergency_contact` */

DROP TABLE IF EXISTS `emergency_contact`;

CREATE TABLE `emergency_contact` (
  `em_id` int(11) NOT NULL AUTO_INCREMENT,
  `dept` varchar(20) DEFAULT NULL,
  `contact` bigint(11) DEFAULT NULL,
  PRIMARY KEY (`em_id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*Data for the table `emergency_contact` */

insert  into `emergency_contact`(`em_id`,`dept`,`contact`) values (1,'emergency',7667656565),(2,'flood',9894309876);

/*Table structure for table `feedback` */

DROP TABLE IF EXISTS `feedback`;

CREATE TABLE `feedback` (
  `feedback_id` int(11) NOT NULL AUTO_INCREMENT,
  `feedback` varchar(50) DEFAULT NULL,
  `date` varchar(50) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`feedback_id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Data for the table `feedback` */

insert  into `feedback`(`feedback_id`,`feedback`,`date`,`user_id`) values (1,'okkk','2023-01-15',7);

/*Table structure for table `login` */

DROP TABLE IF EXISTS `login`;

CREATE TABLE `login` (
  `LOGIN_ID` int(11) NOT NULL AUTO_INCREMENT,
  `USERNAME` varchar(30) DEFAULT NULL,
  `PASSWORD` varchar(10) DEFAULT NULL,
  `USERTYPE` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`LOGIN_ID`)
) ENGINE=MyISAM AUTO_INCREMENT=12 DEFAULT CHARSET=latin1;

/*Data for the table `login` */

insert  into `login`(`LOGIN_ID`,`USERNAME`,`PASSWORD`,`USERTYPE`) values (1,'admin','123','admin'),(11,'fidhafathimapk2@gmail.com','7658','control room'),(3,'krishnenduv6@gmail.com','8072','police'),(7,'s@gmail.com','ss','user'),(9,'fidhafathima098756@gmail.com','2530','control room'),(10,'kv9496598@gmail.com','7492','control room');

/*Table structure for table `missing_person` */

DROP TABLE IF EXISTS `missing_person`;

CREATE TABLE `missing_person` (
  `missing_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) DEFAULT NULL,
  `age` int(11) DEFAULT NULL,
  `gender` varchar(10) DEFAULT NULL,
  `place` varchar(30) DEFAULT NULL,
  `missing_date` date DEFAULT NULL,
  `contact_number` bigint(20) DEFAULT NULL,
  `image` varchar(100) DEFAULT NULL,
  `height` int(11) DEFAULT NULL,
  `weight` int(11) DEFAULT NULL,
  `police_id` int(11) DEFAULT NULL,
  `known_language` varchar(20) DEFAULT NULL,
  `disability` varchar(30) DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`missing_id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

/*Data for the table `missing_person` */

insert  into `missing_person`(`missing_id`,`name`,`age`,`gender`,`place`,`missing_date`,`contact_number`,`image`,`height`,`weight`,`police_id`,`known_language`,`disability`,`status`) values (1,'geethika',20,'FEMALE','chovva','2022-01-15',9876543210,'/static/pic/230115-125328.jpg',154,45,3,'eng','no','found'),(2,'krish',23,'FEMALE','kannur','2022-12-28',9895188520,'/static/pic/230115-130543.jpg',165,56,3,'eng','no','pending'),(3,'fidha',15,'FEMALE','anjarajandy','2006-06-09',9895188520,'/static/pic/230115-210821.jpg',123,45,3,'kjh','no','pending');

/*Table structure for table `missing_person_alert` */

DROP TABLE IF EXISTS `missing_person_alert`;

CREATE TABLE `missing_person_alert` (
  `alert_id` int(11) NOT NULL AUTO_INCREMENT,
  `missing_id` int(11) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `time` varchar(20) DEFAULT NULL,
  `latitude` varchar(20) DEFAULT NULL,
  `longitude` varchar(20) DEFAULT NULL,
  `type` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`alert_id`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

/*Data for the table `missing_person_alert` */

insert  into `missing_person_alert`(`alert_id`,`missing_id`,`date`,`user_id`,`time`,`latitude`,`longitude`,`type`) values (1,1,'2023-01-15',7,'15:00:45','11.8684334','75.3632152','user'),(2,2,'2023-01-18',7,'11:22:35','','','user'),(3,3,'2023-01-18',1,'09:36:16','11.74498','59.17730','cctv'),(4,2,'2023-01-18',1,'11:22:35','11.74498','59.17730','cctv');

/*Table structure for table `most_wanted_criminal` */

DROP TABLE IF EXISTS `most_wanted_criminal`;

CREATE TABLE `most_wanted_criminal` (
  `most_id` int(11) NOT NULL AUTO_INCREMENT,
  `criminal_id` int(11) DEFAULT NULL,
  `status` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`most_id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

/*Data for the table `most_wanted_criminal` */

insert  into `most_wanted_criminal`(`most_id`,`criminal_id`,`status`) values (1,1,'MOST WANTED'),(2,2,'pending'),(3,3,'pending');

/*Table structure for table `police` */

DROP TABLE IF EXISTS `police`;

CREATE TABLE `police` (
  `police_id` int(11) NOT NULL AUTO_INCREMENT,
  `location_name` varchar(30) DEFAULT NULL,
  `place` varchar(40) DEFAULT NULL,
  `phone` bigint(20) DEFAULT NULL,
  `email_id` varchar(30) DEFAULT NULL,
  `station_no` int(11) DEFAULT NULL,
  `latitude` varchar(200) DEFAULT NULL,
  `longitude` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`police_id`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

/*Data for the table `police` */

insert  into `police`(`police_id`,`location_name`,`place`,`phone`,`email_id`,`station_no`,`latitude`,`longitude`) values (3,'thavakkara','kannur',6745321099,'krishnenduv6@gmail.com',9,'11.79876     ','75.53834');

/*Table structure for table `track_vehicle` */

DROP TABLE IF EXISTS `track_vehicle`;

CREATE TABLE `track_vehicle` (
  `track_id` int(11) NOT NULL AUTO_INCREMENT,
  `vehicle_id` int(11) DEFAULT NULL,
  `location_name` varchar(30) DEFAULT NULL,
  `latitude` varchar(20) DEFAULT NULL,
  `longitude` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`track_id`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

/*Data for the table `track_vehicle` */

insert  into `track_vehicle`(`track_id`,`vehicle_id`,`location_name`,`latitude`,`longitude`) values (1,11,NULL,NULL,NULL),(2,NULL,NULL,NULL,NULL),(3,9,'Kannur','11.8684373','75.363203'),(4,7,'Kannur','11.8684337','75.3632151'),(5,7,'Kannur','11.8684337','75.3632151');

/*Table structure for table `user` */

DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(20) DEFAULT NULL,
  `gender` varchar(200) DEFAULT NULL,
  `place` varchar(30) DEFAULT NULL,
  `pin` int(11) DEFAULT NULL,
  `district` varchar(20) DEFAULT NULL,
  `phone_number` bigint(11) DEFAULT NULL,
  `email` varchar(30) DEFAULT NULL,
  `aadhar_no` bigint(11) DEFAULT NULL,
  `image` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;

/*Data for the table `user` */

insert  into `user`(`user_id`,`name`,`gender`,`place`,`pin`,`district`,`phone_number`,`email`,`aadhar_no`,`image`) values (7,'sree','Female','ghh',963854,'Kannur',7352968014,'s@gmail.com',458036927415,'/static/pic/230115-135233.jpg');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
