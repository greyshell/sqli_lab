# author: greyshell
# description: truncate tables
# usage: mysql -u root --password=<pass> < clean_tbl.sql
# lab: sqli

# scenario-1: clear all user comments
# DELETE FROM vulnapp.tbl_post01;

# case02: clear all posts, not created by 'asinha'
DELETE FROM vulnapp.tbl_post02 WHERE user NOT LIKE 'asinha%';

# case03: clear all posts, created by default anonymous user
DELETE FROM vulnapp.tbl_post03 WHERE user LIKE 'anonymous-%';

# case03: reset to the default settings
UPDATE vulnapp.tbl_post03 SET age = 19, comment = 'wipro technologies', city = 'santa clara' WHERE user = 'admin';