-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Sep 20, 2024 at 01:31 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.0.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `herbalhug`
--

-- --------------------------------------------------------

--
-- Table structure for table `plantsf`
--

CREATE TABLE `plantsf` (
  `ID` int(11) NOT NULL,
  `Plant_Name` varchar(50) DEFAULT NULL,
  `Scientific_Name` varchar(100) DEFAULT NULL,
  `Common_Name` varchar(100) DEFAULT NULL,
  `Family_Name` varchar(100) DEFAULT NULL,
  `Uses` varchar(500) DEFAULT NULL,
  `location` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `plantsf`
--

INSERT INTO `plantsf` (`ID`, `Plant_Name`, `Scientific_Name`, `Common_Name`, `Family_Name`, `Uses`, `location`) VALUES
(1, 'Arali', 'Fatsia japonica', 'Japanese Arali', 'Araliaceae', 'Used in traditional medicine for treating coughs, colds, and arthritis.The leaves can be brewed into a tea or used in poultices for arthritis pain relief.', 'Tamil Nadu'),
(2, 'Asoka', 'Polyalthia longifolia', 'Asoka', 'ANNONACEAE', 'The her is useed in inflamatory swellings, urinary calculi, boils, strangury. Its Ash is mixed with pepper and applied in boils and ulcers.Pounded leaves are useful in Poultice and inflamatory swellins.', 'Madhya Pradesh'),
(3, 'Badipala', 'Terminalia bellirica', 'Baheda', 'Combretaceae', 'Used in Ayurvedic medicine for respiratory issues, digestive disorders, and as a rejuvenating tonic.Often used in combination with other herbs like amla and haritaki in Ayurvedic formulations for digestive health.', 'Rajasthan'),
(4, 'Balloon Vine', 'Cardiospermum halicacabum', 'Balloon Plant', 'Sapindaceae', 'Traditionally used for its anti-inflammatory and analgesic properties, and to treat skin conditions.The leaves can be crushed and applied topically to the affected area for skin conditions like eczema or insect bites.', 'Kerala'),
(5, 'Aloe vera', 'Aloe vera', 'Ghee Kunvar', 'LILIACEAE', 'Leaves are used in treatment of chronic ulcers. Fresh juice is useful in fevers and pulp is used on uterus. The root is used in colic.', 'Rajasthan'),
(6, 'Camphor', 'Cinnamomum camphora', 'Kapur', 'Lauraceae', 'The leaves is having carminative properties. It is also employed in colic and diarrhoea.', 'Karnataka'),
(7, 'Castor', 'Ricimus communis', 'Castor bean', 'Euphorbiaceae', 'Castor oil derived from the seats is used as a laxative and for various skin conditions. Castor oil can be applied typically to soothe dry or irritated skin, or taken orally for constipation relief.', 'Gujarat'),
(8, 'Tulsi', 'Ocimum tenuiflorum', 'Holy Basil', 'Lamiaceae', 'It is used for medicinal properties such as boosting immunity and reducing stress. Used for skincare and helps managing repiratory conditions like asthama and bronchitis', 'Rajasthan');

-- --------------------------------------------------------

--
-- Table structure for table `user_loc`
--

CREATE TABLE `user_loc` (
  `User_Id` int(11) NOT NULL,
  `Scientific_Name` varchar(100) NOT NULL,
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `Date_found` date DEFAULT NULL,
  `Presence` tinyint(1) DEFAULT NULL,
  `User_id_updated` int(11) DEFAULT NULL,
  `Last_Confirmed` date DEFAULT NULL,
  `remarks` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `user_loc`
--

INSERT INTO `user_loc` (`User_Id`, `Scientific_Name`, `latitude`, `longitude`, `Date_found`, `Presence`, `User_id_updated`, `Last_Confirmed`, `remarks`) VALUES
(106, 'Aloe vera', 12.93448543548584, 77.61923217773438, '2024-05-30', NULL, NULL, '2024-05-30', NULL),
(0, 'Aloe vera', 12.94336, 77.6077312, '2024-09-20', 1, NULL, '2024-09-20', NULL),
(0, 'Aloe vera', 12.9794048, 77.594624, '2024-09-18', 1, NULL, '2024-09-18', NULL),
(107, 'Aloe vera', 18.27359962463379, 77.5946273803711, '2024-05-31', NULL, NULL, '2024-05-31', NULL),
(112, 'Ocimum tenuiflorum', 12.927467346191406, 77.60895538330078, '2024-06-11', NULL, NULL, '2024-06-11', NULL),
(111, 'Ocimum tenuiflorum', 12.93448543548584, 77.61923217773438, '2024-06-11', NULL, NULL, '2024-06-11', NULL),
(0, 'Ocimum tenuiflorum', 12.9609975, 77.585393, '2024-09-20', 0, NULL, '2024-09-20', NULL),
(110, 'Ocimum tenuiflorum', 12.972850799560547, 77.62084197998047, '2024-05-31', NULL, NULL, '2024-05-31', NULL),
(2, 'Ocimum Tenuiflorum', 22.670799255371094, 71.57240295410156, '2024-05-31', 1, 3, '2024-05-31', NULL),
(1, 'Ocimum tenuiflorum', 26.628450393676758, 73.8775634765625, '2024-05-31', 1, 1, '2024-05-31', NULL);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `plantsf`
--
ALTER TABLE `plantsf`
  ADD PRIMARY KEY (`ID`),
  ADD UNIQUE KEY `Scientific_Name` (`Scientific_Name`);

--
-- Indexes for table `user_loc`
--
ALTER TABLE `user_loc`
  ADD PRIMARY KEY (`Scientific_Name`,`latitude`,`longitude`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `plantsf`
--
ALTER TABLE `plantsf`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `user_loc`
--
ALTER TABLE `user_loc`
  ADD CONSTRAINT `user_loc_ibfk_1` FOREIGN KEY (`Scientific_Name`) REFERENCES `plantsf` (`Scientific_Name`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
