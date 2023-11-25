### Database Migrations
Migrations help us to modify existing databases with deleting the old data. New columns can be added or dropped and the changes can be rolled back if the applications break. Other benefits of migration are that they:
- encapsulate a set of changes to our database schema, made over time.
- are uniquely named
- are usually stored as local files in our project repo, e.g. a `migrations/` folder
- There should be a 1-1 mapping between the changes made to our database, and the *migration files* that exist in our `migrations/` folder.
- Our migrations files set up the tables for our database.
- All changes made to our DB should exist physically as part of migration files in our repository.

#### Migration command-line scripts
There are generally 3 scripts needed, for
- **migrate**: creating a migration script template to fill out; generating a migration file based on changes to be made
- **upgrade**: applying migrations that hadn't been applied yet ("upgrading" our database)
- **downgrade**: rolling back applied migrations that were problematic ("downgrading" our database)

<br>

- **Flask-Migrate** (flask_migrate)is a python library that is used as migration manager for migrating SQLALchemy-based database changes.
- **Flask-Script** (flask_script) lets us run migration scripts we defined, from the terminal

#### Steps to get migrations going
1. Initialize the migration repository structure for storing migrations by running `flask db init`
    - **Note**: If the flask app script is not nmaed `app.py`, you might get the following error *Error: Could not locate a Flask application. Use the 'flask --app' option, 'FLASK_APP' environment variable, or a 'wsgi.py' or 'app.py' file in the current directory*. To fix it, specify the name of the app with `FLASK_APP=01_add_comp_col.py flask db init`.
    - This creates a `migration/` folder in your app directory.
2. Create a migration script (using Flask-Migrate).
    - You can delete the old *udacity_test* db with `dropdb udacity_test` to enable flask-migrate to track changes from the beginning of our workflow. You can reset the postgre server if an existing connections error pops up.
    - Create a clean db for this exercise with `createdb udacity_test`, then run `flask db migrate` in terminal to track changes being made to the db. Use `FLASK_APP=01_add_comp_col.py flask db migrate` if the script name is not app.py.
    - It creates a python script under the `migrate/versions/` folder as a *'revision_id.py'* file. This function contains two functions `upgrade()` and `downgrade()` that can be used to restore the database to the revision_id state in a safe manner. It's very similar to a git commit id. It also creates an **alembic_version** table that holds our db changes and should not be modified
3. (Manually) Run the migration script (using Flask-Script)
    - To upgrade the db, run `flask db upgrade` and to downgrade it, run `flask db downgrade`. Don't forget to include the flask app name.
    - You can also manually alter the revision_id.py scripts and add sql commands if any manual updates were made directly using psql (This is not recommended). e.g. 
    ```python
    # Assuming we manually added rows to the persons in psql after running flask db.rollback().
    # If we try to execute flask db upgrade, we'll get an error except we manually update the upgrade function
    def upgrade():
        '......'
        op.execute('UPDATE persons SET height = 10.0 WHERE height IS NULL')
        op.alter_column('persons', 'height')
    ```
    - After updating the script, `flask db upgrade` can be run successfully.