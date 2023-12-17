## All Projects Description

### Fyurr
Designed artist management system where users could add artists, venues, and shows. This project introduced db creation, db versioning, Create-Read-Update-Delete (CRUD), and Model-View-Controller (MVC) design. Backend was developed using Flask and PostgreSQL. Front end was implemented by **rendering** template HTML files with flask, and dynamically updating them with Jinja2, flask forms, and JS. Key learnings were 
- [x] Database creation and versioning
- [x] Flask app setup
- [x] Performing CRUD on DB
- [x] Using asynchronous requests to update webpage views.
The tools utilized include:
- ```bash
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
- ```bash
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




https://coffeeshop-udy-fsnd.us.auth0.com/authorize?audience=coffee&response_type=token&client_id=Rh1hjjexp2D0th7fcvjpc5ka2daoCAWp&redirect_uri=https://127.0.0.1:8100/login-results


