## Containers
This chapter showed how to pull **Base images** from dockerhub to build local/cloud apps. This base images come with pre-installed dependencies that serve as the building block for additional app development. Specific images pulled were for `psql` and `python` which allowed me to launch psql and create local flask apps with docker. <br>

The chapter also showed how to write local **Dockerfiles**, convert them to **images**, and run the images as **containers**. The chapter also showed how to **shut down** containers and **delete** temporary containers and images. 


### Example docker file
```bash 
# Pull the "tomcat" image. The community maintains this image. 
FROM tomcat                    # Copy all files present in the current folder to the "/usr/local/tomcat/webapps" folder 
COPY ./*.* /usr/local/tomcat/webapps
``` 

### Generic steps for running a docker image as a container
```bash
# This command will look for a Dockerfile in the `pwd`, and build the docker Image
docker build  --tag myImage  [OPTIONS] path_where_to_store_the_image 

# You can also pull an existing image from dockerHub
docker pull tomcat:latest

# Run a the image as a container
docker run --name myContainer myImage
```


### Using docker to run postgresql container that was PULLed from docker hub
```bash
# Download the latest version of the Base Image from docker hub
~ $docker pull postgres:latest
# Launch the container with docker
# Specify the container name, environment variables, port, and path to the docker image
# You're mapping port 5433 on your local machine to port 5432 in the container
~ $docker run --name psql -e POSTGRES_PASSWORD=papilo! -p 5433:5432 -d postgres:latest
# Confirm the server is running by checking running images
~ $docker ps
# Access the docker psql by using the local postgres client
~ $psql -h 0.0.0.0 -p 5433 -U postgres
# You can stop containers using the container id shown in docker ps
~ $docker stop <conainer_id>
```
<br>

### Steps to creating local Docker files, creating images with the files, and running the images as containers
1. Creating the `hello world` container locally
    1. Create a folder where the image will be built and name a docker *file* **"Dockerfile"**. It has no extensions and the file name is fixed.
    2. Populate the file 
        - ```dockerfile
            FROM python:3.7.2-slim
            
            ENTRYPOINT ["echo", "hello world"]
            ```
    3. Build the docker *image*. I included a tag for easy identification and specified the local directory as the path to the docker file `docker build --tag hwrld_jo ./`
    4. Run the *container* with the tag name and include an additional tag to rm it because this is a temporary build `docker run hwrld_jo -rm`
        - If you don't include the rm tag, you can stop the contaiber using the container id and then delete it afterwards
        - ```bash
          # Get the container id by seeing all the running containers
          ~ $docker ps -a
          # Stop the container
          ~ $docker container stop <container_ID>
          # Delete the container
          ~ $docker container rm <container_ID>
          ```
2. Creating a simple `flask app` container locally
    1. Create the `app.py` file in a folder
    2. Create the `Dockerfile` that copies the app.py file into the containers' WORKDIR and installs flask.
    3. Build the image with a tag `docker build --tag flask_app ./`
    4. Run the container and expose a port from the local system to the container `docker run -p 80:8080 flask_app`
    5. You can test the endpoint wth curl in a different terminal window `curl http://0.0.0.0:80`
    6. Use `docker ps` to get the container id and stop it with `docker container stop <container_ID>`
    7. Delete the container with `docker container rm <container_ID>`
    8. You can also delete the docker image with the name `docker image rm <image_name>`.
        - If you don't know the name, check all the names with `docker images` command
3. You can also access help docs with `docker container help`