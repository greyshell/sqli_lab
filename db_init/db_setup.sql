# author: greyshell
# description: create db, tables and inset data
# usage: mysql -u root --password=<pass> < db_setup.sql
# lab: sqli


CREATE DATABASE IF NOT EXISTS vulnapp;

# case01:
CREATE TABLE IF NOT EXISTS vulnapp.tbl_post01 (
comment VARCHAR(100) NOT NULL,
user VARCHAR(10) NOT NULL
);


INSERT INTO vulnapp.tbl_post01 (comment, user) VALUES ('This is not a easy challange buddy', 'tom');
INSERT INTO vulnapp.tbl_post01 (comment, user) VALUES ('Brush up your fundamentals dude, before jump in', 'bob');
INSERT INTO vulnapp.tbl_post01 (comment, user) VALUES ('Take some rest man', 'mut');
INSERT INTO vulnapp.tbl_post01 (comment, user) VALUES ('Try harder sweety, if you are determined to know my password and token', 'admin');


# case02:
CREATE TABLE IF NOT EXISTS vulnapp.tbl_post02 (
comment VARCHAR(30) NOT NULL,
pin INT NOT NULL,
age INT NOT NULL,
user VARCHAR(30) NOT NULL
);

INSERT INTO vulnapp.tbl_post02 (comment, pin, age, user) VALUES ('I like heap', 100, 25, 'dhaval');

CREATE TABLE IF NOT EXISTS vulnapp.tbl_secret (
user VARCHAR(30) NOT NULL,
token INT NOT NULL,
password VARCHAR(30) NOT NULL
);

INSERT INTO vulnapp.tbl_secret (user, token, password) VALUES ('asinha', 777, 'itar@b3d');
INSERT INTO vulnapp.tbl_secret (user, token, password) VALUES ('admin', 101, 'grey@321');

# case03:
CREATE TABLE IF NOT EXISTS vulnapp.tbl_post03 (
comment VARCHAR(30) NOT NULL,
city VARCHAR(30) NOT NULL,
age INT NOT NULL,
user VARCHAR(30) NOT NULL,
PRIMARY KEY (user)
);

INSERT INTO vulnapp.tbl_post03 (comment, city, age, user) VALUES ('facebook', 'mountain view', 25, 'dhaval');
INSERT INTO vulnapp.tbl_post03 (comment, city, age, user) VALUES ('wipro technologies', 'santa clara', 19, 'admin');
INSERT INTO vulnapp.tbl_post03 (comment, city, age, user) VALUES ('splunk', 'gilroy', 19, 'asinha');