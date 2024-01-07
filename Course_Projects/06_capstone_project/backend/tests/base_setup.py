import os, shutil
import sys
import unittest

# Append the directory above to enable imports
sys.path.append("..")

# Import app and model dependencies
from app import create_app
from models import db
from flask_migrate import init, migrate, upgrade


# SQLite creates a local db within this folder so only the name has to be specified
database_filename = 'Test_Capstone_DB.db'
project_dir = os.path.dirname(os.path.abspath(__file__))
database_path = "sqlite:///{}".format(os.path.join(project_dir, database_filename))


class TestSetup(unittest.TestCase):
    '''This class is used to perform tests'''

    def setUp(self):
        self.app = create_app(db_name=database_path)
        self.client = self.app.test_client
        # self.app.app_context().push()
        # Perform the db migration programmatically instead of using `db.create_all()`
        init()
        migrate()
        upgrade()
        print('\n\n----------- Completed DB Migration -----------\n\n\n\n')
    

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        # self.app.app_context().pop()

        # Remove the migrations folder and the sqlite db
        shutil.rmtree('migrations')
        shutil.rmtree('__pycache__')
        os.remove(database_filename)
        os.system('clear')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()