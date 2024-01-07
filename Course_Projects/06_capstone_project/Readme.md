

npm install -g nodemon # Install for node server
npm install express
npm install -g http-server

node server.js # Start node server

http-server src -p 3500

PostgreSQL was used to create the app locally but sqlite was used to run unittests

### Models
1. `Bookings` - Main model to manage appointments. Contains the columns below
    - [x] id - for primary key
    - [x] name, phone, email
    - [x] time - for when the appointment will be completed
    - [x] completed - checkbox for stylist who attended to customer
    - [x] stylist_id - stylist who completed service. One-to-many relationship with `Stylists` model.
    - [x] user_id - unique user id for managing access and Auth0 verification
2. `Stylists` - Main model to describe employee details and services offered. Contains the columns below
    - [x] id - for primary key
    - [x] name, phone, email
    - [x] skills - an array of services offered
    - [x] image_link - url where profile picture is present
    - [x] user_id - unique user id for managing access and Auth0 verification
3. `Services` - Main model for services offered. Contains the columns below
    - [x] id - for primary key
    - [x] name, price, duration and image_link
    - [x] It should contain a many-to-many relationship with `Stylists` but I didn't spend much time on it.


### Endpoints
1. `/appointments` - Main endpoint for booking appointments however, it only renders the template. I minimized Jinja usage for this because the `evo-Calendar` api came with its methods that restricted Jinja maipulation.
    | Request Type | Endpoint | Description | Secured Endpoint |
    | :----------- | :------- | :---------- | :--------------: |
    | GET | `/appointments/refresh` | View all booked appointments | [ ] |
    | GET | `/appointments/<date>` | Check available timeslots before redering future booking times | [ ] |
    | POST | `/appointments/book` | Book an appointment | [x] |
    | PATCH | `/appointments/book/<int:b_id>` | Update an existing appointment | [x] |
    | DELETE | `/appointments/book/<int:b_id>` | Delete an existing appointment | [x] |
2. `/stylists` - Main endpoint for salon employees. Typically renders information in a grid with pagination, however, Admins can perform additional actions on secured endpoints.

<br>

### Roles and Permissions
- Create three major **ROLES** and one guest role
    1. `SalonAdmin` - Capable of managing all stylists, services, and appointments. Can create, edit, and delete stylists, services, and appointment bookings.
    2. `SalonStylist` - Capable of managing all appointments. Can create, edit, and delete appointment bookings.
    3. `SalonUser` - Capable of managing **only** appointments that are created by them. Can view other appointment timeslots but cannot modify them.
    4. `Guest` - Can access unsecured endpoints to view bookings, services, and stylists.
- Here's a table of all **PERMISSIONS** used. 
    Two types of delete permissions were created. Admin delete is used for stylists and services while regular delete is used by all roles. I could have created additional patch roles but I focused on mainly the appointments page for this project.
    | GET | PATCH | POST | DELETE |
    | :-: | :---: | :--: | :----: |
    | `get:bookings` | `patch:bookings` | `post:bookings` | `delete:bookings` |
    | `get:stylists` |  | `post:stylists` | `delete:stylists` |
    | `get:services` |  | `post:services` | `delete:services` |
    |  |  |  | `delete:adminbookings` |



Update empty columns before migrating db
```psql
# Update the db 
UPDATE "Bookings" SET user_id='demo' WHERE user_id IS NULL;
UPDATE "Stylists" SET user_id='demo' WHERE user_id IS NULL;
UPDATE "Stylists" SET salon_role='Stylist' WHERE salon_role IS NULL;
UPDATE "Stylists" SET bio='Lorem ipsum dolor sit amet consectetur adipisicing elit. Excepturi nostrum voluptas repudiandae consequatur animi eos natus laudantium deserunt enim. Accusantium perferendis eaque neque reprehenderit magni dolore molestiae. Officiis, impedit. Labore.' WHERE id=1;
```


## Files
### Authentication files
auth.views is used to create and authenticate login and callback endpoints, open secure user sessions, as well as close user sessions upon logout.
auth.auth is used to verify permissions in a user session. This wrapper is used to verify that a user has necessary permissions before secured endpoints can be accessed.


### Auth0 Checks
- [x] Set up Auth0 Service and APIs
- [x] Set up API permissions with RBAC
- [x] Create Roles and Permissions
- [x] Assign user roles after signup manually (This can be automated in login flow to provide a default user role).
    - [x] Modify the [login flow](https://auth0.com/docs/customize/actions/flows-and-triggers/login-flow#add-user-roles-to-id-and-access-tokens) in **`Auth0 actions`** using instructions from [here](https://www.youtube.com/watch?v=CZxfMD8lXg8).
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
- [x] Because **`user roles`** are also specified, they can be used to verify actions like deleting booking actions for individuals vs. admins.
- [x] All user sessions are closed upon logout.


<!-- {% if event.user_id == user_id %}
    <button onclick="deleteEvent({{ event.id }})">Delete</button>
{% endif %} -->


# --------------
npm install -g live-server Install the server
live-server # Launch the server from terminal



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



// Assuming you have a common ancestor element that contains all the delete buttons
// Replace "commonAncestor" with the actual parent element that holds the delete buttons
// var commonAncestor = document;
// commonAncestor.addEventListener('click', function(event) {
//     // Check if the clicked element has the class "deleteEventButtons"
//     if (event.target.classList.contains('deleteEventButtons')) {
//         // Retrieve the event index from the data attribute
//         var eventId = event.target.dataset.eventIndex;

//         // Perform your delete request using the eventId
//         // Example: You can use fetch to send a DELETE request to your server
//         fetch(`/delete-event/${eventId}`, {
//             method: 'DELETE',
//             // Additional options if needed (headers, body, etc.)
//         })
//         .then(response => {
//             if (response.ok) {
//                 // Successful delete, you may want to update the UI accordingly
//                 console.log(`Event ${eventId} deleted successfully.`);
//             } else {
//                 // Handle errors if needed
//                 console.error(`Failed to delete event ${eventId}.`);
//             }
//         })
//         .catch(error => {
//             console.error('Error during delete request:', error);
//         });
//     }
// });

// Place holder event for tests
var today = new Date();

var events = [{
    id: "imwyx6S",
    name: "Event #3",
    description: "Lorem ipsum dolor sit amet.",
    date: today.getMonth() + 1 + "/18/" + today.getFullYear(),
    type: "event"
}]