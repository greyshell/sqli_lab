# author: greyshell
# description: truncate tables
# usage: mysql -u root --password=<pass> < clean_tbl.sql
# lab: sqli

# scenario-1 SELECT query: clear all user comments
# DELETE FROM vulnapp.tbl_post01;

# scenario-2: clear all posts, not created by 'asinha'
DELETE FROM vulnapp.tbl_post02 WHERE user NOT LIKE 'asinha%';

# scenario-3: clear all posts, created by default anonymous user
DELETE FROM vulnapp.tbl_post03 WHERE user LIKE 'anonymous-%';

# scenario-3: reset to the default settings
UPDATE vulnapp.tbl_post03 SET age = 19, comment = 'wipro technologies', city = 'santa clara' WHERE user = 'admin';