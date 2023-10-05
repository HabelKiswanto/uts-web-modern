-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Oct 05, 2023 at 01:34 PM
-- Server version: 5.7.36
-- PHP Version: 7.4.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `perpus calvin`
--

-- --------------------------------------------------------

--
-- Table structure for table `room_bookings`
--

DROP TABLE IF EXISTS `room_bookings`;
CREATE TABLE IF NOT EXISTS `room_bookings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `student_id` int(11) DEFAULT NULL,
  `booking_date` date DEFAULT NULL,
  `booking_time` time DEFAULT NULL,
  `end_time` time DEFAULT NULL,
  `room_name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `student_id` (`student_id`)
) ENGINE=MyISAM AUTO_INCREMENT=13 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `room_bookings`
--

INSERT INTO `room_bookings` (`id`, `student_id`, `booking_date`, `booking_time`, `end_time`, `room_name`) VALUES
(1, 1, '2023-10-05', '10:00:00', '00:00:00', 'Ruangan A'),
(2, 1, '2023-10-05', '11:00:00', '12:00:00', 'Ruangan A'),
(3, 1, '2023-10-06', '11:00:00', '12:00:00', 'Ruangan A'),
(4, 1, '2023-10-07', '11:00:00', '14:00:00', 'Ruangan A'),
(5, 1, '2023-10-08', '11:00:00', '16:00:00', 'Ruangan A'),
(6, 1, '2023-10-07', '12:00:00', '13:00:00', 'Ruangan A'),
(7, 1, '2023-10-10', '15:00:00', '17:00:00', 'Ruangan A'),
(8, 1, '2023-10-10', '16:00:00', '18:00:00', 'Ruangan A'),
(9, 1, '2023-10-11', '19:00:00', '21:00:00', 'Ruangan A'),
(10, 1, '2023-10-11', '20:00:00', '21:00:00', 'Ruangan A'),
(11, 1, '2023-10-12', '12:00:00', '14:00:00', 'Ruangan A'),
(12, 1, '2023-10-12', '13:00:00', '14:00:00', 'Ruangan A');

-- --------------------------------------------------------

--
-- Table structure for table `students`
--

DROP TABLE IF EXISTS `students`;
CREATE TABLE IF NOT EXISTS `students` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `full_name` varchar(255) NOT NULL,
  `nim` varchar(10) NOT NULL,
  `password` varchar(255) NOT NULL,
  `fine` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `students`
--

INSERT INTO `students` (`id`, `full_name`, `nim`, `password`, `fine`) VALUES
(2, 'Justin Ambatukam', '2', '123', '5000.00');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
