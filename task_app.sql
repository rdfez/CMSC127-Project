CREATE TABLE category (
    categoryid INT(2) NOT NULL,
    cname VARCHAR(50) NOT NULL,
    priority VARCHAR(6) NOT NULL,
    color VARCHAR(20),
    PRIMARY KEY (categoryid)
);

CREATE TABLE task (
    taskid INT(2) NOT NULL,
    title VARCHAR(50) NOT NULL,
    details VARCHAR(500) NOT NULL,
    status VARCHAR(11) NOT NULL DEFAULT "not started",
    duedate DATE,
    categoryid INT(2),
    PRIMARY KEY (taskid),
    CONSTRAINT task_categoryid_fk FOREIGN KEY (categoryid) REFERENCES category (categoryid)
);

--Add category
INSERT INTO category VALUES (1, "Acad-related", "Urgent", "Pink"), (2, "Org-related", "High", "Violet"), (3, "Movies to watch", "Low", "Orange"), (4, "Personal", "Normal", "Yellow");

--Add/Create Task
INSERT INTO task VALUES (01, "CMSC 127 Exercise 1", "ER Model/EER Model", "not started", "2022-05-30", 1), (02, "CMSC 131 Exercise 1", "Basic Arithmetics", "not started", "2022-05-22", NULL), (03, "CMSC 131 Quiz 1", "Basic Arithmetics", "not started", "2022-05-22", 1);

--Edit Task
UPDATE task SET status = "in progress" WHERE taskid = 01;

--Delete Task
DELETE FROM task WHERE title = "CMSC 127 Exercise 1";

--View Task
SELECT taskid, title, details, status, duedate FROM task WHERE status = "in progress";

--View All Tasks 
SELECT taskid, title, details, status, duedate FROM task;

--Mark Task as Done
UPDATE task SET status = "done" WHERE title = "CMSC 131 Quiz 1";

--Edit category
UPDATE category SET cname="Acads" WHERE cname="Acad-related";

--Delete category
DELETE FROM category WHERE categoryid IN (2, 3);

--View category
SELECT * FROM category WHERE cname="Personal";

--Add a task to category
UPDATE task SET categoryid=1 WHERE title="CMSC 131 Exercise 1";

--View task per day
SELECT * FROM task WHERE duedate = "2022-05-22";

--View task per month
SELECT * FROM task WHERE MONTH(duedate) = 5;
