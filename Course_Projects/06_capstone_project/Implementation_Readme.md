### DB Migration
- Multiple columns were modified after creating the initial db warranting db migration.
- Raw SQL was used to update empty columns before migrating db and changing Nullable to False.
    ```psql
    # Update the db 
    UPDATE "Bookings" SET user_id='demo' WHERE user_id IS NULL;
    UPDATE "Stylists" SET user_id='demo' WHERE user_id IS NULL;
    UPDATE "Stylists" SET salon_role='Stylist' WHERE salon_role IS NULL;
    UPDATE "Stylists" SET bio='Lorem ipsum dolor sit amet consectetur adipisicing elit. Excepturi nostrum voluptas repudiandae consequatur animi eos natus laudantium deserunt enim. Accusantium perferendis eaque neque reprehenderit magni dolore molestiae. Officiis, impedit. Labore.' WHERE id=1;
    ```

<br><br>

### Auth0 Checks
- [x] Set up Auth0 Service and APIs
- [x] Set up API permissions with RBAC
- [x] Create Roles and Permissions
- [x] Assign user roles after signup manually (This can be automated in login flow to provide a default user role).
    - [x] Modify the [login flow](https://auth0.com/docs/customize/actions/flows-and-triggers/login-flow#add-user-roles-to-id-and-access-tokens) in **`Auth0 actions`** using instructions from [here](https://www.youtube.com/watch?v=CZxfMD8lXg8).
    - [ ] Automatically assign user roles for default user upon signup
- [x] Include the following lines in your environment file. You can generate a string for `LOCAL_SECRET_KEY` using o`penssl rand -hex 32` from your terminal.
    ```bash
    ~ $export CLIENT_ID='AUTH0-CLIENT-ID'
    ~ $export CLIENT_SECRET='AUTH0-CLIENT-SECRET'
    ~ $export AUTH0_DOMAIN='**********.auth0.com'
    ~ $export AUTH0_ALGORITHMS='*******'
    ~ $export AUTH0__AUDIENCE='********'
    ~ $export LOCAL_SECRET_KEY='*********'
    ```
- [x] Instead of using `response.headers['Authorization']`, I used [authlib to access Auth0](https://developer.auth0.com/resources/guides/web-app/flask/basic-authentication#configure-flask-with-auth-0) to create access-tokens that were saved in flask session cookies. This simplified obtaining and decoding the tokens required to verify **user permissions**.
    - Other [useful resources](https://auth0.com/docs/quickstart/webapp/python/interactive) for Auth0 integration with flask.
    - Another technique to obtain user permissions with Auth0 can be found [here](https://auth0.com/docs/quickstart/backend/python/interactive).
    - Secure user sessions could not be created for unittests, so I modified the `get_auth_token()` function in `backend/auth/auth.py` to work with flask sessions and authorization headers. This allowed the same function to be used for production and testing simultaneously
- [x] Because **`user roles`** are also specified, they can be used to verify actions like deleting booking actions for individuals vs. admins.
- [x] All user sessions are closed upon logout.

<br><br>

### Authentication files
- Flask Blueprints were used to register an authentication app ('auth') for Auth0 integration.
- auth.views is used to create and authenticate login and callback endpoints, open secure user sessions, as well as close user sessions upon logout.
- auth.auth is used to verify permissions in a user session. This wrapper is used to verify that a user has necessary permissions before secured endpoints can be accessed.

<br><br>

### Unittests
- All test files are saved in the `backend/tests` folder.
- A `base_setup.py` file was used to create the unittest setup and tear down process.
- A `populate_test_db.py` file is used to populate the sqllite db during the setup process so the endpoint requests don't return empty
- DB tests are performed with the `test_db_models.py` file
- Endpoint tests are in the main `test_app.py` file.

<br><br>

**PS**: After creating the production db, dummy entries can be created with the `backend/01_insert_single_db_entry.py` file.

### Creating a frontend
I tried creating a React App unsuccessfully because React works well with using proxy servers for the front end i.e. You can run a backend flask app on one ip address and use a different ip address for the frontend server. <br>
Unfortunately my knowledge of frontend is limited to HTML, CSS, and JS, so I reverted to using flask templates. I had a lot of fun using JS and I intend to use it more in the future. I also had some fun using Jinja, its way simpler than JS but doesn't work on prexisting web-templates like evo-calendar. I used pagination to load pages in batches, and Jinja/js to restrict front end display depending on RBAC permissions. <br>
Here are some things I learnt while trying to create the react app that might be useful in the future.
#### Create a React app
1. The name of the app is frontend - `npx create-react-app booking_app`
2. Open the `package.json` file to configure the proxy that will enable communication between the frontend and backend
    - Insert this new line intot the package.json file to tell it where the backend server is hosted `"proxy": "http://127.0.0.1:5000",`. I inserted this at line 5.
    - Change the react version lines to support revo-calendar
        ```json
        "react": "^17.0.1",
        "react-dom": "^17.0.1",
        ```
3. Open the `src/App.js` file and remove all the starter code. Install the [React Snippets](https://marketplace.visualstudio.com/items?itemName=dsznajder.es7-react-js-snippets) extension if you don't have it. Type `rfce` shortcut to create a new template.
4. Import `{useState, useEffect}` into the `src/App.js` file.
    - useState - is used to create a data route variable from the backend.
    - useEffect - is used to fetch the backend api on the first render.
highlight text and press Cmd+Shift+L to change all values that correspond to the text

    ```bash
    ~$npm show revo-calendar version

    ~$npm list -g
    ├── evo-calendar@1.1.2
    ├── express@4.18.2
    └── revo-calendar@3.2.3

    # I also tried other frontend servers without success. 
    ~$npm install -g live-server Install the server
    ~$live-server # Launch the server from terminal
    ```

    