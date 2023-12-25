## All Projects Description

### Fyurr
Designed artist management system where users could add artists, venues, and shows. This project introduced db creation, db versioning, Create-Read-Update-Delete (CRUD), and Model-View-Controller (MVC) design. Backend was developed using Flask and PostgreSQL. Front end was implemented by **rendering** template HTML files with flask, and dynamically updating them with Jinja2, flask forms, and JS. Key learnings were 
- [x] Database creation and versioning
- [x] Flask app setup
- [x] Performing CRUD on DB
- [x] Using asynchronous requests to update webpage views.
The tools utilized include:
    ```bash
    .
    ├── Backend
    │   ├── Flask (local server)
    │   ├── Flask-SQLAlchemy (DB_ORM)
    │   ├── Flask-Migrate (DB_versioning)
    │   └── PostgreSQL (DB)
    └── Frontend
        ├── Bootstrap3
        ├── Flask-WTF (data handling, form validation, & error handling)
        ├── HTML & CSS (UI)
        └── JS (asynchronous requests)
    ```

### Trivia
Designed trivia game website where users could add questions to different categories and play trivia. This project introduced RESTful apis, api calls, error handling, api tests, and api documentation. Backend was developed using Flask and Flask-CORS. API tests were performed with curl and unittests. Frontend was designed with React. <br>
Unlike the first project, environment variables like the DB_NAME,USER, & PASSWORD were stored in a `.env` file for security reasons. Key learning were
- [x] Embedding flask apps within functions that can be imported into multiple scripts
- [x] Enforcing Cross-Origin Resource Sharing (CORS) within apps to limit the type of requests and urls that the apis respond to
- [x] Performing api tests to validate response of every successful/unsuccessful api requests
- [x] Creating PostgreSQL DBs with `.psql` scripts
The tools utilized include:
    ```bash
    .
    ├── Backend
    │   ├── curl (manual api tests in terminal)
    │   ├── dotenv (handling environment variables)
    │   ├── Flask (local server)
    │   ├── Flask-SQLAlchemy (DB_ORM)
    │   ├── Flask-CORS (Resource Sharing)
    │   ├── PostgreSQL (DB)
    │   └── Unittest (scripted api tests)
    └── Frontend
        ├── Nodejs 
        ├── Node Package Manager (npm)
        ├── HTML & CSS (UI)
        └── React and JS (asynchronous requests)
    ```

### Coffee Shop
Designed coffee shop website where different drink flavors could be added, and baristas serving in cafes could be managed. This project introduced authentication and website security. It highlighted some of the potential adversarial attacks (*cross site scripting and sql injection*) that can affect future projects and how to guard against them. Endpoints were secured using json web tokens (jwt) to restrict access and Auth0 was used to validate users. Backend was developed with flask and Auth0. API tests were performed with POSTMAN collections. Frontend was designed with ionic. <br>
Like the previous project, environment variables were stored in an environment file for security reasons. SQLite was used in the dev environment which didn't require a separate database script, and could be launched directly from python. Key learnings were
- [x] Introducing Authentication in CORS within app
- [x] Validating endpoints using jwts to restrict user access. E.g only Managers can create new coffee drinks while baristas can only view existing drinks
- [x] Performing integration and unit tests for api with POSTMAN
- [x] Creating development database with `SQLite`.
- [x] Test code review on git to restrict access during dev.
    ```bash
    .
    ├── Backend
    │   ├── dotenv (handling environment variables)
    │   ├── Flask (local server)
    │   ├── Flask-SQLAlchemy (DB_ORM)
    │   ├── Flask-CORS (Resource Sharing)
    │   ├── SQLite (DB)
    │   └── POSTMAN (scripted api tests)
    └── Frontend
        ├── Node Package Manager (npm)
        ├── Ionic (includes HTML & CSS (UI))
        │   └── Creates forms with tags for updating db 
        └── Angular, JS and TS (asynchronous requests for backend)
    ```

### JWT Kubernetes
Designed the backend for a simple flask app that had only 3 endpoints. The first endpoint was a GET request to check that the backend server was active. The second endpoint allowed the user to encode an email and password pair and generate jwts. The last endpoint allowed decoding of the previously encoded token. `gunicorn` was used as the production server instead of flask. No frontend architecture was developed, and all endpoints had to be queried with `curl`. The project was focused on deploying the flask app to AWS EKS with the aid of containers, kubernetes and AWS services. Key learnings were
- [x] Containerizing applications with docker
- [x] Managing users, roles, and permissions with AWS web console
- [x] Using AWS cli to create, populate, empty and delete S3 buckets.
- [x] Using `eksctl` to create kubernetes clusters, node groups, and load balancers
    - [x] Using `kubectl` to manage existing aws services like assessing the health of nodes and updating authentication.
- [x] Using template configuration `.yaml` files to create AWS stacks which include EC2 instances, IAM roles, lambda functions, S3 buckets, and VPCs.
- [x] Creating environment variables within AWS Parameter Store instead of using local environment variables.
- [x] Linking multiple AWS services to create **automatic pipelines** that source code from Git repos/S3 buckets, build the code and start servers, perform unit tests, and expose API endpoints.

    ```bash
    .
    ├── curl (manual api tests in terminal)
    ├── docker (container for packaging application)
    ├── flask (development server)
    ├── gunicorn (production server)
    ├── github (repo for code pipeline)
    ├── kubernetes (automatic load balancing)
    └── Multiple AWS services (notably EKS, CodeBuild, CodePipeline)
    ```

### Deployment
Basics of configuring and deploying apps to Heroku and Render cloud platforms.