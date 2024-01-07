from datetime import datetime
import os
import sys
import unittest

# Append the current directory
sys.path.append("..")
sys.path.append(os.getcwd())


# Import db model dependencies and test initialization class
from models import db, Booking, Stylist
from base_setup import TestSetup



class CapstoneDBModelsTestCase(TestSetup):
    '''
    This class is used to perform tests of CRUD operations on the db model
    These first two tests are important so the db is not empty when doing Endpoint tests
    '''
    
    # ---------------------------------------- Model Tests ----------------------------------------
    # json.dumps(my_dictionary, indent=4, sort_keys=True, default=str)
    
    def test_create_booking_appointment(self):
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
    

    def test_create_stylist_entity(self):
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



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()