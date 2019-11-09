-- phpMyAdmin SQL Dump
-- version 4.7.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 06, 2019 at 10:40 AM
-- Server version: 10.1.26-MariaDB
-- PHP Version: 7.1.9

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `cellardr`
--

-- --------------------------------------------------------

--
-- Table structure for table `boite`
--

CREATE TABLE `boite` (
  `id` int(11) NOT NULL,
  `nom` text NOT NULL,
  `theme` int(11) NOT NULL,
  `categorie_age` enum('0-3','4-7','7-12','12-18') NOT NULL,
  `img_link` text,
  `description` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `boite`
--

INSERT INTO `boite` (`id`, `nom`, `theme`, `categorie_age`, `img_link`, `description`) VALUES
(1, 'Camion poubelle', 2, '0-3', '/public/img/boites/city-camion-poubelle.jpeg', 'Le robuste camion poubelle permet de nettoyer les rues de LEGO City.'),
(2, 'La Statue de la Liberté', 1, '12-18', '/public/img/boites/architecture-status-liberte.jpeg', 'Créez un célèbre symbole de liberté : la Statue de la Liberté !'),
(3, 'Le van des surfeurs', 4, '7-12', '/public/img/boites/3in1-van-surfeur.jpeg', 'Partez faire un tour sur la côte avec l’ensemble Le van des surfeurs 3-en-1 !'),
(4, 'Le camion du chef des pompiers', 2, '4-7', '/public/img/boites/city-camion-chef-pompiers.jpeg', 'Les enfants découvrent un jeu riche en action avec ce superbe camion du chef des pompiers !');

-- --------------------------------------------------------

--
-- Table structure for table `couleur`
--

CREATE TABLE `couleur` (
  `ref_color` int(11) NOT NULL,
  `nom` text NOT NULL,
  `rgb` text NOT NULL,
  `is_trans` tinyint(1) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `couleur`
--

INSERT INTO `couleur` (`ref_color`, `nom`, `rgb`, `is_trans`) VALUES
(1, 'Orange', '255,140,0', 0),
(2, 'Silver', '192,192,192', 0),
(3, 'Gris', '169,169,169', 0),
(4, 'Maron', '165,42,42', 0),
(5, 'Jaune', '255,255,0', 0),
(6, 'Bleu', '65,105,225', 0),
(7, 'Blanc', '255,255,255', 0),
(8, 'Noir', '0,0,0', 0),
(9, 'Beige', '245,245,220', 0),
(10, 'Violet', '182, 102, 210', 0),
(11, 'Rose', '128,0,128', 0),
(12, 'Rouge', '255,0,0', 0),
(13, 'Or', '255,223,0', 0),
(14, 'Vert', '0,100,0', 0),
(15, 'Orange transparent', '255,140,0', 1),
(17, 'Gris transparent', '169,169,169', 1),
(18, 'Maron transparent', '165,42,42', 1),
(19, 'Jaune transparent', '255,255,0', 1),
(20, 'Bleu transparent', '65,105,225', 1),
(21, 'Blanc transparent', '255,255,255', 1),
(22, 'Noir transparent', '0,0,0', 1),
(24, 'Violet transparent', '182, 102, 210', 1),
(25, 'Rose transparent', '128,0,128', 1),
(26, 'Rouge transparent', '255,0,0', 1),
(28, 'Vert transparent', '0,100,0', 1);

-- --------------------------------------------------------

--
-- Table structure for table `liste_brique`
--

CREATE TABLE `liste_brique` (
  `boite_id` int(11) NOT NULL,
  `piece_id` int(11) NOT NULL,
  `quantite` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `liste_brique`
--

INSERT INTO `liste_brique` (`boite_id`, `piece_id`, `quantite`) VALUES
(2, 5, 10),
(2, 1, 120),
(4, 3, 15),
(2, 3, 15);

-- --------------------------------------------------------

--
-- Table structure for table `pieces`
--

CREATE TABLE `pieces` (
  `id` int(11) NOT NULL,
  `nom` text NOT NULL,
  `couleur` int(11) NOT NULL,
  `taille` int(11) NOT NULL DEFAULT '1',
  `specifique` tinyint(1) NOT NULL DEFAULT '0',
  `description` text NOT NULL,
  `prix` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `pieces`
--

INSERT INTO `pieces` (`id`, `nom`, `couleur`, `taille`, `specifique`, `description`, `prix`) VALUES
(1, 'Brique Standart', 9, 1, 0, '', 0.07),
(2, 'Brique Standart', 10, 2, 0, '', 0.11),
(3, 'Brique Standart', 3, 3, 0, '', 0.14),
(4, 'Brique Standart', 9, 4, 0, '', 0.16),
(5, 'Brique Palace', 13, 14, 0, 'Brique edition limité', 0.28);

-- --------------------------------------------------------

--
-- Table structure for table `taille`
--

CREATE TABLE `taille` (
  `ref_size` int(11) NOT NULL,
  `longueur` int(11) NOT NULL,
  `largeur` int(11) NOT NULL,
  `hauteur` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `taille`
--

INSERT INTO `taille` (`ref_size`, `longueur`, `largeur`, `hauteur`) VALUES
(1, 1, 1, 1),
(2, 1, 2, 1),
(3, 1, 3, 1),
(4, 1, 4, 1),
(5, 1, 5, 1),
(6, 1, 6, 1),
(7, 1, 7, 1),
(8, 1, 8, 1),
(9, 1, 9, 1),
(10, 1, 10, 1),
(11, 1, 11, 1),
(12, 1, 12, 1),
(13, 2, 1, 1),
(14, 2, 2, 1),
(15, 2, 3, 1),
(16, 2, 4, 1),
(17, 2, 5, 1),
(18, 2, 6, 1),
(19, 2, 7, 1),
(20, 2, 8, 1),
(21, 2, 9, 1),
(22, 2, 10, 1),
(23, 2, 11, 1),
(24, 2, 12, 1),
(25, 3, 1, 1),
(26, 3, 2, 1),
(27, 3, 3, 1),
(28, 3, 4, 1),
(29, 3, 5, 1),
(30, 3, 6, 1),
(31, 3, 7, 1),
(32, 3, 8, 1),
(33, 3, 9, 1),
(34, 3, 10, 1),
(35, 3, 11, 1),
(36, 3, 12, 1),
(37, 4, 1, 1),
(38, 4, 2, 1),
(39, 4, 3, 1),
(40, 4, 4, 1),
(41, 4, 5, 1),
(42, 4, 6, 1),
(43, 4, 7, 1),
(44, 4, 8, 1),
(45, 4, 9, 1),
(46, 4, 10, 1),
(47, 4, 11, 1),
(48, 4, 12, 1),
(49, 1, 1, 0.33),
(50, 1, 2, 0.33),
(51, 1, 3, 0.33),
(52, 1, 4, 0.33),
(53, 1, 5, 0.33),
(54, 1, 6, 0.33),
(55, 1, 7, 0.33),
(56, 1, 8, 0.33),
(57, 1, 9, 0.33),
(58, 1, 10, 0.33),
(59, 1, 11, 0.33),
(60, 1, 12, 0.33),
(61, 2, 1, 0.33),
(62, 2, 2, 0.33),
(63, 2, 3, 0.33),
(64, 2, 4, 0.33),
(65, 2, 5, 0.33),
(66, 2, 6, 0.33),
(67, 2, 7, 0.33),
(68, 2, 8, 0.33),
(69, 2, 9, 0.33),
(70, 2, 10, 0.33),
(71, 2, 11, 0.33),
(72, 2, 12, 0.33),
(73, 3, 1, 0.33),
(74, 3, 2, 0.33),
(75, 3, 3, 0.33),
(76, 3, 4, 0.33),
(77, 3, 5, 0.33),
(78, 3, 6, 0.33),
(79, 3, 7, 0.33),
(80, 3, 8, 0.33),
(81, 3, 9, 0.33),
(82, 3, 10, 0.33),
(83, 3, 11, 0.33),
(84, 3, 12, 0.33),
(85, 4, 1, 0.33),
(86, 4, 2, 0.33),
(87, 4, 3, 0.33),
(88, 4, 4, 0.33),
(89, 4, 5, 0.33),
(90, 4, 6, 0.33),
(91, 4, 7, 0.33),
(92, 4, 8, 0.33),
(93, 4, 9, 0.33),
(94, 4, 10, 0.33),
(95, 4, 11, 0.33),
(96, 4, 12, 0.33);

-- --------------------------------------------------------

--
-- Table structure for table `theme`
--

CREATE TABLE `theme` (
  `id` int(11) NOT NULL,
  `nom` text NOT NULL,
  `img_link` text,
  `description` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `theme`
--

INSERT INTO `theme` (`id`, `nom`, `img_link`, `description`) VALUES
(1, 'Architecture', '/public/img/themes/architecture.png', 'LEGO® Architecture présente des constructions architecturales fantastiques du monde entier. Des bâtiments célèbres aux plus originaux, ces ensembles ajoutent un côté décalé aux maisons et aux bureaux.'),
(2, 'City', '/public/img/themes/city.png', 'LEGO® City reproduit tous les éléments que ton enfant voit tous les jours et en fait des modèles qui lui permettent de créer une ville pleine d\'action, d\'humour et de charme.'),
(3, 'Classic', '/public/img/themes/classic.png', 'LEGO® Classic aide les enfants à découvrir leurs talents de construction créative. Et comme la gamme couvre autant de tranches d\'âge, toute la famille peut s\'amuser !'),
(4, 'Creator 3-in-1', '/public/img/themes/creator.png', 'La série LEGO® Creator permet à ton enfant d\'expérimenter avec des maisons, des voitures, des avions et des animaux. Avec les ensembles LEGO Creator 3-en-1, ton enfant a le choix entre 3 constructions incroyables pour encore plus de jeu et d\'amusement.'),
(5, 'Ideas', '/public/img/themes/ideas.png', 'Les fans LEGO ont inspiré et soutenu les produits LEGO® Ideas ! Les ensembles ont été conçus avec la passion d\'un véritable constructeur !');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `boite`
--
ALTER TABLE `boite`
  ADD PRIMARY KEY (`id`),
  ADD KEY `theme_id` (`theme`);

--
-- Indexes for table `couleur`
--
ALTER TABLE `couleur`
  ADD PRIMARY KEY (`ref_color`);

--
-- Indexes for table `liste_brique`
--
ALTER TABLE `liste_brique`
  ADD KEY `boite_ref` (`boite_id`),
  ADD KEY `piece_ref` (`piece_id`) USING BTREE;

--
-- Indexes for table `pieces`
--
ALTER TABLE `pieces`
  ADD PRIMARY KEY (`id`),
  ADD KEY `couleur` (`couleur`),
  ADD KEY `taille` (`taille`);

--
-- Indexes for table `taille`
--
ALTER TABLE `taille`
  ADD PRIMARY KEY (`ref_size`) USING BTREE;

--
-- Indexes for table `theme`
--
ALTER TABLE `theme`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `boite`
--
ALTER TABLE `boite`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `couleur`
--
ALTER TABLE `couleur`
  MODIFY `ref_color` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;

--
-- AUTO_INCREMENT for table `pieces`
--
ALTER TABLE `pieces`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `taille`
--
ALTER TABLE `taille`
  MODIFY `ref_size` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=97;

--
-- AUTO_INCREMENT for table `theme`
--
ALTER TABLE `theme`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `boite`
--
ALTER TABLE `boite`
  ADD CONSTRAINT `theme_id` FOREIGN KEY (`theme`) REFERENCES `theme` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `liste_brique`
--
ALTER TABLE `liste_brique`
  ADD CONSTRAINT `boite_ref` FOREIGN KEY (`boite_id`) REFERENCES `boite` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `brique_ref` FOREIGN KEY (`piece_id`) REFERENCES `pieces` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `pieces`
--
ALTER TABLE `pieces`
  ADD CONSTRAINT `pieces_ibfk_1` FOREIGN KEY (`couleur`) REFERENCES `couleur` (`ref_color`),
  ADD CONSTRAINT `pieces_ibfk_2` FOREIGN KEY (`taille`) REFERENCES `taille` (`ref_size`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
