## SQL Data Modeling Requirements

### Installing PostgreSQL on mac
1. Local Postgres installation - Download a suitable version up to v12.x.x. [https://www.postgresql.org/download/]
2. Install Postgre with the install manager. On my mac, it installed it into the `/Library/PostgreSQL/12` directory.
3. During installation, you can set a port and password for the database as desired.
4. Post-installation, add the dependencies libraries to your bash profile by copying this command `export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/Library/PostgreSQL/12/lib` to the `/Library/PostgreSQL/12/pg_env.sh` file. This is only mentioned in manual's post-installation setup instructions.
4. After installing on a mac, run the the following commands in terminal to add the file paths to your bash_profile and launch the server with the `psql` command. 
```bash
~ $sh ~/Library/PostgreSQL/12/pg_env.sh 
~ $source ~/.bash_profile
~ $psql
```
5. It shoudl prompt you to enter a passord and the terminal should show
```bash
~ $psql
Password for user postgres: 
psql (12.16)
Type "help" for help.

postgres=# 
```
6. At this point you can create a database and add tables.


### Testing SQL synthax online
Use this two websites to test sql code interactively online. Make sure to save it or copy the commands to a git repo else you lose your progress if the page reloads
- [http://sqlfiddle.com/#!15]
- [https://www.db-fiddle.com/]


### Creating your first database
1. After launching sql, you can create your first table