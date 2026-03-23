-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Jan 22, 2026 at 01:33 PM
-- Server version: 8.0.30
-- PHP Version: 8.3.27

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `fuzzy_tsukamoto`
--

-- --------------------------------------------------------

--
-- Table structure for table `calculation_results`
--

CREATE TABLE `calculation_results` (
  `id` int NOT NULL,
  `stock_id` int NOT NULL,
  `final_score` decimal(10,2) NOT NULL,
  `risk_category` varchar(50) NOT NULL,
  `calculation_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `calculation_results`
--

INSERT INTO `calculation_results` (`id`, `stock_id`, `final_score`, `risk_category`, `calculation_date`) VALUES
(269, 28, '82.67', 'Low Risk', '2026-01-22 13:29:06'),
(270, 29, '100.00', 'Low Risk', '2026-01-22 13:29:06'),
(271, 30, '57.06', 'Medium Risk', '2026-01-22 13:29:06'),
(272, 31, '71.09', 'Low Risk', '2026-01-22 13:29:06'),
(273, 32, '67.07', 'Medium Risk', '2026-01-22 13:29:06'),
(274, 33, '17.33', 'High Risk', '2026-01-22 13:29:06');

-- --------------------------------------------------------

--
-- Table structure for table `fuzzy_outputs`
--

CREATE TABLE `fuzzy_outputs` (
  `id` int NOT NULL,
  `output_name` varchar(50) NOT NULL,
  `min_value` decimal(10,2) NOT NULL,
  `max_value` decimal(10,2) NOT NULL,
  `description` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `fuzzy_outputs`
--

INSERT INTO `fuzzy_outputs` (`id`, `output_name`, `min_value`, `max_value`, `description`) VALUES
(1, 'Risk_Score', '0.00', '100.00', 'Skor risiko saham (0=High Risk, 100=Low Risk)');

-- --------------------------------------------------------

--
-- Table structure for table `fuzzy_output_sets`
--

CREATE TABLE `fuzzy_output_sets` (
  `id` int NOT NULL,
  `set_name` varchar(50) DEFAULT NULL,
  `min_value` decimal(20,2) DEFAULT NULL,
  `max_value` decimal(20,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `fuzzy_output_sets`
--

INSERT INTO `fuzzy_output_sets` (`id`, `set_name`, `min_value`, `max_value`) VALUES
(1, 'Low_Risk', '60.00', '100.00'),
(2, 'Medium_Risk', '30.00', '70.00'),
(3, 'High_Risk', '0.00', '40.00');

-- --------------------------------------------------------

--
-- Table structure for table `fuzzy_rules`
--

CREATE TABLE `fuzzy_rules` (
  `id` int NOT NULL,
  `rule_name` varchar(100) NOT NULL,
  `volatilitas_set` varchar(50) NOT NULL,
  `volume_set` varchar(50) NOT NULL,
  `frekuensi_set` varchar(50) NOT NULL,
  `output_set` varchar(50) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `fuzzy_rules`
--

INSERT INTO `fuzzy_rules` (`id`, `rule_name`, `volatilitas_set`, `volume_set`, `frekuensi_set`, `output_set`, `created_at`) VALUES
(103, 'R1', 'Rendah', 'Rendah', 'Rendah', 'Medium_Risk', '2025-12-22 16:25:50'),
(104, 'R2', 'Rendah', 'Rendah', 'Sedang', 'Medium_Risk', '2025-12-22 16:25:50'),
(105, 'R3', 'Rendah', 'Rendah', 'Tinggi', 'Low_Risk', '2025-12-22 16:25:50'),
(106, 'R4', 'Rendah', 'Sedang', 'Rendah', 'Medium_Risk', '2025-12-22 16:25:50'),
(107, 'R5', 'Rendah', 'Sedang', 'Sedang', 'Low_Risk', '2025-12-22 16:25:50'),
(108, 'R6', 'Rendah', 'Sedang', 'Tinggi', 'Low_Risk', '2025-12-22 16:25:50'),
(109, 'R7', 'Rendah', 'Tinggi', 'Rendah', 'Low_Risk', '2025-12-22 16:25:50'),
(110, 'R8', 'Rendah', 'Tinggi', 'Sedang', 'Low_Risk', '2025-12-22 16:25:50'),
(111, 'R9', 'Rendah', 'Tinggi', 'Tinggi', 'Low_Risk', '2025-12-22 16:25:50'),
(112, 'R10', 'Sedang', 'Rendah', 'Rendah', 'High_Risk', '2025-12-22 16:25:50'),
(113, 'R11', 'Sedang', 'Rendah', 'Sedang', 'Medium_Risk', '2025-12-22 16:25:50'),
(114, 'R12', 'Sedang', 'Rendah', 'Tinggi', 'Medium_Risk', '2025-12-22 16:25:50'),
(115, 'R13', 'Sedang', 'Sedang', 'Rendah', 'Medium_Risk', '2025-12-22 16:25:50'),
(116, 'R14', 'Sedang', 'Sedang', 'Sedang', 'Medium_Risk', '2025-12-22 16:25:50'),
(117, 'R15', 'Sedang', 'Sedang', 'Tinggi', 'Low_Risk', '2025-12-22 16:25:50'),
(118, 'R16', 'Sedang', 'Tinggi', 'Rendah', 'Medium_Risk', '2025-12-22 16:25:50'),
(119, 'R17', 'Sedang', 'Tinggi', 'Sedang', 'Low_Risk', '2025-12-22 16:25:51'),
(120, 'R18', 'Sedang', 'Tinggi', 'Tinggi', 'Low_Risk', '2025-12-22 16:25:51'),
(121, 'R19', 'Tinggi', 'Rendah', 'Rendah', 'High_Risk', '2025-12-22 16:25:51'),
(122, 'R20', 'Tinggi', 'Rendah', 'Sedang', 'High_Risk', '2025-12-22 16:25:51'),
(123, 'R21', 'Tinggi', 'Rendah', 'Tinggi', 'Medium_Risk', '2025-12-22 16:25:51'),
(124, 'R22', 'Tinggi', 'Sedang', 'Rendah', 'High_Risk', '2025-12-22 16:25:51'),
(125, 'R23', 'Tinggi', 'Sedang', 'Sedang', 'Medium_Risk', '2025-12-22 16:25:51'),
(126, 'R24', 'Tinggi', 'Sedang', 'Tinggi', 'Medium_Risk', '2025-12-22 16:25:51'),
(127, 'R25', 'Tinggi', 'Tinggi', 'Rendah', 'Medium_Risk', '2025-12-22 16:25:51'),
(128, 'R26', 'Tinggi', 'Tinggi', 'Sedang', 'Medium_Risk', '2025-12-22 16:25:51'),
(129, 'R27', 'Tinggi', 'Tinggi', 'Tinggi', 'Low_Risk', '2025-12-22 16:25:51');

-- --------------------------------------------------------

--
-- Table structure for table `fuzzy_sets`
--

CREATE TABLE `fuzzy_sets` (
  `id` int NOT NULL,
  `variable_id` int NOT NULL,
  `set_name` varchar(50) NOT NULL,
  `min_value` decimal(20,2) DEFAULT NULL,
  `max_value` decimal(20,2) DEFAULT NULL,
  `peak_start` decimal(20,2) DEFAULT NULL,
  `peak_end` decimal(20,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `fuzzy_sets`
--

INSERT INTO `fuzzy_sets` (`id`, `variable_id`, `set_name`, `min_value`, `max_value`, `peak_start`, `peak_end`) VALUES
(20, 2, 'Rendah', '0.00', '50000000.00', '0.00', '25000000.00'),
(21, 2, 'Sedang', '30000000.00', '120000000.00', '60000000.00', '90000000.00'),
(22, 2, 'Tinggi', '100000000.00', '300000000.00', '150000000.00', '300000000.00'),
(23, 3, 'Rendah', '0.00', '10000.00', '0.00', '5000.00'),
(24, 3, 'Sedang', '6000.00', '20000.00', '10000.00', '15000.00'),
(25, 3, 'Tinggi', '15000.00', '40000.00', '25000.00', '40000.00'),
(29, 1, 'Rendah', '0.00', '60.00', '0.00', '30.00'),
(30, 1, 'Sedang', '30.00', '120.00', '60.00', '90.00'),
(31, 1, 'Tinggi', '90.00', '300.00', '150.00', '300.00');

-- --------------------------------------------------------

--
-- Table structure for table `fuzzy_variables`
--

CREATE TABLE `fuzzy_variables` (
  `id` int NOT NULL,
  `variable_name` varchar(50) NOT NULL,
  `min_value` decimal(20,2) DEFAULT NULL,
  `max_value` decimal(20,2) DEFAULT NULL,
  `description` text,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `fuzzy_variables`
--

INSERT INTO `fuzzy_variables` (`id`, `variable_name`, `min_value`, `max_value`, `description`, `created_at`) VALUES
(1, 'Volatilitas', '0.00', '300.00', NULL, '2025-12-22 16:25:50'),
(2, 'Volume', '0.00', '300000000.00', NULL, '2025-12-22 16:25:50'),
(3, 'Frekuensi', '0.00', '40000.00', NULL, '2025-12-22 16:25:50');

-- --------------------------------------------------------

--
-- Table structure for table `stock_data`
--

CREATE TABLE `stock_data` (
  `id` int NOT NULL,
  `stock_code` varchar(10) NOT NULL,
  `stock_name` varchar(100) DEFAULT NULL,
  `selisih` decimal(10,2) NOT NULL,
  `volume` bigint NOT NULL,
  `frekuensi` int NOT NULL,
  `input_date` date NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `stock_data`
--

INSERT INTO `stock_data` (`id`, `stock_code`, `stock_name`, `selisih`, `volume`, `frekuensi`, `input_date`, `created_at`) VALUES
(28, 'BBCA', 'Bank Central Asia Tbk.', '100.00', 164597000, 29517, '2026-01-22', '2026-01-22 13:23:30'),
(29, 'BBRI', 'Bank Rakyat Indonesia (Persero) Tbk.', '0.00', 226832200, 28803, '2026-01-22', '2026-01-22 13:24:27'),
(30, 'TLKM', 'Telkom Indonesia (Persero) Tbk.', '50.00', 96333300, 9425, '2026-01-22', '2026-01-22 13:25:34'),
(31, 'ASII', 'Astra International Tbk.', '0.00', 46038900, 13608, '2026-01-22', '2026-01-22 13:26:44'),
(32, 'UNVR', 'Unilever Indonesia Tbk.', '35.00', 50952000, 9231, '2026-01-22', '2026-01-22 13:27:53'),
(33, 'ICBP', 'Indofood CBP Sukses Makmur Tbk.', '100.00', 2335600, 2079, '2026-01-22', '2026-01-22 13:28:52');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('admin','user') DEFAULT 'user',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `password`, `role`, `created_at`) VALUES
(1, 'admin', '$2b$12$im70DnrmxXLegBO3TH.mjee6XMuVweiCkbMthpv899sv6MOMvsJ2u', 'admin', '2025-12-11 13:07:56'),
(2, 'user', '$2b$12$t4ym7hf.vJsMT7X1h/0i9er1cYl9lm01UGRPVDcsmzXNfDO/ZJyHa', 'user', '2025-12-11 13:58:01');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `calculation_results`
--
ALTER TABLE `calculation_results`
  ADD PRIMARY KEY (`id`),
  ADD KEY `stock_id` (`stock_id`),
  ADD KEY `idx_calculation_date` (`calculation_date`);

--
-- Indexes for table `fuzzy_outputs`
--
ALTER TABLE `fuzzy_outputs`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `fuzzy_output_sets`
--
ALTER TABLE `fuzzy_output_sets`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `fuzzy_rules`
--
ALTER TABLE `fuzzy_rules`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `fuzzy_sets`
--
ALTER TABLE `fuzzy_sets`
  ADD PRIMARY KEY (`id`),
  ADD KEY `variable_id` (`variable_id`);

--
-- Indexes for table `fuzzy_variables`
--
ALTER TABLE `fuzzy_variables`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `stock_data`
--
ALTER TABLE `stock_data`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_stock_code` (`stock_code`),
  ADD KEY `idx_input_date` (`input_date`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `calculation_results`
--
ALTER TABLE `calculation_results`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=275;

--
-- AUTO_INCREMENT for table `fuzzy_outputs`
--
ALTER TABLE `fuzzy_outputs`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `fuzzy_output_sets`
--
ALTER TABLE `fuzzy_output_sets`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `fuzzy_rules`
--
ALTER TABLE `fuzzy_rules`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=130;

--
-- AUTO_INCREMENT for table `fuzzy_sets`
--
ALTER TABLE `fuzzy_sets`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=32;

--
-- AUTO_INCREMENT for table `fuzzy_variables`
--
ALTER TABLE `fuzzy_variables`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `stock_data`
--
ALTER TABLE `stock_data`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=34;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `calculation_results`
--
ALTER TABLE `calculation_results`
  ADD CONSTRAINT `calculation_results_ibfk_1` FOREIGN KEY (`stock_id`) REFERENCES `stock_data` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `fuzzy_sets`
--
ALTER TABLE `fuzzy_sets`
  ADD CONSTRAINT `fuzzy_sets_ibfk_1` FOREIGN KEY (`variable_id`) REFERENCES `fuzzy_variables` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
