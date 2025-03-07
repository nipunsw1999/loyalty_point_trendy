-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 07, 2025 at 12:48 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `trendy`
--

-- --------------------------------------------------------

--
-- Table structure for table `bills`
--

CREATE TABLE `bills` (
  `bid` int(255) NOT NULL,
  `Date` date NOT NULL,
  `Name` varchar(255) NOT NULL,
  `Mobile` varchar(255) NOT NULL,
  `Total` varchar(222) NOT NULL,
  `Services` varchar(1024) NOT NULL,
  `Prices` varchar(1024) NOT NULL,
  `Points` varchar(1014) NOT NULL,
  `Discount` varchar(8) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `bills`
--

INSERT INTO `bills` (`bid`, `Date`, `Name`, `Mobile`, `Total`, `Services`, `Prices`, `Points`, `Discount`) VALUES
(15, '2025-02-28', 'Nipun Sadeepa', '071-9941470', '4200', '[\'Fashion Hair Cut : RS.1200/-\', \'Ayurwedic Facial : RS.1500/-\', \'Ayurwedic Facial : RS.1500/-\']', '[1200, 1500, 1500]', '[10, 10, 10]', 'NO'),
(16, '2025-02-28', 'Nipun Sadeepa', '071-9941470', '4500', '[\'Ayurwedic Facial : RS.1500/-\', \'Ayurwedic Facial : RS.1500/-\', \'Ayurwedic Facial : RS.1500/-\']', '[1500, 1500, 1500]', '[10, 10, 10]', 'NO'),
(17, '2025-02-28', 'Nipun Sadeepa', '071-9941470', '420.0', '[\'Fashion Hair Cut : RS.1200/-\']', '[1200]', '[10]', 'YES'),
(18, '2025-02-28', 'Pasan Malli Gym', '077-4497308', '12000', '[\'Ayurwedic Facial : RS.1500/-\', \'Ayurwedic Facial : RS.1500/-\', \'Ayurwedic Facial : RS.1500/-\', \'Ayurwedic Facial : RS.1500/-\', \'Ayurwedic Facial : RS.1500/-\', \'Ayurwedic Facial : RS.1500/-\', \'Ayurwedic Facial : RS.1500/-\', \'Ayurwedic Facial : RS.1500/-\']', '[1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500]', '[10, 10, 10, 10, 10, 10, 10, 10]', 'NO'),
(19, '2025-02-28', 'Pasan Malli Gym', '077-4497308', '1050.0', '[\'Ayurwedic Facial : RS.1500/-\', \'Ayurwedic Facial : RS.1500/-\']', '[1500, 1500]', '[10, 10]', 'YES'),
(20, '2025-02-28', 'Nipun Sadeepa', '071-9941470', '2700', '[\'Fashion Hair Cut : RS.1200/-\', \'Ayurwedic Facial : RS.1500/-\']', '[1200, 1500]', '[10, 10]', 'NO'),
(21, '2025-03-03', 'Nipun Sadeepa', '071-9941470', '2700', '[\'Ayurwedic Facial : RS.1500/-\', \'Fashion Hair Cut : RS.1200/-\']', '[1500, 1200]', '[10, 10]', 'NO');

-- --------------------------------------------------------

--
-- Table structure for table `customer`
--

CREATE TABLE `customer` (
  `CID` int(128) NOT NULL,
  `Name` varchar(128) NOT NULL,
  `Mobile` varchar(32) NOT NULL,
  `Gender` varchar(8) NOT NULL,
  `Points` int(128) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `customer`
--

INSERT INTO `customer` (`CID`, `Name`, `Mobile`, `Gender`, `Points`) VALUES
(13, 'Nipun Sadeepa', '071-9941470', 'Male', 40),
(14, 'Pasan Malli Gym', '077-4497308', 'Male', 70);

-- --------------------------------------------------------

--
-- Table structure for table `services`
--

CREATE TABLE `services` (
  `SID` int(128) NOT NULL,
  `Service` varchar(128) NOT NULL,
  `Price` int(128) NOT NULL,
  `Point` int(16) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `services`
--

INSERT INTO `services` (`SID`, `Service`, `Price`, `Point`) VALUES
(1, 'Fashion Hair Cut', 1200, 10),
(2, 'Ayurwedic Facial', 1500, 10);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `bills`
--
ALTER TABLE `bills`
  ADD PRIMARY KEY (`bid`);

--
-- Indexes for table `customer`
--
ALTER TABLE `customer`
  ADD PRIMARY KEY (`CID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `bills`
--
ALTER TABLE `bills`
  MODIFY `bid` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT for table `customer`
--
ALTER TABLE `customer`
  MODIFY `CID` int(128) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
