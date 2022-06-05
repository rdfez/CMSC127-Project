DROP DATABASE IF EXISTS `task_app`;
CREATE DATABASE IF NOT EXISTS `task_app`;
USE `task_app`;

CREATE TABLE IF NOT EXISTS `category` (
    `categoryid` INT(2) NOT NULL,
    `cname` VARCHAR(50) NOT NULL,
    `priority` VARCHAR(6) NOT NULL,
    `color` VARCHAR(20) NOT NULL,
    PRIMARY KEY (`categoryid`)
);

CREATE TABLE IF NOT EXISTS `task` (
    `taskid` INT(2) NOT NULL,
    `title` VARCHAR(50) NOT NULL,
    `details` VARCHAR(500) NOT NULL,
    `status` VARCHAR(11) NOT NULL DEFAULT "not started",
    `duedate` DATE,
    `categoryid` INT(2),
    PRIMARY KEY (`taskid`),
    CONSTRAINT `task_categoryid_fk` FOREIGN KEY (`categoryid`) REFERENCES `category` (`categoryid`)
);

--Add categories
INSERT INTO `category` VALUES 
    (1, "Acad-related", "Urgent", "Green"), 
    (2, "Org-related", "High", "Blue"), 
    (3, "Movies to watch", "Low", "Cyan"), 
    (4, "Personal", "Medium", "Yellow");

--Add tasks
INSERT INTO `task` VALUES 
    (1, "CMSC 127 Exercise 1", "ER Model/EER Model", "Done", "2022-05-22", 1), 
    (2, "CMSC 131 Exercise 1", "GNU Debugger", "Done", "2022-05-22", 1), 
    (3, "CMSC 131 Exercise 2", "Basic Arithmetics Instructions", "Not started", "2022-05-22", 1),
    (4, "Laundry", "Wash stuff", "Not started", "2022-06-02", NULL),
    (5, "Publishing Materials", "Make pubmats for orientation", "In progress", "2022-06-28", 2),
    (6, "Shrektastic", "Watch the entire Shrek franchise", "In progress", NULL, 3),
    (7, "Fast and Furious", "Watch the entire F&F franchise", "In progress", "3013-01-28", 3),
    (8, "Garbodor", "Take the trash out", "Not started", NULL, NULL);
