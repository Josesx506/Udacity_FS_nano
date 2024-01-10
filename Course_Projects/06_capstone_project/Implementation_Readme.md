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

<br><br>

### Merging multiple flask apps
After the project, I learnt you can register different python scripts as mini-flask apps with `Flask Blueprint`. In other words, you don't have to write all your endpoints in one infinite app file. You can create multiple files for each page, and register then within the main app. An example is shown below. <br>
- `appointments.py` file
    ```python
    from flask import Blueprint

    # Create the sub-app
    appts_bp = Blueprint('appts', __name__)

    @appts.route('/appointments')
    def get_appointments():
        pass
    ```
- `app.py` file
    ```python
    from flask import FLASK
    from appointments import appts_bp

    def create_app(test_config=None, db_name=db_name):
        # create and configure the app
        app = Flask(__name__, template_folder='templates/')
        
        # Register the mini-app within the main app
        app.register_blueprint(appts_bp, url_prefix='/')

        @app.route('/')
        def index():
            pass
        
        return app
    
    if __name__ == '__main__':
        app: Flask = create_app()
        app.run(host='0.0.0.0', port=8080, debug=True)
    ```

With this setup, you can access the `/appointments` endpoint whenever the main app is lainched. This means you code blocks can be broken into smaller segments for each page, and a single file can be used to link everything.

<br>

### Deployment Details
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

<br>

#### Remote deployment to AWS
- [x] First step I tried with AWS was to use CloudFormation to create CodePipeline resources for CI-CD. 
    - I just couldn't get the EKS EC2 instances and RDS DBs to share the same VPC so I let it go after 24 hours.
- [x] Create a [default VPC](https://docs.aws.amazon.com/vpc/latest/userguide/default-vpc.html#create-default-vpc) if you dont have one. It is required for connecting the instances.
- [x] Create a key pair from the [EC2 key-pair](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/create-key-pairs.html) page.Be careful about the region when creating key-pairs, my default region was `us-east-2`. Change the region to your default region. You'll need the key-pair to login to your instance.
- [x] I proceeded to manually create the EC2 Instance and RDS DB using information from (here)[https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/TUT_WebAppWithRDS.html].
    - Set a database username and password if you  prefer
- [x] Both the EC2 and RDS instances **MUST** share the same virtual private cloud (VPC) unless they won't work.
- [x] After linking both instances. Log in to the EC2 instance using ssh and the key-pair file
    ```bash
    # Example of `instance-public-dns-name` is 3.139.74.135
    # The `instance-user-name` is ec2-user
    ~$ssh -i path-to-key-pair-file.pem instance-user-name@$instance-public-dns-name
    ```
- [x] Once you're logged in, install required dependencies like psql,git,python, and docker
    ```bash
    ~$sudo dnf update -y 
    ~$sudo dnf install postgresql 
    ~$sudo dnf install git 
    ~$sudo dnf install python
    ~$sudo dnf install docker
    # If docker has any permission issues when trying to launch it, run the command below to fix it
    ~$sudo chmod 666 /var/run/docker.sock
    ```
- [x] Connect to the RDS DB from the EC2.
    ```bash
    # Example of `db-instance-endpoint` is salon-database.cjiasyzzf8nn.us-east-2.rds.amazonaws.com
    # This is a replacement for local host in the database path
    # I used the default port of `5432` and default username of `postgres` when creating the db
    # The default dbname is `postgres`. You can enter your password after running this line.
    ~$psql --host=db-instance-endpoint --port=5432 --dbname=postgres --username=postgres
    ```
- [x] Once you've tested that the psql server is running, clone the git repository and create an environment file. If you need help setting up git credentials, checkout this [video](https://www.youtube.com/watch?v=2K_-EQ-7vdc).
    ```bash
    # Clone repo
    ~$git clone git@github.com:Josesx506/Joses_FSND_Capstone.git
    # Create python environment and install requirements
    ~$python -m venv capstoneenv
    ~$source capstoneenv/bin/activate
    ~$pip install -r requirements.txt
    ```
- [x] Copy the RDS DB host endpoint into your .env file and prevent the file from being uploaded to git in the `.gitignore` file. Change the database path in your models.py file to 
    ```python
    database_path = f'postgresql://{DB_USER}:{DB_PASSWORD}@{RDS_HOST_ADDRESS}:{RDS_SQL_PORT}/{database_filename}'
    ```
- [x] Launch the gunicorn server with **Docker** and expose a port to your EC2 instance, I exposed port **2020**.
    ```bash
    # Create the docker image. 
    ~$docker build -t capstoneimage .
    # Launch the container. The docker file will launch the gunicorn server and start the app
    ~$docker run --detach --name capstoneContainer --env-file=.docker_env -p 2020:8080 capstoneimage
    ```
- [x] Navigate back to your [EC2 web-console](https://console.aws.amazon.com/ec2/), click on the active instance, and select the **security group**.
    - Change the inbound rules of the security group to allow traffic from port **2020**.
    - Each time your EC2 instance restarts, the public IP changes and you'll have to change your ssh config etc. To prevent this, use an Elastic IP address.
- [x] Navigate to the **EC2 web-console/Network & Security/Elastic IPs** service. Create a new elastic IP and associate it with active EC2 instance. Now your public address is fixed.
- [x] Change the allowed login, callback, and logout addresses in your Auth0 service to the new Elastic IP.
- [x] You app is live and you can go ahead to assign a free domain name if you want. For this app, the base url address is `http://3.23.56.12:2020/home`.