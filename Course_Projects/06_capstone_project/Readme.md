

npm install -g nodemon # Install for node server
npm install express
npm install -g http-server

node server.js # Start node server

http-server src -p 3500

### Endpoints



### Auth0
- [x] Set up Auth0 Service and APIs
- [x] Set up API permissions with RBAC
- [x] Create Roles and Permissions
- [x] Assign user roles after signup
    - [x] Modify the [login flow](https://auth0.com/docs/customize/actions/flows-and-triggers/login-flow#add-user-roles-to-id-and-access-tokens) in **`Auth0 actions`** using instructions from [here](https://www.youtube.com/watch?v=CZxfMD8lXg8).
- [x] Include the following lines in your environment file
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
- [x] Because **`user roles`** are also specified, they can be used to verify actions like deleting booking actions for individuals vs. admins.
- [x] All user sessions are closed upon logout.

# --------------
npm install -g live-server Install the server
live-server # Launch the server from terminal


1. Add userId to the Bookings db column
2. Add user roles to event-container data.
3. Users will only be able to view events that were created by that user


### Create a React app
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

npm show revo-calendar version
├── evo-calendar@1.1.2
├── express@4.18.2
└── revo-calendar@3.2.3