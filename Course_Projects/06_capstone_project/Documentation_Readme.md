# API Documentation
### Introduction
The Salon API is organized around REST. Our API accepts form-encoded request bodies and returns json-encoded responses. It also uses standard HTTP response codes and verbs. <br>
The Salon api allows users to view and create appointments on a calendar. The calendar frontend is modified from [evo-calendar](https://edlynvillegas.github.io/evo-calendar/), and we allow role-based access control (RBAC) operations on top for our users.

### Getting Started
- Base URL: This app can be run locally at `http://127.0.0.1/5000` and it will be deployed on AWS. The backend app uses flask and the frontend is rendered with HTML templates.
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
#### Retrieve All Stylists and Booked appointmentmets
- **GET /stylists**
    - Arguments
        - base_url (*required*) <br><br>
    - Example
        - `curl http://127.0.0.1:5000/stylists` <br><br>
    - Returns: A html page of all the stylists employed by the salon.
    - No permissions are required
    - Roles - None


<br><br>

export TOKEN=`curl --data '{"email":"salonadmin@myhair.com","password":"DFnMq8Xa5HAgACP"}' --header "Content-Type: application/json" -X POST 127.0.0.1:5000/auth  | jq -r '.token'`
echo $TOKEN

var today = new Date();

var events = [{
    id: "imwyx6S",
    name: "Event #3",
    description: "Lorem ipsum dolor sit amet.",
    date: today.getMonth() + 1 + "/18/" + today.getFullYear(),
    type: "event"
}]
