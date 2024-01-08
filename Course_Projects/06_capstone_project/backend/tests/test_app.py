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

admin_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Iko5SUc1OUVxLVdNNHM3bmZJYzZpdiJ9.eyJjb2ZmZWVzaG9wLXVkeS1mc25kLnVzLmF1dGgwLmNvbS9yb2xlcyI6WyJTYWx\
vbkFkbWluIl0sImlzcyI6Imh0dHBzOi8vY29mZmVlc2hvcC11ZHktZnNuZC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjU5NmZkNWYwNWViYjk4YmExNTRkNjc3IiwiYXVkIjpbInNhbG9u\
IiwiaHR0cHM6Ly9jb2ZmZWVzaG9wLXVkeS1mc25kLnVzLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE3MDQ2Njk3NDcsImV4cCI6MTcwNDc1NjE0NywiYXpwIjoicm9PNWdhNE5VUFhtS\
HhLRE9qclkyN05iUGloR1dNd0siLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFkbWluYm9va2luZ3MiLCJkZWxldGU6Ym9va2luZ3\
MiLCJkZWxldGU6c2VydmljZXMiLCJkZWxldGU6c3R5bGlzdHMiLCJnZXQ6Ym9va2luZ3MiLCJnZXQ6c2VydmljZXMiLCJnZXQ6c3R5bGlzdHMiLCJwYXRjaDpib29raW5ncyIsIn\
Bvc3Q6Ym9va2luZ3MiLCJwb3N0OnNlcnZpY2VzIiwicG9zdDpzdHlsaXN0cyJdfQ.RSUo5OSkOT1e0cNuzEuVqYstWjWyxLibvgONj-v6xWBNE469mwxDXIPuupRiHEGqbai\
KqsvBpgi9oy_DMIezfirH3DQcCyjk4rWNrA7FOI1BSV2Qqg8QblPOv2Q7HUYVQl4fxW-ERpsAE7OT0TIR8oPQGDHESLkmOHGlwYBTlI0-r6DZh5UbrC3VvV9BjO1MAe\
u5EnKN0YIexChm1z1ls_C8JkWXnaUL55qsatOBU4yEfgaqDWxQGjbRkgS_mtxz3UK2UuWnZ8Hlc3Y4PDMLnY2LBK7Z_0BlCqKmtx0c-S8x0XQ77ZII6Ed-1wir\
h0woVoeNEaVct3EjqI1SkYwGyQ'

user_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Iko5SUc1OUVxLVdNNHM3bmZJYzZpdiJ9.eyJjb2ZmZWVzaG9wLXVkeS1mc25kLnVzLmF1dGgwLmNvbS9yb2xlcyI6WyJT\
YWxvblVzZXIiXSwiaXNzIjoiaHR0cHM6Ly9jb2ZmZWVzaG9wLXVkeS1mc25kLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NTk4NjM3OTQ4YjdiNmNhOWUzY2Q5NjEiLCJhdWQiOlsic2F\
sb24iLCJodHRwczovL2NvZmZlZXNob3AtdWR5LWZzbmQudXMuYXV0aDAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTcwNDY3MjI1MywiZXhwIjoxNzA0NzU4NjUzLCJhenAiOiJyb081Z2E0Tl\
VQWG1IeEtET2pyWTI3TmJQaWhHV013SyIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6Ym9va2luZ3MiLCJnZXQ6Ym9va2luZ3MiL\
CJnZXQ6c2VydmljZXMiLCJnZXQ6c3R5bGlzdHMiLCJwYXRjaDpib29raW5ncyIsInBvc3Q6Ym9va2luZ3MiXX0.BHf56ilB4tIjrP_MUVlwM6Y8bYgS4KKLdGJmyGZVXXsTZbp8\
LZhRXqwY-hYWHF7f0Ctxa54IKcJ51yEgoMQ2iOTKP4i9Tvz7et9v3HjXC4e5YhUPB2Ka09cfKgbKB27AASxOP2I72yBp3uCo8QCFk0qVDJ2HwIXYfYnhmEW9RBQ0iwry7md\
687o8XKiRVKwU_7BgSR43ri807ZK_6fEM6St28UH8difa21asiX6Tp_pQgJS7ttnmONR4FvS5IUVpNF7ckT_U-PMJwW2hQRJ3Ag98Ka2W8r5rodd7c1fm5kosD0IPnc\
tBPzzL0XzgRzMEOTTo6lnrqDXg_-VTthbatg'


from contextlib import contextmanager

@contextmanager
def captured_output():
    import sys
    from io import StringIO

    new_out, new_err = StringIO(), StringIO()
    old_out, old_err = sys.stdout, sys.stderr

    try:
        sys.stdout, sys.stderr = new_out, new_err
        yield sys.stdout, sys.stderr
    finally:
        sys.stdout, sys.stderr = old_out, old_err


class CapstoneEndpointsTestCase(TestSetup):
    '''
    This class is used to perform tests on the endpoints

    The first 3 tests are for endpoints that render flask html template filess
    '''
    
    # # -------------------------------- Render Template Endpoint Tests --------------------------------
    # def test_home_page_get_request(self):
    #     endpoint = "/home"
                
    #     response = self.client().get(endpoint)
    #     html_content = response.data.decode("utf-8")

    #     # Check if the response status code is 200 (OK)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTrue(html_content)
    

    # def test_stylist_page_get_request(self):
    #     endpoint = "/stylists"
        
    #     response = self.client().get(endpoint)
    #     html_content = response.data.decode("utf-8")

    #     # Check if the response status code is 200 (OK)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTrue(html_content)
    

    # def test_book_appointments_page_get_request(self):
    #     endpoint = "/appointments"
    #     response = self.client().get(endpoint)
    #     html_content = response.data.decode("utf-8")

    #     # Check if the response status code is 200 (OK)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTrue(html_content)

    # # -------------------------------- JSON response endpoint tests --------------------------------
        
    # # POST Stylist unittests
    # def test_200_post_new_stylist_as_admin(self):
    #     endpoint = '/stylists/create'
    #     header = {'Authorization': f'Bearer {admin_token}'}
    #     json_payload = self.stylist_entry

    #     response = self.client().post(endpoint, json=json_payload, headers=header)
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 200)
    #     self.assertTrue(data["stylist"])
    

    # def test_403_post_new_stylist_as_user(self):
    #     endpoint = '/stylists/create'
    #     header = {'Authorization': f'Bearer {user_token}'}
    #     json_payload = self.stylist_entry

    #     response = self.client().post(endpoint, json=json_payload, headers=header)
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 403)
    #     self.assertEqual(data["success"], False)
    #     self.assertEqual(data["message"], 'Permission not found.')
    

    # #  ----------------------------- Appointments unittests -----------------------------
        
    # # -------- GET REQUESTS --------
    # def test_200_get_appointments_as_guest(self):
    #     endpoint = '/appointments/refresh'

    #     response = self.client().get(endpoint)
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertTrue(data["booked_slots"])
    #     self.assertTrue(data["roles"])
    

    # def test_200_get_appointments_as_user(self):
    #     endpoint = '/appointments/refresh'
    #     header = {'Authorization': f'Bearer {user_token}'}

    #     response = self.client().get(endpoint, headers=header)
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertTrue(data["booked_slots"])
    #     self.assertTrue(data["roles"])
    

    # def test_200_get_appointments_as_admin(self):
    #     endpoint = '/appointments/refresh'
    #     header = {'Authorization': f'Bearer {admin_token}'}

    #     response = self.client().get(endpoint, headers=header)
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertTrue(data["booked_slots"])
    #     self.assertTrue(data["roles"])
    

    # -------- POST Requests --------
    # def test_200_post_new_booking_as_admin(self):
    #     '''
    #     This test confirms that an admin can create new events in the db. 
    #     It also checks that the returned test values correspond to the json payload posted
    #     '''
    #     endpoint = '/appointments/book'
    #     header = {'Authorization': f'Bearer {admin_token}'}
    #     json_payload = self.booking_entry_admin
        
    #     response = self.client().post(endpoint, json=json_payload, headers=header)
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertTrue(data["event"]) # Confirm an event was returned
    #     self.assertEqual(data["event"][0]['first_name'], self.booking_entry_admin['first']) # Confirm the returned event is corrent
    

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
    

    # def test_401_post_new_booking_without_authentication(self):
    #     '''
    #     This test confirms that a guest user cannot post to the db.
    #     I also tried using a random jwt token but I got a urlopen error.
    #     '''
    #     endpoint = '/appointments/book'
    #     json_payload = self.booking_entry_user
        
    #     response = self.client().post(endpoint, json=json_payload)
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 401)
    #     self.assertEqual(data["success"], False)
    #     self.assertEqual(data["message"], 'Verified user session is not identified or request header is invalid.')


    # # -------- PATCH Requests --------
    # def test_200_patch_existing_booking_as_admin(self):
    #     '''
    #     This test confirms that an admin can modify existing events in the db. 
    #     It also checks that the returned test values correspond to the json payload patched
    #     '''
    #     endpoint = '/appointments/book'
    #     header = {'Authorization': f'Bearer {admin_token}'}

    #     # Perform a db model query to get a random event
    #     query = Booking.query.all()
    #     fmt_query = [book.format() for book in query]
    #     patch_event = random.choice(fmt_query)
    #     patch_event_id = patch_event['id']
        
    #     # Change the names and datetime of the booking
    #     patch_event['first_name'] = self.booking_entry_admin['first']
    #     patch_event['last_name'] = self.booking_entry_admin['last']
    #     patch_event['start_time'] = datetime.now()

    #     # Create the new json payload
    #     json_payload = patch_event
        
    #     response = self.client().patch(f"{endpoint}/{patch_event_id}", json=json_payload, headers=header)
    #     data = json.loads(response.data)

    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(data["success"], True)
    #     self.assertTrue(data["event"]) # Confirm an event was returned
    #     self.assertEqual(data["event"][0]['first_name'], self.booking_entry_admin['first']) # Confirm the returned event is corrent




# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()