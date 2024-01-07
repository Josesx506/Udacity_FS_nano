from datetime import datetime
import json
import os, shutil
import sys
import unittest

# Append the current directory
sys.path.append("..")
sys.path.append(os.getcwd())


# Import dependencies
from app import create_app
from models import setup_db, db, Booking, Stylist
from flask_migrate import init, migrate, upgrade




# SQLite creates a local db within this folder so only the name has to be specified
database_filename = 'TEST_CAPSTONE_DB.db'
project_dir = os.path.dirname(os.path.abspath(__file__))
database_path = "sqlite:///{}".format(os.path.join(project_dir, database_filename))

# Note a valid token should be obtained FROM Auth0 and posted here "manually" before any tests are run 
VALID_TOKEN = ''


class CapstoneTestCase(unittest.TestCase):
    '''This class is used to perform tests'''

    def setUp(self):
        self.app = create_app(db_name=database_path)
        self.client = self.app.test_client
        # Perform the db migration programmatically instead of using `db.create_all()`
        init()
        migrate()
        upgrade()
        print('\n\n----------- Completed DB Migration -----------\n\n\n\n')
    
    
    # ---------------------------------------- Model Tests ----------------------------------------
    # These first two tests are important so the db is not empty when doing Endpoint tests
    # json.dumps(my_dictionary, indent=4, sort_keys=True, default=str)
    
    def test_createDemoBookingEntry(self):
        '''Create a simple Booking entry to the db and confirm that it can be retrieved'''

        event_1 =  Booking(first_name="Julius",
                      last_name='Agu',
                      phone='+4494041098',
                      email='jugu@gmail.com',
                      start_time=datetime(2023, 12, 1, 12, 0),
                      completed=True,
                      stylist_id=1,
                      user_id='demo')
        db.session.add(event_1)
        db.session.commit()

        # Perform query to retrieve the entry
        query = Booking.query.order_by(Booking.start_time).all()
        serialized_query = [appointment.format() for appointment in query]

        self.assertEqual(len(serialized_query), 1)
        self.assertTrue(serialized_query)
    

    def test_createDemoStylistEntry(self):
        '''Create a simple Stylist entry to the db and confirm that it can be retrieved'''

        stylist1 = Stylist(name="King Ella",
                      phone="+2275499450",
                      email="stylist1@luxehair.com",
                      salon_role='Stylist',
                      bio="Lorem ipsum dolor sit amet consectetur adipisicing elit. Excepturi nostrum voluptas repudiandae.",
                      image_link='https://pbs.twimg.com/media/DnZXDYyXcAYsPyj.jpg',
                      user_id='demo')
        db.session.add(stylist1)
        db.session.commit()

        # Perform query to retrieve the entry
        query = Stylist.query.order_by(Stylist.id).all()
        serialized_query = [person.format() for person in query]

        self.assertEqual(len(serialized_query), 1)
        self.assertTrue(serialized_query)
    
    
    # ---------------------------------------- Endpoint Tests ----------------------------------------


    def tearDown(self):
        db.session.remove()
        db.drop_all()

        # Remove the migrations folder and the sqlite db
        shutil.rmtree('migrations')
        os.remove(database_filename)
        os.system('clear')
        # self.app.app_context().pop()


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()