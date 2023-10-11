-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Oct 06, 2023 at 04:46 PM
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
-- Table structure for table `catalogue`
--

DROP TABLE IF EXISTS `catalogue`;
CREATE TABLE IF NOT EXISTS `catalogue` (
  `id_buku` int(11) NOT NULL AUTO_INCREMENT,
  `nama_buku` text NOT NULL,
  `deskripsi_buku` longtext NOT NULL,
  `tanggal_masuk` date NOT NULL,
  `tanggal_terbit` date NOT NULL,
  `author` text NOT NULL,
  `genre` text NOT NULL,
  `status` text NOT NULL,
  PRIMARY KEY (`id_buku`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `catalogue`
--

INSERT INTO `catalogue` (`id_buku`, `nama_buku`, `deskripsi_buku`, `tanggal_masuk`, `tanggal_terbit`, `author`, `genre`, `status`) VALUES
(1, 'Stanley', 'A struggle against Autism', '2023-10-01', '2022-01-15', 'Habel', 'Biography', 'unavailable'),
(2, '100 cara menjadi Ryan Gosling', 'bagaimana cara menjadi pria pujangga idola semua pria', '2023-10-01', '2022-01-15', 'Kenji Yamamoto', 'Pyschology', 'available');

-- --------------------------------------------------------

--
-- Table structure for table `peminjaman_done`
--

DROP TABLE IF EXISTS `peminjaman_done`;
CREATE TABLE IF NOT EXISTS `peminjaman_done` (
  `id_peminjaman` int(11) NOT NULL AUTO_INCREMENT,
  `id_buku` int(11) DEFAULT NULL,
  `nim_peminjam` int(11) DEFAULT NULL,
  `tanggal_peminjaman` date DEFAULT NULL,
  `tanggal_pengembalian` date DEFAULT NULL,
  PRIMARY KEY (`id_peminjaman`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `peminjaman_done`
--

INSERT INTO `peminjaman_done` (`id_peminjaman`, `id_buku`, `nim_peminjam`, `tanggal_peminjaman`, `tanggal_pengembalian`) VALUES
(1, 2, 1, '2023-10-06', '2023-10-06'),
(2, 2, 103, '2023-10-06', '2023-10-06');

-- --------------------------------------------------------

--
-- Table structure for table `peminjaman_ongoing`
--

DROP TABLE IF EXISTS `peminjaman_ongoing`;
CREATE TABLE IF NOT EXISTS `peminjaman_ongoing` (
  `id_peminjaman` int(11) NOT NULL AUTO_INCREMENT,
  `id_buku` int(11) NOT NULL,
  `nim_peminjam` varchar(10) NOT NULL,
  `tanggal_peminjaman` date NOT NULL,
  `waktu_peminjaman` time NOT NULL,
  PRIMARY KEY (`id_peminjaman`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `peminjaman_ongoing`
--

INSERT INTO `peminjaman_ongoing` (`id_peminjaman`, `id_buku`, `nim_peminjam`, `tanggal_peminjaman`, `waktu_peminjaman`) VALUES
(3, 1, '103', '2023-10-06', '23:38:01');

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
) ENGINE=MyISAM AUTO_INCREMENT=17 DEFAULT CHARSET=latin1;

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
(12, 1, '2023-10-12', '13:00:00', '14:00:00', 'Ruangan A'),
(13, 1, '2023-10-15', '21:00:00', '21:00:00', 'Ruangan A'),
(14, 1, '2023-10-16', '21:00:00', '22:00:00', 'Ruangan A'),
(15, 1, '2023-10-16', '07:30:00', '08:30:00', 'Ruangan A'),
(16, 1, '2023-10-16', '10:00:00', '12:00:00', 'Ruangan A');

-- --------------------------------------------------------

--
-- Table structure for table `students`
--

DROP TABLE IF EXISTS `students`;
CREATE TABLE IF NOT EXISTS `students` (
  `nim` varchar(10) NOT NULL,
  `full_name` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `fine` decimal(10,2) NOT NULL DEFAULT '0.00',
  PRIMARY KEY (`nim`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `students`
--

INSERT INTO `students` (`nim`, `full_name`, `password`, `fine`) VALUES
('2', 'Justin Ambatukam', '123', '5000.00'),
('103', 'Justin Habel Kiswanto', 'ehey', '0.00');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
