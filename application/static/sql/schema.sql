-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema TestDb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema TestDb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `TestDb` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `TestDb` ;

-- -----------------------------------------------------
-- Table `TestDb`.`User`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `TestDb`.`User` (
  `idUser` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `DOB` DATE NULL DEFAULT NULL,
  PRIMARY KEY (`idUser`))
ENGINE = InnoDB
AUTO_INCREMENT = 202
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `TestDb`.`Account`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `TestDb`.`Account` (
  `idAccount` INT NOT NULL AUTO_INCREMENT,
  `idUser` INT NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  `hashed_password` VARCHAR(225) NOT NULL,
  `created_at` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  `username` VARCHAR(50) NULL DEFAULT NULL,
  `Account_Type` ENUM('General', 'Student', 'Company') NOT NULL DEFAULT 'General',
  `profile_pic_url` VARCHAR(255) NULL DEFAULT NULL,
  `is_verified` TINYINT(1) NULL DEFAULT '0',
  PRIMARY KEY (`idAccount`),
  UNIQUE INDEX `email_accountType_UNIQUE` (`email` ASC, `Account_Type` ASC) VISIBLE,
  INDEX `FK_Account_User_idx` (`idUser` ASC) VISIBLE,
  CONSTRAINT `FK_Account_User`
    FOREIGN KEY (`idUser`)
    REFERENCES `TestDb`.`User` (`idUser`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
AUTO_INCREMENT = 198
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `TestDb`.`Admin`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `TestDb`.`Admin` (
  `idAccount` INT NOT NULL,
  `expire_at` DATE NULL DEFAULT NULL,
  PRIMARY KEY (`idAccount`),
  CONSTRAINT `FK_Admin_Account`
    FOREIGN KEY (`idAccount`)
    REFERENCES `TestDb`.`Account` (`idAccount`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `TestDb`.`Category`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `TestDb`.`Category` (
  `idCategory` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`idCategory`))
ENGINE = InnoDB
AUTO_INCREMENT = 10
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `TestDb`.`Company`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `TestDb`.`Company` (
  `idAccount` INT NOT NULL,
  `company_name` VARCHAR(100) NOT NULL,
  `website` VARCHAR(225) NULL DEFAULT NULL,
  `description` TEXT NULL DEFAULT NULL,
  PRIMARY KEY (`idAccount`),
  CONSTRAINT `FK_Company_Account`
    FOREIGN KEY (`idAccount`)
    REFERENCES `TestDb`.`Account` (`idAccount`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `TestDb`.`Tools`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `TestDb`.`Tools` (
  `idTool` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  `company` INT NULL DEFAULT NULL,
  `url` VARCHAR(255) NOT NULL,
  `timestamp` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  `thumbnail_url` TEXT NULL DEFAULT NULL,
  `published_date` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `version` FLOAT NULL DEFAULT NULL,
  `pricing` VARCHAR(70) NULL DEFAULT 'Free',
  `description` TEXT NULL DEFAULT NULL,
  PRIMARY KEY (`idTool`),
  INDEX `FK_Tools_Company` (`company` ASC) VISIBLE,
  FULLTEXT INDEX `title` (`name`) VISIBLE,
  CONSTRAINT `FK_Tools_Company`
    FOREIGN KEY (`company`)
    REFERENCES `TestDb`.`Company` (`idAccount`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
AUTO_INCREMENT = 194
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `TestDb`.`SearchIndex`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `TestDb`.`SearchIndex` (
  `idIndex` INT NOT NULL AUTO_INCREMENT,
  `idTool` INT NOT NULL,
  `idCategory` INT NOT NULL,
  `index_at` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`idIndex`),
  INDEX `FK_Index_Doc_idx` (`idTool` ASC) VISIBLE,
  INDEX `Fk_Index_Category_idx` (`idCategory` ASC) VISIBLE,
  CONSTRAINT `Fk_Index_Category`
    FOREIGN KEY (`idCategory`)
    REFERENCES `TestDb`.`Category` (`idCategory`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `FK_Index_Tool`
    FOREIGN KEY (`idTool`)
    REFERENCES `TestDb`.`Tools` (`idTool`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
AUTO_INCREMENT = 211
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `TestDb`.`Favorite`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `TestDb`.`Favorite` (
  `idFavorite` INT NOT NULL AUTO_INCREMENT,
  `idAccount` INT NOT NULL,
  `idIndex` INT NOT NULL,
  PRIMARY KEY (`idFavorite`),
  UNIQUE INDEX `unique_user_index` (`idAccount` ASC, `idIndex` ASC) VISIBLE,
  INDEX `FK_Favorite_User_idx` (`idAccount` ASC) VISIBLE,
  INDEX `FK_Favorite_Index_idx` (`idIndex` ASC) VISIBLE,
  CONSTRAINT `FK_Favorite_Account`
    FOREIGN KEY (`idAccount`)
    REFERENCES `TestDb`.`Account` (`idAccount`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `FK_Favorite_Index`
    FOREIGN KEY (`idIndex`)
    REFERENCES `TestDb`.`SearchIndex` (`idIndex`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
AUTO_INCREMENT = 44
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `TestDb`.`Platform`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `TestDb`.`Platform` (
  `idPlatform` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`idPlatform`))
ENGINE = InnoDB
AUTO_INCREMENT = 9
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `TestDb`.`IndexPlatform`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `TestDb`.`IndexPlatform` (
  `idIndex` INT NOT NULL,
  `idPlatform` INT NOT NULL,
  PRIMARY KEY (`idIndex`, `idPlatform`),
  INDEX `Fk_IndexPlatform_Platform_idx` (`idPlatform` ASC) VISIBLE,
  CONSTRAINT `FK_IndexPlatform_Index`
    FOREIGN KEY (`idIndex`)
    REFERENCES `TestDb`.`SearchIndex` (`idIndex`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `Fk_IndexPlatform_Platform`
    FOREIGN KEY (`idPlatform`)
    REFERENCES `TestDb`.`Platform` (`idPlatform`)
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `TestDb`.`Keywords`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `TestDb`.`Keywords` (
  `idKeywords` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`idKeywords`),
  FULLTEXT INDEX `name` (`name`) VISIBLE)
ENGINE = InnoDB
AUTO_INCREMENT = 566
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `TestDb`.`Keywords_Indexes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `TestDb`.`Keywords_Indexes` (
  `IndexID` INT NOT NULL,
  `keywordID` INT NOT NULL,
  PRIMARY KEY (`IndexID`, `keywordID`),
  INDEX `Fk_Indexes_idx` (`IndexID` ASC) VISIBLE,
  INDEX `FK_Keywords_idx` (`keywordID` ASC) VISIBLE,
  CONSTRAINT `Fk_Indexes`
    FOREIGN KEY (`IndexID`)
    REFERENCES `TestDb`.`SearchIndex` (`idIndex`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `FK_Keywords`
    FOREIGN KEY (`keywordID`)
    REFERENCES `TestDb`.`Keywords` (`idKeywords`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `TestDb`.`Rating`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `TestDb`.`Rating` (
  `idRating` INT NOT NULL AUTO_INCREMENT,
  `rating` FLOAT NOT NULL,
  `idIndex` INT NOT NULL,
  `idAccount` INT NOT NULL,
  PRIMARY KEY (`idRating`),
  INDEX `FK_Rating_Account_idx` (`idAccount` ASC) VISIBLE,
  INDEX `FK_Rating_Index_idx` (`idIndex` ASC) VISIBLE,
  CONSTRAINT `FK_Rating_Account`
    FOREIGN KEY (`idAccount`)
    REFERENCES `TestDb`.`Account` (`idAccount`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `FK_Rating_Index`
    FOREIGN KEY (`idIndex`)
    REFERENCES `TestDb`.`SearchIndex` (`idIndex`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
AUTO_INCREMENT = 37
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `TestDb`.`Review`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `TestDb`.`Review` (
  `idReview` INT NOT NULL AUTO_INCREMENT,
  `review_text` LONGTEXT NOT NULL,
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `idAccount` INT NOT NULL,
  `idIndex` INT NOT NULL,
  PRIMARY KEY (`idReview`),
  INDEX `FK_Review_User_idx` (`idAccount` ASC) VISIBLE,
  INDEX `Fk_Review_Index_idx` (`idIndex` ASC) VISIBLE,
  CONSTRAINT `FK_Review_Account`
    FOREIGN KEY (`idAccount`)
    REFERENCES `TestDb`.`Account` (`idAccount`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `Fk_Review_Index`
    FOREIGN KEY (`idIndex`)
    REFERENCES `TestDb`.`SearchIndex` (`idIndex`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
AUTO_INCREMENT = 33
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `TestDb`.`Search_History`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `TestDb`.`Search_History` (
  `idSearch_History` INT NOT NULL AUTO_INCREMENT,
  `idAccount` INT NOT NULL,
  `query_text` VARCHAR(255) NULL DEFAULT NULL,
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`idSearch_History`),
  INDEX `FK_SearchHistory_Account_idx` (`idAccount` ASC) VISIBLE,
  CONSTRAINT `FK_SearchHistory_Account`
    FOREIGN KEY (`idAccount`)
    REFERENCES `TestDb`.`Account` (`idAccount`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
AUTO_INCREMENT = 767
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `TestDb`.`Student`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `TestDb`.`Student` (
  `idAccount` INT NOT NULL,
  `university` VARCHAR(100) NULL DEFAULT NULL,
  `major` VARCHAR(45) NULL DEFAULT NULL,
  `graduation_year` DATETIME NULL DEFAULT NULL,
  PRIMARY KEY (`idAccount`),
  CONSTRAINT `FK_Student_Account`
    FOREIGN KEY (`idAccount`)
    REFERENCES `TestDb`.`Account` (`idAccount`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `TestDb`.`User_Sessions`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `TestDb`.`User_Sessions` (
  `idUser_Sessions` INT NOT NULL AUTO_INCREMENT,
  `idAccount` INT NOT NULL,
  `start_time` TIMESTAMP NULL DEFAULT CURRENT_TIMESTAMP,
  `end_time` TIMESTAMP NULL DEFAULT NULL,
  PRIMARY KEY (`idUser_Sessions`),
  INDEX `FK_UserSession_Account_idx` (`idAccount` ASC) VISIBLE,
  CONSTRAINT `FK_UserSession_Account`
    FOREIGN KEY (`idAccount`)
    REFERENCES `TestDb`.`Account` (`idAccount`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
