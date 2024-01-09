# Project Rubric Checklist
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
First test if you can access the endpoints locally within a docker container before deploying it remotely.

#### Containerize the app.
1. Add the `gunicorn` package to the requirements file
2. I wanted it to run on port :8080 for the gunicorn server, so I added :8080/callback to the Auth0 callback urls when running gunicorn on my local computer, and `/callback` when running gunicorn in docker.
3. Next step is to create a docker file in the root directory. The files are copied from t
    ```docker
    # Use the `python:3.7` as a source image from the Amazon ECR Public Gallery
    # We are not using `python:3.7.2-slim` from Dockerhub because it has put a  pull rate limit. 
    FROM public.ecr.aws/sam/build-python3.9:latest

    # Set up an app directory for your code and copy all the files in backend directory to docker
    COPY /backend /src
    # Change the workdir which is equivalent to `cd /src`
    WORKDIR /src

    # Install `pip` and needed Python packages from `requirements.txt`
    RUN pip install --upgrade pip
    RUN pip install -r requirements.txt

    # Define an entrypoint which will run the main app using the Gunicorn WSGI server.
    # The name of the file with the app is `app.py`, the name of the flask app variable is also `app`
    # Hence the `app:app` entrypoint. This is a gunicorn equivalent of flask run
    ENTRYPOINT ["gunicorn", "-b", ":8080", "app:app"]
    ```
4. Create a docker environment file `.docker_env`. This is used to set environment variables so that the env file is not copied into docker. <br>
    **NOTE**: variable names in the docker file should not be enclosed in quotes unlike the python environment files, and no spaces should be left between words e.g
    ```env
    AUTH0_ALGORITHMS=RS256
    AUTH0__AUDIENCE=salon
    ```
5. To create the docker image and run it locally. Note how the docker port 8080 is exposed to port 80 on localhost
    ```bash
    # Create the image
    ~$docker build -t capstoneimage .
    # Launch the container with the environmental file. 
    ~$docker run --detach --name capstoneContainer --env-file=.docker_env -p 80:8080 capstoneimage
    ```
6. Test the endpoints on your local computer using port 80 e.g `curl --request GET 'http://localhost:80/home'` returns the HTML of the homepage.
7. **Note**: the docker container `Base Image` doesn't have postgres installed and the db is not connected. Hence you will not be able to see items on the Book Appointments and Services page.
    - You can download a separate base image that has psql installed and link both containers together using `docker compose` but it wasn't a priority for me at the time of completion.
    - For the remote deployment on AWS, I used the `Amazon RDS DB` instance. Check the [link](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/TUT_WebAppWithRDS.html) for additional setup details.

#### Remote deployment to AWS
- [x] First step will be to install `awscli`, `eksctl`, and `kubectl` packages.
- [x] Remote deployment on AWS doesn't support using environment variables for docker/python. Instead, the environment variables are stored in `AWS Parameter Store`
    ```bash
    ~$aws ssm put-parameter --name JWT_SECRET --overwrite --value "myjwtsecret" --type SecureString
    # Verify
    ~$aws ssm get-parameter --name JWT_SECRET
    # Once you submit your project and receive the reviews, you can consider deleting the variable from parameter-store using:
    ~$aws ssm delete-parameter --name JWT_SECRET
    ```
- [x] The project is deployed on AWS (tentatively).

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