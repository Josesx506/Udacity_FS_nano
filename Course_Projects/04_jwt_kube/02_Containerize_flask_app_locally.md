The following steps describe how to complete the Dockerization part of the project. After you complete these steps, you should have the Flask application up and running in a Docker container. <br>

1. **Verify the Dockerfile** <br>
    Verify the Dockerfile to have the following content the in the app's home directory:
    ```bash
    # Use the `python:3.9` as a source image from the Amazon ECR Public Gallery, because I upgraded my local requirements file
    # We are not using `python:3.7.2-slim` from Dockerhub because it has put a  pull rate limit. 
    FROM public.ecr.aws/sam/build-python3.9:latest
    # Set up an app directory for your code
    COPY . /app
    WORKDIR /app
    # Install `pip` and needed Python packages from `requirements.txt`
    RUN pip install --upgrade pip
    RUN pip install -r requirements.txt
    # Define an entrypoint which will run the main app using the Gunicorn WSGI server.
    ENTRYPOINT ["gunicorn", "-b", ":8080", "main:APP"]
    ```
2. **Store Environment Variables** <br>
    Containers cannot read the values stored in your localhost's environment variables. Therefore, create a file named `.env_file` and save both `JWT_SECRET` and `LOG_LEVEL` into that `.env_file`. We will use this file while creating the container. Here, we do not need the `export` command, just an equals sign:
    ```bash
    JWT_SECRET='myjwtsecret'
    LOG_LEVEL=DEBUG
    ```
    This `.env_file` is only for the purposes of running the container locally, you do not want to push it into the Github or other public repositories. You can prevent this by adding it to your `.gitignore` file, which will cause git to ignore it. To safely store and use secrets in the cloud, use a secure solution such as AWS’s parameter store.
3. **Start the Docker Desktop service.**
4. **Build an image** <br>
    Build a local Docker image, by running the commands below from the directory where your Dockerfile resides:
    ```bash
    ~ $docker build -t myimage .
    # Other useful commands
    # Check the list of images
    ~ $docker image ls
    # Remove any image
    ~ $docker image rm <image_id>
    # View a summary of image vulnerabilities and recommendations → 
    ~ $docker scout quickview
    ```
5. **Create and run a container** <br>
    Create and run a container using the image locally:
    - You can pass the name of the env file using the flag <br>
        `--env-file=<YOUR_ENV_FILENAME>`.
    - You should expose the port 8080 of the container to port 80 on your host machine. <br>
    `~ $docker run --name myContainer --env-file=.env_file -p 80:8080 myimage`
    ```bash
    # Other useful commands
    # List running containers
    ~ $docker container ls
    ~ $docker ps
    # Stop a container
    ~ $docker container stop <container_id>
    # Remove a container
    ~ $docker container rm <container_id>
    ```
6. **Check the endpoints** <br>
    To use the endpoints, you can use the same curl commands as before, except using port 80 this time. Open a new terminal window, and try the following command:
    ```bash
    # Flask server running inside a container
    ~ $curl --request GET 'http://localhost:80/'
    # Flask server running locally (only the port number is different)
    ~ $curl --request GET 'http://localhost:8080/'
    ```
    or check http://localhost:80/ in the browser. You should see a "Healthy" response. For other two endpoints, try running the following commands:
    ```bash
    # Calls the endpoint 'localhost:80/auth' with the email/password as the message body. 
    # The return JWT token assigned to the environment variable 'TOKEN' 
    ~ $export TOKEN=`curl --data '{"email":"abc@xyz.com","password":"WindowsPwd"}' --header "Content-Type: application/json" -X POST localhost:80/auth  | jq -r '.token'`
    ~ $echo $TOKEN
    # Decrypt the token and returns its content
    ~ $curl --request GET 'http://localhost:80/contents' -H "Authorization: Bearer ${TOKEN}" | jq .
    ```