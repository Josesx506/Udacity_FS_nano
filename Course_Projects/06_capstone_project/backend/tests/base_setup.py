from datetime import datetime,timedelta
from jose import jwt
import os, shutil
import secrets
import sys
import unittest

# Append the directory above to enable imports
sys.path.append("..")

# Import app and model dependencies
from app import create_app
from models import db
from flask_migrate import init, migrate, upgrade
from populate_test_db import single_entry_db
from settings import AUTH0_DOMAIN


# SQLite creates a local db within this folder so only the name has to be specified
database_filename = 'Test_Capstone_DB.db'
project_dir = os.path.dirname(os.path.abspath(__file__))
database_path = "sqlite:///{}".format(os.path.join(project_dir, database_filename))


class TestSetup(unittest.TestCase):
    '''This class is used to perform tests'''

    def setUp(self):
        self.app = create_app(test_config=True, db_name=database_path)
        self.client = self.app.test_client
        
        # Test to confirm that the route names for each endpoint is within the app
        # for rule in self.app.url_map.iter_rules():
        #     print(f"Route names: {rule.rule} | Function name: {rule.endpoint}()\n")
        #     print('\n\n\n\n\n')

        # Perform the db migration programmatically instead of using `db.create_all()`
        init()
        migrate()
        upgrade()
        print('\n\n----------- Completed DB Migration -----------\n\n\n\n')

        # Populate the test db with some demo values
        single_entry_db()

        # Create entries that can be used to test user permissions
        self.stylist_entry = {
            'stylist_name': 'Test stylist',
            'phone': '+244545556',
            'email': 'stylisttest@luxehair.com',
            'stylist_salon_role': 'Stylist / Make up artist',
            'bio': 'This is the test stylist',
            'img_link': 'https://st5.depositphotos.com/2783505/66161/i/450/depositphotos_661619094-stock-photo-passport-photo-serious-young-adult.jpg'}
        
        self.booking_entry_admin = {
            'first':'Barista',
            'last':'fyurr',
            'phone': '+345465677766',
            'email': 'testbookingadmin@unittest.com',
            'date_time': datetime.now()
        }

        self.booking_entry_user = {
            'first':'Trivia',
            'last':'coffee',
            'phone': '+38473784342',
            'email': 'testbookinguser@unittest.com',
            'date_time': datetime.now()
        }


    def randomJWToken(self):
        # Secret key to sign the token
        secret_key = secrets.token_hex(32)

        # Payload data (you can customize this)
        payload = {
            'sub': 'user123',
            "iss": f"https://{AUTH0_DOMAIN}/",
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(minutes=5),
            'permissions': ['post:bookings','delete:bookings']
        }

        # Generate the JWT token
        token = jwt.encode(payload, secret_key, algorithm='HS256')

        return token


    def tearDown(self):
        db.session.remove()
        db.drop_all()
        # self.app.app_context().pop()

        # Remove the migrations folder and the sqlite db
        shutil.rmtree('migrations')
        os.remove(database_filename)
        if os.path.exists('__pycache__'):
            shutil.rmtree('__pycache__')
        os.system('clear')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()