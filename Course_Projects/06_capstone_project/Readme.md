# Project Rubric Checklist
This Readme is for the capstone project of my Udacity Fullstack developer nano-degreee. It integrates all the concepts learnt from previous nanodegree projects including database migration, REST apis, RBAC, authorization and deployment. For this project, I built a salon booking app where users can sign up and book appointments. CRUD functions were implemented and endpoints were secured using roles and permissions. The backend was developed with flask, and the front end was developed with flask templates.
<br>

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
    - [x] bio - an description of services offered
    - [x] salon_role - role of the stylist in the salon
    - [x] image_link - url where profile picture is present
    - [x] user_id - unique user id for managing access and Auth0 verification
3. `Services` - Main model for services offered. Contains the columns below
    - [x] id - for primary key
    - [x] name, price, duration and image_link
    - [x] It should contain a many-to-many relationship with `Stylists` but I didn't spend much time on it.
    - [x] Nothing was done for this table because I met the project requirements with the two tables above
<br><br>

### API Architecture and Testing
#### Endpoints
1. `/appointments` - Main endpoint for booking appointments however, it only renders the template. I minimized Jinja usage for this because the `evo-Calendar` api came with its methods that restricted Jinja maipulation.
    | Request Type | Endpoint | Description | Secured Endpoint |
    | :----------- | :------- | :---------- | :--------------: |
    | GET | `/appointments/refresh` | View all booked appointments | [ ] |
    | GET | `/appointments/<date>` | Check available timeslots before redering future booking times | [ ] |
    | POST | `/appointments/book` | Book an appointment | [x] |
    | PATCH | `/appointments/book/<int:b_id>` | Update an existing appointment | [x] |
    | DELETE | `/appointments/book/<int:b_id>` | Delete an existing appointment | [x] |

2. `/stylists` - Main endpoint for salon employees. Typically renders information in a grid with pagination, however, Admins can perform additional actions on secured endpoints.
    | Request Type | Endpoint | Description | Secured Endpoint |
    | :----------- | :------- | :---------- | :--------------: |
    | GET | `/stylists` | View all stylists employed in salon | [ ] |
    | POST | `/stylists/create` | Create a new stylist profile | [x] |

    Buttons for PATCH and DELETE requests were created but endpoints were not developed due to time constraints
<br>

#### Unit tests
1. Always **source the `.env`** before running any unittests to avoid the urllib error. It cost me 2 hours of lost time.
    - An .env file will be provided in the submission for evaluation purposes
2. Testing db is created with `SQLLite`. Production db is created with `PostgresSQL` or `AWS RDS`.
3. Tests are performed with the `unittest` library on endpoints to validate authentication, errors, and endpoint behaviours.
    - [x] DB migration tests were implemented.
    - [x] Includes three different roles that have distinct permissions for actions. Check out permissions in [RBAC](#roles-and-permissions) section.
    - [x] Includes at least one test for expected success and error behavior for each endpoint using the unittest library
    - [x] Includes tests demonstrating role-based access control, at least two per role. The SalonStylist role was not tested because it behaves very similar to the Admin role with the exception that it cannot modify Stylist profiles.
    - [x] User roles affect visible buttons on the frontend, and are secured with permissions and jwts on the backend.

<br><br>

### Roles and Permissions
- [x] Third-Party authentication with Auth0
- Create three major **ROLES** and one guest role
    1. `SalonAdmin` - Capable of managing all stylists, services, and appointments. Can create, edit, and delete stylists, services, and appointment bookings.
    2. `SalonStylist` - Capable of managing all appointments. Can create, edit, and delete appointment bookings.
    3. `SalonUser` - Capable of managing **only** appointments that are created by them. Can view other appointment timeslots but cannot modify them.
    4. `Guest` - Can access all unsecured endpoints to view bookings, services, and stylists.
- Here's a table of all **PERMISSIONS** used. 
    Two types of delete permissions were created. Admin delete is used for stylists and services while regular delete is used by all roles. I could have created additional patch roles but I focused on mainly the appointments page for this project.
    | GET | PATCH | POST | DELETE |
    | :-: | :---: | :--: | :----: |
    | `get:bookings` | `patch:bookings` | `post:bookings` | `delete:bookings` |
    | `get:stylists` |  | `post:stylists` | `delete:stylists` |
    | `get:services` |  | `post:services` | `delete:services` |
    |  |  |  | `delete:adminbookings` |

<br><br>

### Deployment
- [x] The app was containerized with Docker and deployed on AWS using EC2, RDS, and Elastic IP services. The baseurl can be accessed here `http://3.23.56.12:2020/home`.
    - Additional details on the deployment can be [read here](./Implementation_Readme.md#deployment-details).

<br><br>

### Code Quality & Documentation
- [x] The Project uses REST API and the api documentation is in a separate readme [HERE](./Documentation_Readme.md).
- [x] Variable names are logical, code is DRY and well-commented where code complexity makes them useful
- [x] Requirements file is provided in `backend/requirements.txt` to enable recreation of virtual environment. This allows the application to run with no errors and respond with expected results.
- [x] Unittests were used to confirm endpoints and RBAC behavior.
- [x] Secrets are stored as environment variables (except the tokens in the test file. They expire anyway and I wouldn't include them in live projects).

<br><br>

### Suggestions to Make Your Project Stand Out
- [x] Create a frontend that works with your API - including a login that will redirect the user to Auth0. Let your work come to life on the screen!!
- [ ] Implement authorization with a tool other than email or Google. Add more options for your users’ authentication flow.
- [x] Deploy your application and database on AWS. 