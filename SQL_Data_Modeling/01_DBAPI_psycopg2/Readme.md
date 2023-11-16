### psycopg2 overview
This python package allows you to connect to a Postgre SQL (psql) server and execute queries directly in python. <br>
1. You'll need to create the database first. After installing psql, run `createdb <db_name>` in terminal to create the database, following which you can connect with the psql or pscopg2.
2. You can check whether the database was created by running `psql <db_name>` in terminal.
3. After logging into psql, you can use `\l` to list all your existing databases and see if the db was created. For this exercises, I named my db **udacity_test**.
4. You'll have to manually open connections, perform transactions, and close them out manually, which can make it hard to scale to web development. 
<br><br>
psycopg2 is a Database API (DBAPI) that is good if you want to write low-level SQL but it easily inflates the workload.