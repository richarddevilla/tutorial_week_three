CREATE DATABASE `profile`;
USE `profile`;
CREATE TABLE `profile` (
      `id` int(11) AUTO_INCREMENT,
      `birth_date` date,
      `first_name` varchar(30),
      `last_name` varchar(30),
      `phone_number1` varchar(30),
      `phone_number2` varchar(30),
      `address_id` int(11) REFERENCES `address`(`id`),
      PRIMARY KEY (`id`)
    );
CREATE TABLE `address` (
      `id`    int(11)  AUTO_INCREMENT,
      `line1` varchar(100) DEFAULT '',
      `street` varchar(100) DEFAULT '',
      `suburb` varchar(100)  DEFAULT '',
      `postcode` varchar(100) DEFAULT '',
      `state` varchar(100) DEFAULT '',
      `country` varchar(100) DEFAULT 'Australia',
      PRIMARY KEY (`id`)
    );