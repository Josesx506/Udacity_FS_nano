from datetime import datetime
import json
import os
import random
import sys
import unittest

# Append the current directory
sys.path.append("..")
sys.path.append(os.getcwd())


# Import db model dependencies and test initialization class
from models import db, Booking, Stylist
from base_setup import TestSetup
from settings import CUSTOMER_USER_ID,ADMIN_TOKEN,USER_TOKEN

# Extract the tokens at the top of the file
admin_token = ADMIN_TOKEN
user_token = USER_TOKEN



class CapstoneEndpointsTestCase(TestSetup):
    '''
    This class is used to perform tests on the endpoints

    The first 3 tests are for endpoints that render flask html template files.
    The next 2 tests are for POST requests on the Stylist Endpoint.
    The next 3 tests are for GET requests to the Appointments Endpoint
    The next 3 tests are for PATCH requests to the Appointments Endpoint
    The next 3 tests are for DELETE requests to the Appointments Endpoint
    The last 2 tests are for Errors validation to the Appointments Endpoint

    # The script can be executed with 
    ~$source ../../.env
    ~$python -m unittest -v test_app.py 
    '''
    
    # -------------------------------- Render Template Endpoint Tests --------------------------------
    def test_home_page_get_request(self):
        endpoint = "/home"
                
        response = self.client().get(endpoint)
        html_content = response.data.decode("utf-8")

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(html_content)
    

    def test_stylist_page_get_request(self):
        endpoint = "/stylists"
        
        response = self.client().get(endpoint)
        html_content = response.data.decode("utf-8")

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(html_content)
    

    def test_book_appointments_page_get_request(self):
        endpoint = "/appointments"
        response = self.client().get(endpoint)
        html_content = response.data.decode("utf-8")

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(html_content)

    # -------------------------------- JSON response endpoint tests --------------------------------
        
    # POST Stylist unittests
    def test_200_post_new_stylist_as_admin(self):
        endpoint = '/stylists/create'
        header = {'Authorization': f'Bearer {admin_token}'}
        json_payload = self.stylist_entry

        response = self.client().post(endpoint, json=json_payload, headers=header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data["stylist"])
    

    def test_403_post_new_stylist_as_user(self):
        endpoint = '/stylists/create'
        header = {'Authorization': f'Bearer {user_token}'}
        json_payload = self.stylist_entry

        response = self.client().post(endpoint, json=json_payload, headers=header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], 'Permission not found.')
    

    #  ----------------------------- Appointments unittests -----------------------------
        
    # -------- GET REQUESTS --------
    def test_200_get_appointments_as_guest(self):
        endpoint = '/appointments/refresh'

        response = self.client().get(endpoint)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["booked_slots"])
        self.assertTrue(data["roles"])
    

    def test_200_get_appointments_as_user(self):
        endpoint = '/appointments/refresh'
        header = {'Authorization': f'Bearer {user_token}'}

        response = self.client().get(endpoint, headers=header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["booked_slots"])
        self.assertTrue(data["roles"])
    

    def test_200_get_appointments_as_admin(self):
        endpoint = '/appointments/refresh'
        header = {'Authorization': f'Bearer {admin_token}'}

        response = self.client().get(endpoint, headers=header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["booked_slots"])
        self.assertTrue(data["roles"])

    # -------- POST Requests --------
    def test_200_post_new_booking_as_admin(self):
        '''
        This test confirms that an admin can create new events in the db. 
        It also checks that the returned test values correspond to the json payload posted
        '''
        endpoint = '/appointments/book'
        header = {'Authorization': f'Bearer {admin_token}'}
        json_payload = self.booking_entry_admin
        
        response = self.client().post(endpoint, json=json_payload, headers=header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["event"]) # Confirm an event was returned
        self.assertEqual(data["event"][0]['first_name'], self.booking_entry_admin['first']) # Confirm the returned event is corrent
    

    def test_200_post_new_booking_as_user(self):
        '''
        This test confirms that a registered user can create new events in the db. 
        It also checks that the returned json values correspond to the json payload posted
        '''
        endpoint = '/appointments/book'
        header = {'Authorization': f'Bearer {user_token}'}
        json_payload = self.booking_entry_user
        
        response = self.client().post(endpoint, json=json_payload, headers=header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["event"]) # Confirm an event was returned
        self.assertEqual(data["event"][0]['first_name'], self.booking_entry_user['first']) # Confirm the returned event is corrent
    

    def test_401_post_new_booking_without_authentication(self):
        '''
        This test confirms that a guest user cannot post to the db, even if bogus permissions and jwts are provided.
        I also tried using a random jwt token but I got a urlopen error.
        '''
        endpoint = '/appointments/book'
        json_payload = self.booking_entry_user
        header = {'Authorization': f'Bearer {self.randomJWToken()}'}
        
        response = self.client().post(endpoint, json=json_payload, headers=header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Authorization malformed 4. This token dies not have a valid `kid`")


    # -------- PATCH Requests --------
    def test_200_patch_existing_booking_as_admin(self):
        '''
        This test confirms that an admin can modify existing events in the db. 
        It also checks that the returned test values correspond to the json payload patched
        '''
        endpoint = '/appointments/book'
        header = {'Authorization': f'Bearer {admin_token}'}

        # Perform a db model query to get a random event
        query = Booking.query.all()
        fmt_query = [book.format() for book in query]
        patch_event = random.choice(fmt_query)
        patch_event_id = patch_event['id']
        
        # Change the names and datetime of the booking
        patch_event['first_name'] = self.booking_entry_admin['first']
        patch_event['last_name'] = self.booking_entry_admin['last']
        patch_event['start_time'] = datetime.now()

        # Create the new json payload
        json_payload = patch_event
        
        response = self.client().patch(f"{endpoint}/{patch_event_id}", json=json_payload, headers=header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["event"]) # Confirm an event was returned
        self.assertEqual(data["event"][0]['first_name'], self.booking_entry_admin['first']) # Confirm the returned event is corrent

    
    def test_200_patch_existing_user_booking_as_user(self):
        '''
        This test confirms that a user can ONLY modify existing events that they created in the db.
        Although they can see all the bookings, the user_id must match the one used to create an event before a
        user role can patch the event. To implement this, an initial post request is done, and then the 
        posted entry is patched. It also checks that the returned test values correspond to the json payload patched
        '''
        endpoint = '/appointments/book'
        header = {'Authorization': f'Bearer {user_token}'}

        # Implement the post request so the user has an entry that they created in the db
        post_payload = self.booking_entry_user
        post_response = self.client().post(endpoint, json=post_payload, headers=header)
        post_data = json.loads(post_response.data)

        # Perform a db model query to get the event that the user posted above
        query = Booking.query.all()
        fmt_query = [book.format() for book in query]
        patch_event = [user_event for user_event in fmt_query if user_event['user_id'] == CUSTOMER_USER_ID][0]
        patch_event_id = patch_event['id']
        
        # Change the names and datetime of the booking to that of the admin
        patch_event['first_name'] = self.booking_entry_admin['first']
        patch_event['last_name'] = self.booking_entry_admin['last']
        patch_event['start_time'] = datetime.now()

        # Create the new json payload
        json_payload = patch_event
        
        response = self.client().patch(f"{endpoint}/{patch_event_id}", json=json_payload, headers=header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["event"]) # Confirm an event was returned
        self.assertEqual(data["event"][0]['first_name'], self.booking_entry_admin['first']) # Confirm the returned event is corrent
    

    def test_422_patch_existing_non_user_booking_as_user(self):
        '''
        This test confirms that a user can ONLY modify existing events that they created in the db.
        A POST request is not done first and the user attempts to modify an event that they didn't create.
        It checks that the test fails.
        '''
        endpoint = '/appointments/book'
        header = {'Authorization': f'Bearer {user_token}'}

        # Perform a db model query to get a random event
        query = Booking.query.all()
        fmt_query = [book.format() for book in query]
        patch_event = random.choice(fmt_query)
        patch_event_id = patch_event['id']
        
        # Change the names and datetime of the booking to that of the admin
        patch_event['first_name'] = self.booking_entry_user['first']
        patch_event['last_name'] = self.booking_entry_user['last']
        patch_event['start_time'] = datetime.now()

        # Create the new json payload
        json_payload = patch_event
        
        response = self.client().patch(f"{endpoint}/{patch_event_id}", json=json_payload, headers=header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], 'unprocessable')


    # -------- DELETE Requests --------
    def test_200_delete_existing_booking_as_admin(self):
        '''
        This test confirms that an admin can delete any existing events in the db. 
        It also checks that the returned delete id corresponds to event id selected.
        '''
        endpoint = '/appointments/book'
        header = {'Authorization': f'Bearer {admin_token}'}

        # Perform a db model query to get a random event
        query = Booking.query.all()
        fmt_query = [book.format() for book in query]
        delete_event = random.choice(fmt_query)
        delete_event_id = delete_event['id']
        
        response = self.client().delete(f"{endpoint}/{delete_event_id}", headers=header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["delete"], delete_event_id) # Confirm the id of the event selected and the deleted event match
    

    def test_200_delete_existing_user_booking_as_user(self):
        '''
        This test confirms that a user can ONLY delete an existing event that they created in the db.
        An initial post request is done to make this test successful.
        It also checks that the returned delete id corresponds to event id selected.
        '''
        endpoint = '/appointments/book'
        header = {'Authorization': f'Bearer {user_token}'}

        # Implement the post request so the user has an entry that they created in the db
        post_payload = self.booking_entry_user
        post_response = self.client().post(endpoint, json=post_payload, headers=header)
        post_data = json.loads(post_response.data)

        # Perform a db model query to get the event that the user posted above
        query = Booking.query.all()
        fmt_query = [book.format() for book in query]
        delete_event = [user_event for user_event in fmt_query if user_event['user_id'] == CUSTOMER_USER_ID][0]
        delete_event_id = delete_event['id']

        response = self.client().delete(f"{endpoint}/{delete_event_id}", headers=header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["delete"], delete_event_id) # Confirm the id of the event selected and the deleted event match
    

    def test_422_delete_existing_non_user_booking_as_user(self):
        '''
        This test confirms that a user can ONLY delete an existing event that they created in the db.
        A POST request is not done first and the user attempts to delete an event that they didn't create.
        It checks that the test fails.
        '''
        endpoint = '/appointments/book'
        header = {'Authorization': f'Bearer {user_token}'}

        # Perform a db model query to get a random event
        query = Booking.query.all()
        fmt_query = [book.format() for book in query]
        delete_event = random.choice(fmt_query)
        delete_event_id = delete_event['id']

        response = self.client().delete(f"{endpoint}/{delete_event_id}", headers=header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], 'unprocessable')


    # -------- Error Tests --------
    def test_404_error_message_for_bad_delete_endpoint(self):
        '''
        This test confirms that a 404 error is returned if a delete id is not provided.
        '''
        endpoint = '/appointments/book/'
        header = {'Authorization': f'Bearer {admin_token}'}
        
        response = self.client().delete(endpoint, headers=header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], 'resource not found, booking/service/stylist not in the db')

    
    def test_422_error_message_for_invalid_delete_endpoint(self):
        '''
        This test confirms that a 422 error is returned if a delete id is not in the db.
        '''
        endpoint = '/appointments/book/422'
        header = {'Authorization': f'Bearer {admin_token}'}
        
        response = self.client().delete(endpoint, headers=header)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], 'unprocessable')



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()