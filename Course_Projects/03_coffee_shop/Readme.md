### Coffee Shop Implementation Checklist
Here are the lists of Todo Items I've completed. They were not completed sequentially but it helped me keep track. <br>

Note: all requests are handled within the *IONIC* frontend app.
- [x] Setup local python environment and installed all requirements.
- [x] Setup authorization domain for the app on auth0.com.
- [x] Setup environment variables in `backend/src/settings.py` and `.env`.
- [x] Setup functions to validate the json web tokens in `backend/src/auth/auth.py`
- [x] Setup the db functions to create the app in `backend/src/database/models.py`.
    - This was a SQLite db so I didn't have to create the db with a .psql script.
- [x] Setup the CORS app in `backend/src/api.py` script.
<br>

**Auth0 Todos**
- [x] Create a new authorization domain name.
- [x] Create new application with appropriate callback, login, and logout uris.
    - The callback url should end with `tabs/user-page` with a `http` protocol because the flask app is not using https.
- [x] Create new api with a specified audience name and user permissions.
- [x] Create different roles for *Administrator*, *Manager*, and *Barista*.
- [x] Include Auth0 credentials as environment variables for backend and load them with `backend/src/settings.py`.
    - Frontend environment variables are setup in an configuration file at `frontend/src/environments/environments.ts`
<br>

**Authorization Todos**
- [x] Create function to the `header` from each request.
- [x] Create function to check that each user has `permissions` in the header of each request.
- [x] Create function to decode and verify json web tokens (jwt) that exist in the request headers.
- [x] Create custom decorator for verifying user permissions that can be applied to any endpoint.
<br>

**Model Todos**
- [x] Setup custom database name within settings file that is hidden as environment variable for security purposes.
<br>

**POSTMAN Todos**
- [x] Implement GET request to obtains drinks and drink details for Baristas
- [x] Implement GET request to obtains drinks and drink details for Managers
- [x] Implement POST and PATCH requests to create and edit drinks in the db for Managers
- [x] Implement DELETE request to delete existing drinks from the db for Managers
- [x] Implement POST and PATCH requests to create and edit baristas in the db for Managers and Administrators
- [x] Implement DELETE request to delete existing baristas from the db for Managers and Administrators
- [x] All tests ran successfully in the collection and it was exported with an `backend/updated_*.json` prefix. Appropriate tokens were also included.
<br>

**Main API Todos**
- [x] Create the flask app and import all dependencies
- [x] Uncomment `db_drop_and_create_all()` the first time the app is run to create the local SQLite db. 
    - It is commented afterwards to prevent the app from deleting the db each time the app is restarted.
- [x] Create an endpoint to GET all the drinks in the db.
- [x] Create an endpoint to GET all the drinks detail in the db.
- The todo items here only works for the manager and administrator roles
    - [x] Create an endpoint to POST a new drink to the db.
    - [x] Create an endpoint to PATCH an existing drink to the db.
    - [x] Create an endpoint to DELETE an existing drink from the db.
<br>

**Above and Beyond Todos**
- [x] Barista access is limited (can do nothing)
- [x] Manager access is limited (can manage baristas)
- [x] Administrator access is limited (can manage baristas, managers)
- [x] Created a new tab for managing Baristas. This tab allows Managers/Administrators to
    - POST new baristas
    - PATCH existing baristas
    - DELETE existing baristas
    - Each Barista has an id, name, flavors of coffee (fixed list) they can prepare, and an image.
- [x] Created a new tab where administrators can manage Managers too but I didn't populate it.
    - It would have required a **cafe** table too where baristas will be linked to the cafes, managers will be linked to baristas, and admins will be linked to managers (probably something I can work on after the nano degree).
<br>

#### Install the environment
```bash
# Create the environment
~ $python -m venv coffeepy
~ $source coffeepy/bin/activate
~ $pip install -r backend/requirements.txt
# Assign the environment variables
~ $source .env
```
<br><br>

The main repo has a .gitignore file so I didn't include one in this folder. For security purposes, the environment variable files should not be tracked but I included them here to enable replication. <br><br>

You have to remove the venv and node_modules folder for the submission to go through unless the portal throws an error.