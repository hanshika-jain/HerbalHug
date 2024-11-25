-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Sep 27, 2024 at 08:18 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.1.25

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
(8, 'Tulsi', 'Ocimum tenuiflorum', 'Holy Basil', 'Lamiaceae', 'It is used for medicinal properties such as boosting immunity and reducing stress. Used for skincare and helps managing repiratory conditions like asthama and bronchitis', 'Rajasthan'),
(9, 'Plant_Name', 'Scientific_Name', 'Common_Name', 'Family_Name', 'Uses', 'location\r'),
(11, 'Amla', 'Emblica officinalis', 'Amla, Amlika', 'EUPHORBIACEAE', 'The fruit of the plant is having  sour and astringent properties and is utilized as cooling, diuretic and laxative; The fruit is a good source of vitamin C.', 'Uttar Pradesh\r'),
(12, 'Amruthaballi', 'Tinospora cordifolia', 'Giloy', 'Menispermaceae', 'Can be consumed as a decoction or in powdered form. Combining with honey or amla (Indian gooseberry) may enhance its effects on immunity.', 'Uttarakhand\r'),
(17, 'Bamboo', 'Bambusa bambos', 'Kalak (Local name)', 'POACEAE', 'Leaf emmenagogue, antileprotic, febrifuge, bechic; used in haemoptysis. Stem and leaf blood purifier (used in leucoderma and inflammatory\nconditions). Root poisonous. Burnt root is applied to ringworm, bleeding gums, painful joints. Bark used for eruptions.', 'Assam\r'),
(18, 'Betel', 'Piper betle', 'Betel leaf', 'Piperaceae', 'Used in traditional medicine for its antiseptic, digestive, and stimulant properties. Chewing betel leaves with areca nut and other ingredients is a traditional practice in many cultures for oral health and digestion.', 'West Bengal\r'),
(19, 'Bhrami', 'Bacopa monnieri', 'Brahmi', 'Plantaginaceae', 'Used as a brain tonic, memory enhancer, and to reduce anxiety and stress. Consuming brahmi in powdered form or as a supplement is common for cognitive health. It can also be brewed into a tea.', 'Kerala\r'),
(20, 'Bringaraja', 'Eclipta prostrata', 'False daisy', 'Asteraceae', 'Used in Ayurveda for hair growth, liver disorders, and as a general tonic.  Bringaraja oil is often massaged into the scalp to promote hair growth and scalp health.', 'Kerala\r'),
(22, 'Caricature', 'Graptophyllum pictum', 'Caricature Plant,Kaala-aduusa', 'Acanthaceae', 'Studies have suggested anti-inflammatory, analgesic, anti-diabetic, oxytocic, nephroprotective properties.', 'Himachal Pradesh\r'),
(23, 'Castor', 'Ricinus communis', 'Castor bean', 'Euphorbiaceae', 'Castor oil derived from the seeds is used as a laxative and for various skin conditions.Castor oil can be applied topically to soothe dry or irritated skin, or taken orally for constipation relief.', 'Gujarat\r'),
(24, 'Catharanthus', 'Catharanthus roseus', 'Madagascar periwinkle', 'Apocynaceae', 'Source of alkaloids used in cancer chemotherapy and for treating diabetes.The alkaloids vinblastine and vincristine derived from Catharanthus are used in cancer treatment. Always consult a healthcare professional for proper usage.', 'Tamil Nadu\r'),
(25, 'Chakte', 'Caesalpinia platyloba', 'Chakte kok', 'Fabaceae', 'Used in traditional medicine for its anti-inflammatory properties.The bark and leaves are sometimes used to make decoctions or teas for treating inflammation.', 'Uttarakhand\r'),
(26, 'Citron Lime', 'Citrus medica var. sarcodactylis', 'Fingered citron', 'Rutaceae', 'Used in traditional medicine for its antioxidant properties and as a digestive aid.Adding citron lime juice to warm water with honey may aid digestion and boost immunity.', 'Maharashtra\r'),
(27, 'Common Rue', 'Ruta graveolens', 'Garden Rue (Eng.)', 'RUTACEAE', 'Roots used in dysentery, strangury, boils, eye diseases etc.', 'Rajasthan\r'),
(28, 'Eucalyptus', 'Eucalyptus globulus', 'Yukeliptas, Eucalyptus (Beng.)', 'MYRTACEAE', 'Leaves used in treatment of  respiratory tract diseases.', 'Tamil Nadu\r'),
(29, 'Ganike', 'Solanum torvum', 'Turkey berry', 'Solanaceae', 'Used in traditional medicine for its anti-inflammatory and antioxidant properties.Ganike can be cooked and eaten as a vegetable or used in traditional dishes for its medicinal benefits.', 'Maharashtra\r'),
(30, 'Globe Amarnath', 'Gomphrena globosa', 'Bachelor\'s button', 'Amaranthaceae', 'Used in traditional medicine for its diuretic and anti-inflammatory properties. The flowers can be brewed into a tea or added to salads for their medicinal benefits.', 'Maharashtra\r'),
(31, 'Henna', 'Lawsonia inermis', 'Henna', 'Lythraceae', 'Used in traditional medicine for its cooling and anti-inflammatory properties, and as a natural hair dye. Henna paste can be applied to the skin for cooling relief or used to dye hair naturally.', 'Rajasthan\r'),
(32, 'Hibiscus', 'Hibiscus rosa-sinensis', 'Hibiscus, Shoeblackplant', 'Malvaceae', 'Used in traditional medicine for its antioxidant properties and as a remedy for hair loss and skin conditions. Hibiscus flowers can be brewed into a tea or used as a hair rinse for shiny, healthy hair.', 'Kerala\r'),
(33, 'Honge/Hing', 'Ferula asa-foetida', 'Hing', 'APIACEAE', 'Source of the gum-resin, asafoetida, used as a condiment and in medicine, and known as gum-resin, exuded from incisions in living tap roots, used as an expectorant, laxative, antispasmodic;', 'Himachal Pradesh\r'),
(34, 'Insulin', 'Cissus quadrangularis', 'Veld grape', 'Vitaceae', 'Used in Ayurvedic medicine for its anti-inflammatory properties and as a treatment for diabetes. Insulin leaves can be chewed or brewed into a tea for managing blood sugar levels.', 'Kerala\r'),
(35, 'Jasmine', 'Jasminum officinale', 'Chameli, Jati', 'OLEACEAE', 'Leaves are used in tooth-ache relief and flowers used in treatment of piles.', 'Tamil Nadu\r'),
(36, 'Kamakasturi', 'Ocimum basilicum', 'Basil', 'Lamiaceae', 'Basil is commonly used in traditional medicine for its potential antioxidant, antimicrobial, and anti-inflammatory properties. It is also believed to aid digestion and relieve respiratory conditions like coughs and asthma.Basil leaves can be brewed into a tea, chewed raw, or used in cooking to incorporate its medicinal benefits into the diet.', 'Uttar Pradesh\r'),
(37, 'Kepala', 'Ixora coccinea', 'Ixora, Jungle Geranium', 'Rubiaceae', 'In traditional medicine, Ixora coccinea is used for its potential anti-inflammatory, antioxidant, and wound-healing properties. It may also be used to treat skin conditions and digestive issues. Ixora flowers and leaves can be brewed into a tea or used topically as a poultice for wound healing and skin ailments.', 'Kerala\r'),
(38, 'Kohlrabi', 'Brassica oleracea var. gongylodes', 'Kohlrabi', 'Brassicaceae', 'Rich in nutrients and antioxidants, used in traditional medicine for its anti-inflammatory properties.  Kohlrabi can be eaten raw or cooked as part of a balanced diet to promote overall health.', 'Punjab\r'),
(39, 'Lantana', 'Lantana camara', 'Lantana', 'Verbenaceae', 'Used in traditional medicine for its antimicrobial and anti-inflammatory properties. Lantana leaves can be brewed into a tea or applied topically as a poultice for wound healing.', 'Maharashtra\r'),
(40, 'Lemongrass', 'Cymbopogon flexuosus', 'Lemongrass (Eng.), Kodi-pullu (Mal.)', 'POACEAE', 'Oil used as mosquito repellent.', 'Kerala\r'),
(41, 'Malabar Nut', 'Justicia adhatoda', 'Arusha', 'ACANTHACEAE', 'Applied in boils and swellings and also used in diarrhoea.', 'Kerala\r'),
(42, 'Malabar Spinach', 'Basella alba or Basella rubra', 'Malabar spinach', 'Basellaceae', 'Rich in vitamins and minerals, used in traditional medicine for its cooling properties and as a laxative. Malabar spinach can be cooked and eaten as a vegetable or added to soups and stews for its health benefits.', 'Kerala\r'),
(43, 'Marigold', 'Tagetes spp.', 'Marigold', 'Asteraceae', 'Used in traditional medicine for its anti-inflammatory and antimicrobial properties.  Marigold flowers can be brewed into a tea or used topically as a poultice for wound healing and skin conditions.', 'Maharashtra\r'),
(44, 'Mint', 'Mentha arvensis', 'Podina, Pudina', 'LAMIACEAE', 'The plant is employed as antiseptic, carminative and stimulant. The decoction of the herb is used in fever and heat apoplexy.', 'Uttar Pradesh\r'),
(45, 'Neem', 'Murraya koenigii', 'Kathneem, Mitha neem', 'RUTACEAE', 'Leaves used in diarrhoea and dysentery and cuts. Leaves along with root-bark used in curing coughs, rheumatism and hysteria.', 'Maharashtra\r'),
(46, 'Nelavembu', 'Andrographis paniculata', 'Nilavembu', 'Acanthaceae', 'Used as an immunostimulant and to treat fevers and infections. Nelavembu leaves can be brewed into a tea or decoction for boosting immunity and treating common ailments.', 'Tamil Nadu\r'),
(48, 'Noni', 'Morinda citrifolia', 'Noni', 'Rubiaceae', 'Used in traditional medicine for its antioxidant and anti-inflammatory properties.  Noni fruit juice can be consumed as a health tonic or applied topically for skin conditions.', 'Kerala\r'),
(49, 'Padri', 'Tabernaemontana divaricata', 'Fragrant Padri-tree, Yellow Snaketree', 'Apocynaceae', 'Padri (Tabernaemontana divaricata) is used in traditional medicine for its potential analgesic, anti-inflammatory, and antipyretic properties. It may also be used to treat fevers and skin conditions.Padri leaves and flowers can be brewed into a tea or applied topically as a poultice for pain relief and skin ailments.', 'Assam\r'),
(50, 'Papaya', 'Carica papaya', 'Papeeta, Papaya', 'CARICACEAE', 'Medicine prepared from the bark is used in blood dysentery, wounds, eye disease.', 'Maharashtra\r'),
(51, 'Parijatha', 'Nyctanthes arbor-tristis', 'Parijat, Night-flowering jasmine', 'Oleaceae', 'Used in traditional medicine for its anti-inflammatory and analgesic properties. Parijatha flowers can be brewed into a tea or used in aromatherapy for relaxation.', 'Uttar Pradesh\r'),
(52, 'Sampige', 'Magnolia champaca', 'Champak', 'Magnoliaceae', 'Used in traditional medicine for its antimicrobial and anti-inflammatory properties. Sampige flowers can be used in aromatherapy, and the bark and leaves can be brewed into a tea for medicinal purposes.', 'Kerala\r'),
(53, 'Seethaashoka', 'Saraca asoca', 'Ashoka tree', 'Fabaceae', 'Used in traditional medicine for its uterine tonic and anti-inflammatory properties. Seethaashoka bark can be brewed into a tea or decoction for treating menstrual disorders and inflammation.', 'Odisha\r'),
(54, 'Taro', 'Colocasia esculenta', 'Taro', 'Araceae', 'Rich in nutrients, used in traditional medicine for its anti-inflammatory properties and as a source of dietary fiber. Taro roots can be cooked and eaten, while the leaves can be used in salads or cooked as greens for their health benefits.', 'Kerala\r'),
(55, 'Tecoma', 'Tecoma stans', 'Sonapatti (Tam.)', 'BIGNONIACEAE', 'Bark is used for syphilis.', 'Maharashtra\r'),
(56, 'Thumbe', 'Leucas aspera', 'Thumbai Plant', 'Lamiaceae', 'Thumbai (Leucas aspera) is widely used in traditional medicine for its potential anti-inflammatory, antimicrobial, and analgesic properties. It is commonly used to treat respiratory conditions, skin disorders, and digestive issues.   Thumbai leaves and flowers can be brewed into a tea, crushed and applied topically, or consumed orally in various forms (e.g., decoction, powder) to address specific health concerns.', 'Karnataka\r'),
(58, 'Turmeric', 'Curcuma longa', 'Turmeric', 'Zingiberaceae', 'Contains curcumin with anti-inflammatory and antioxidant properties, aids digestion, wound healing.  Turmeric powder can be added to dishes, brewed into a tea, or mixed with honey and warm milk for its health benefits. Combining with black pepper enhances its absorption.', 'Andhra Pradesh\r');

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
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `plantsf`
--
ALTER TABLE `plantsf`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=59;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
