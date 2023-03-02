# author: greyshell
# description: drop all tables and db
# usage: mysql -u root --password=<pass> < drop_tbls.sql
# lab: sqli


# scenario-1:
DROP TABLE vulnapp.tbl_post01;

# scenario-2:
DROP TABLE vulnapp.tbl_post02;
DROP TABLE vulnapp.tbl_secret;

# scenario-3:
DROP TABLE vulnapp.tbl_post03;

DROP DATABASE vulnapp;