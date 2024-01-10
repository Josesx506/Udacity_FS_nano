# API Documentation
### Introduction
The Salon API is organized around REST. Our API accepts form-encoded request bodies and returns json-encoded responses. It also uses standard HTTP response codes and verbs. <br>
The Salon api allows users to view and create appointments on a calendar. The calendar frontend is modified from [evo-calendar](https://edlynvillegas.github.io/evo-calendar/), and we allow role-based access control (RBAC) operations on top for our users.

### Getting Started
- Base URL: This app can be run locally at `http://3.23.56.12:2020` and it will be deployed on AWS. The backend app uses flask and the frontend is rendered with HTML templates.
- Authentication: Authentication is performed using Auth0. Bearer tokens are used to validate api requests obtain access to secured endpoints. Users can sign up using the login page.

### Errors
The Salon api uses conventional HTTP response [codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status#redirection_messages) to indicate the success or failure of an API request. Errors are returned as json objects. Codes in the `2.x.x` range indicate success. Codes in the `4.x.x` range indicate an error from the request body.

#### Attributes
**success** *string* <br>
The status of the error as a boolean. This can be True or False. <br>

**error** int <br>
This indicates the HTTP error status code. It is usually in the `2.x.x` and `4.x.x` range. <br>

**message** *string* <br>
The error description returned as a string An example is `unprocessable`. <br><br>

<table>
    <thead>
        <tr>
            <th colspan=2 style="text-align: center;">HTTP STATUS CODE SUMMARY</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td style="text-align: right;"><b>200 - OK</b></td>
            <td style="text-align: left;">Request was successful, and the server has responded</td>
        </tr>
        <tr>
            <td style="text-align: right;"><b>400 - Bad request</b></td>
            <td style="text-align: left;">The request cannot be processed because required fields are missing</td>
        </tr>
        <tr>
            <td style="text-align: right;"><b>401 - Unauthorized</b></td>
            <td style="text-align: left;">The client must authenticate itself to get the requested response</td>
        </tr>
        <tr>
            <td style="text-align: right;"><b>403 - Forbidden</b></td>
            <td style="text-align: left;">A known client's identity is forbidden from performing unauthorized actions</td>
        </tr>
        <tr>
            <td style="text-align: right;"><b>404 - Resource not found</b></td>
            <td style="text-align: left;">The requested result doesn't exist</td>
        </tr>
        <tr>
            <td style="text-align: right;"><b>422 - Unprocessable</b></td>
            <td style="text-align: left;">The server understands the content type but it is unable to process the request.</td>
        </tr>
    </tbody>
</table>

<br>

### Resource Endpoint Library
- **GET /stylists** - Retrieve All Stylists
    - Arguments
        - base_url (*required*)
    - Example
        - `curl http://3.23.56.12:2020/stylists`
    - Returns: A html page of all the stylists employed by the salon.
    - No permissions are required
    - Roles - None
 <br><br>

- **POST /stylists/create** - Create a new stylist profile
    - Arguments
        - base_url (*required*)
    - Example
        ```bash
        ~$curl -H "'Authorization': 'Bearer ACCESS_TOKEN' " -d "{'stylist_name': 'Lauren Ipsita', 'phone': '+4494040912', 'email': 'stylist4@luxehair.com', \
        'stylist_salon_role': 'Stylist','bio': 'Lorem Ipsum dumdum', 'img_link': 'https:image.com/7384.jpg'}" -X POST http://3.23.56.12:2020/stylists/create
        ```
    - Returns: A json payload of success and the serialized json of the new stylist profile
        ```bash
        {
            'success': True,
            'stylist': [{
                'bio': 'Lorem Ipsum dumdum',
                'email': 'stylist4@luxehair.com',
                'image_link': 'https:image.com/7384.jpg',
                'name': 'Lauren Ipsita',
                'phone': '+4494040912',
                'salon_role': 'Stylist',
                'user_id': 'adsdss9182'
            }]
        }
        
        ```
    - `post:stylists` permission required
    - Roles - Admin
 <br><br>

- **GET /appointments** - Retrieve All Bookings
    - Arguments
        - base_url (*required*)
    - Example
        - `curl http://3.23.56.12:2020/appointments` 
    - Returns: A paginated html page of all the bookings made with the salon.
    - No permissions are required
    - Roles - None
 <br><br>

- **POST /appointments/book** - Book a new appointment on the calendar
    - Arguments
        - base_url (*required*)
    - Example
        ```bash
        ~$curl  -H "'Authorization': 'Bearer ACCESS_TOKEN' " -d "{'first': 'Lauren', 'last': 'Ipsita', 'phone': '+4494040912', 'email': 'stylist4@luxehair.com', \
        'start_time': '01/11/2024 11:00 AM', 'completed': false} http://3.23.56.12:2020/appointments/book
        ```
    - Returns: A json payload with the newest event and success status
        ```bash
        {
            "event": [
                {
                "completed": false,
                "date": "01/01/2024",
                "description": "Time: 11:00 AM\t Name: Lauren Ipsita",
                "email": "jugu@gmail.com",
                "first_name": "Lauren",
                "last_name": "Ipsita",
                "name": "Hair Appointment",
                "phone": "+4494041098",
                "start_time": "01-01-2024 11:00 AM",
                "stylist_id": 1,
                "time": "11:00 AM",
                "type": "event",
                "user_id": "demo",
                "verified": false
                }],
            "success": true
        }
        ```
    - `post:bookings` permission required
    - Roles - `SalonAdmin` or `SalonUser`
<br><br>

- **PATCH /appointments/book/<int:booking_id>** - Edit an existing appointment on the calendar
    - Arguments
        - base_url (*required*)
    - Example
        ```bash
        ~$curl  -H "'Authorization': 'Bearer ACCESS_TOKEN' " -d "{'first': 'Larry', 'last': 'Ipsita'} http://3.23.56.12:2020/appointments/book/1
        ```
    - Returns: A json payload with the modified event and success status
        ```bash
        {
            "event": [
                {
                "completed": false,
                "date": "01/01/2024",
                "description": "Time: 11:00 AM\t Name: Larry Ipsita",
                "email": "jugu@gmail.com",
                "first_name": "Larry",
                "last_name": "Ipsita",
                "name": "Hair Appointment",
                "phone": "+4494041098",
                "start_time": "01-01-2024 11:00 AM",
                "stylist_id": 1,
                "time": "11:00 AM",
                "type": "event",
                "user_id": "demo",
                "verified": false
                }],
            "success": true
        }
        ```
    - `patch:bookings` permission required
    - Roles - `SalonAdmin` or `SalonUser`. 
        **Note**: Admins can modify any event, Users can only modify events that they create
<br><br>

- **DELETE /appointments/book/<int:booking_id>** - Delete an existing appointment on the calendar
    - Arguments
        - base_url (*required*)
    - Example
        ```bash
        ~$curl  -H "'Authorization': 'Bearer ACCESS_TOKEN' " http://3.23.56.12:2020/appointments/book/1
        ```
    - Returns: A json payload with the deleted event id and success status
        ```bash
        {
            "delete": 1,
            "success": true
        }
        ```
    - `delete:bookings` permission required
    - Roles - `SalonAdmin` or `SalonUser`. 
        **Note**: Admins can delete any event, Users can only delete events that they create
<br><br>