CREATE TABLE category (
    categoryid INT(2) NOT NULL,
    name VARCHAR(50) NOT NULL,
    priority INT(2) NOT NULL,
    color VARCHAR(20),
    CONSTRAINT category_categoryid_pk PRIMARY KEY (categoryid)
);

CREATE TABLE task (
	taskid INT(2) NOT NULL,
	title VARCHAR(50) NOT NULL,
	details VARCHAR(500) NOT NULL,
	status BOOLEAN NOT NULL DEFAULT 0,
	duedate DATE,
    categoryid INT(2),
	CONSTRAINT task_taskid_pk PRIMARY KEY(taskid),
    CONSTRAINT task_categoryid_fk FOREIGN KEY(categoryid) REFERENCES category(categoryid)
);