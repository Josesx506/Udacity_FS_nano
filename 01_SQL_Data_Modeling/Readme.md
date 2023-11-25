## SQL Data Modeling Requirements
SQL - Structured Query Language <br>
### Installing PostgreSQL on mac
1. Local Postgres installation - Download a suitable version up to v12.x.x. [https://www.postgresql.org/download/]
2. Install Postgre with the install manager. On my mac, it installed it into the `/Library/PostgreSQL/12` directory.
3. During installation, you can set a port and password for the database as desired.
4. Post-installation, add the dependencies libraries to your bash profile by copying this command `export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/Library/PostgreSQL/12/lib` to the `/Library/PostgreSQL/12/pg_env.sh` file. This is only mentioned in manual's post-installation setup instructions.
4. After installing on a mac, run the the following commands in terminal to add the file paths to your bash_profile and launch the server with the `psql` command. 
```bash
~$ sh ~/Library/PostgreSQL/12/pg_env.sh 
~$ source ~/.bash_profile
~$ psql
```
5. It shoudl prompt you to enter a passord and the terminal should show
```bash
~$ psql
Password for user postgres: 
psql (12.16)
Type "help" for help.

postgres=# 
```
6. At this point you can create a database and add tables.
7. You can also view your connection info like port and username with the ` \conninfo` command in postgres
<br><br>

### Testing SQL synthax online
Use this two websites to test sql code interactively online. Make sure to save it or copy the commands to a git repo else you lose your progress if the page reloads
- [http://sqlfiddle.com/#!15]
- [https://www.db-fiddle.com/]
<br><br>

### Creating your first database (DB's can be created in terminal or psql)
1. After instaling sql, you can create your first table `create <dbname>` in terminal
2. You can access the db with `psql <dbname> <username>`, or delete it with `dropdb <dbname>`. The username does not need to be explicitly included for local tests and can be omitted.

#### Database Tables Key Description
<u><b>Primary Key (PK):</b></u> is a unique column in a particular table. It is commonly the first column in our tables in most databases and can be named "id".

<u><b>Foreign Key (FK):</b></u> is a column in one table that is a primary key in a different table. 
<br><br>

### Popular SQL commands
- CREATE | DROP | SELECT | FROM | LIMIT | JOIN
- 'Wildcats' in sql can be accessed with `LIKE` e.g. 
```sql
SELECT * FROM web_events_full WHERE referrer_url LIKE '%google%';
```

The communication protocol used to send and receive data over the internet is TCP/IP. It is an abbreviation that refers to  two main protocols
    - Transmission Control Protocol (TCP) and 
    - Internet Protocol (IP)
Port 80 is responsible for HTTP requests. Port 5432 is the default port for Postgres and most databases. The higher the number of TCP connections open on a server, the worse the performance issues.

Flask-SQLAlchemy 3.1.1