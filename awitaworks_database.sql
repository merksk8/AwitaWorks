-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Sep 03, 2022 at 05:42 PM
-- Server version: 10.7.4-MariaDB-1:10.7.4+maria~bionic
-- PHP Version: 8.0.19

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `awitaworks`
--

-- --------------------------------------------------------

--
-- Table structure for table `rooms_active`
--

CREATE TABLE `rooms_active` (
  `register_id` int(11) NOT NULL,
  `room_id` bigint(255) NOT NULL,
  `server_id` bigint(255) NOT NULL,
  `price` float NOT NULL DEFAULT 0,
  `max_active` int(11) NOT NULL DEFAULT -1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `work_registers`
--

CREATE TABLE `work_registers` (
  `register_id` int(99) NOT NULL,
  `user_id` bigint(99) NOT NULL,
  `username` varchar(999) NOT NULL DEFAULT '',
  `time_created` datetime NOT NULL DEFAULT current_timestamp(),
  `start_message_id` bigint(255) NOT NULL DEFAULT 0,
  `work_type` text NOT NULL DEFAULT 'default',
  `time_finished` datetime DEFAULT NULL,
  `finish_message_id` bigint(255) NOT NULL DEFAULT 0,
  `total_minutes` int(99) NOT NULL DEFAULT 0,
  `room_id` bigint(255) NOT NULL DEFAULT 0,
  `server_id` bigint(255) NOT NULL DEFAULT 0,
  `deleted` tinyint(1) NOT NULL DEFAULT 0,
  `deleted_manually` tinyint(1) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `rooms_active`
--
ALTER TABLE `rooms_active`
  ADD PRIMARY KEY (`register_id`);

--
-- Indexes for table `work_registers`
--
ALTER TABLE `work_registers`
  ADD PRIMARY KEY (`register_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `rooms_active`
--
ALTER TABLE `rooms_active`
  MODIFY `register_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `work_registers`
--
ALTER TABLE `work_registers`
  MODIFY `register_id` int(99) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
