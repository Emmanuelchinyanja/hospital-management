-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 23, 2025 at 01:06 PM
-- Server version: 10.4.27-MariaDB
-- PHP Version: 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `hospital-management`
--

-- --------------------------------------------------------

--
-- Table structure for table `doctors`
--

CREATE TABLE `doctors` (
  `id` int(4) NOT NULL,
  `firstname` varchar(255) NOT NULL,
  `lastname` varchar(255) NOT NULL,
  `national_id` varchar(255) NOT NULL,
  `qualification` varchar(255) NOT NULL,
  `specialization` enum('Surgeon','Optician','Psychian','Neurologuist','Medicine','Hematologist') DEFAULT NULL,
  `date_registered` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `doctors`
--

INSERT INTO `doctors` (`id`, `firstname`, `lastname`, `national_id`, `qualification`, `specialization`, `date_registered`) VALUES
(1, 'George', 'Phiri', 'XZY342', 'Masters in Neurology', 'Neurologuist', '2025-06-23 10:40:22');

-- --------------------------------------------------------

--
-- Table structure for table `patients`
--

CREATE TABLE `patients` (
  `patient_id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `date_of_birth` datetime NOT NULL,
  `gender` varchar(10) NOT NULL,
  `blood_type` enum('O','AB','O+','B','B+') NOT NULL,
  `date_registered` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `patients`
--

INSERT INTO `patients` (`patient_id`, `name`, `date_of_birth`, `gender`, `blood_type`, `date_registered`) VALUES
(1, 'Antony kazembe', '0000-00-00 00:00:00', 'male', 'O', '2025-05-18 14:05:25'),
(2, 'chisomo kanzengo', '0000-00-00 00:00:00', 'female', 'O', '2025-05-18 14:05:52'),
(3, 'prince', '0000-00-00 00:00:00', 'male', 'O', '2025-05-19 11:41:34'),
(4, 'chifundo kachingwe', '0000-00-00 00:00:00', 'male', 'O', '2025-05-21 06:46:20'),
(5, 'emmanuel kadzanja', '0000-00-00 00:00:00', 'male', 'O', '2025-05-21 06:48:55'),
(6, 'manxy', '0000-00-00 00:00:00', 'male', 'O', '2025-05-22 06:39:11'),
(7, 'emmanuel chinyanja', '0000-00-00 00:00:00', 'male', 'O', '2025-06-22 15:27:27'),
(8, 'princo', '0000-00-00 00:00:00', 'male', 'O', '2025-06-22 20:32:35'),
(9, 'ejchinyanja', '0000-00-00 00:00:00', 'male', 'O', '2025-06-22 20:49:36'),
(10, 'chiso', '0000-00-00 00:00:00', 'female', 'O', '2025-06-22 21:13:07');

-- --------------------------------------------------------

--
-- Table structure for table `treatments`
--

CREATE TABLE `treatments` (
  `treatment_id` int(11) NOT NULL,
  `patient_id` int(11) NOT NULL,
  `doctor_id` int(4) NOT NULL,
  `symptoms` text DEFAULT NULL,
  `treatment` text DEFAULT NULL,
  `blood_pressure` int(3) NOT NULL,
  `temperature` int(2) NOT NULL,
  `weight` int(3) NOT NULL,
  `date` timestamp NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `treatments`
--

INSERT INTO `treatments` (`treatment_id`, `patient_id`, `doctor_id`, `symptoms`, `treatment`, `blood_pressure`, `temperature`, `weight`, `date`) VALUES
(1, 1, 1, 'Headache ', 'Paracetamol', 132, 36, 60, '2025-05-19 00:56:39'),
(2, 1, 1, 'Nasal discharged', 'Flumed', 132, 36, 67, '2025-05-19 00:57:06'),
(3, 1, 0, 'Dry cough', 'Conjex', 133, 36, 67, '2025-05-19 10:02:16'),
(4, 3, 1, 'BP: 232\\333, Pulse: 23, Resp: 433hz, Oxygen: 233rf', '', 0, 0, 0, '2025-05-19 11:44:48');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp(),
  `role` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `password`, `timestamp`, `role`) VALUES
(1, 'reception', '1234', '2025-05-22 06:38:50', 'Receptionist'),
(2, 'nurse', '1234', '2025-05-21 06:44:56', 'Nurse'),
(3, 'doctor', '1234', '2025-05-19 11:45:28', 'Doctor'),
(4, 'admin', '1234', '2025-05-19 11:47:12', 'Admin');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `doctors`
--
ALTER TABLE `doctors`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `patients`
--
ALTER TABLE `patients`
  ADD PRIMARY KEY (`patient_id`);

--
-- Indexes for table `treatments`
--
ALTER TABLE `treatments`
  ADD PRIMARY KEY (`treatment_id`),
  ADD KEY `patient_id` (`patient_id`),
  ADD KEY `doctor_id` (`doctor_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `doctors`
--
ALTER TABLE `doctors`
  MODIFY `id` int(4) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `patients`
--
ALTER TABLE `patients`
  MODIFY `patient_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `treatments`
--
ALTER TABLE `treatments`
  MODIFY `treatment_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `treatments`
--
ALTER TABLE `treatments`
  ADD CONSTRAINT `treatments_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patients` (`patient_id`),
  ADD CONSTRAINT `treatments_ibfk_2` FOREIGN KEY (`doctor_id`) REFERENCES `doctors` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
