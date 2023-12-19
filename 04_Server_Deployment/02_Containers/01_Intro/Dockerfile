# Start the dockerfile with a source image from docker hub
FROM python:3.7.2-slim

# Copy files and define the work directory
COPY . /app
WORKDIR /app

# Install dependencies
RUN pip install --upgrade pip
RUN pip install flask

# Specify the entry point, ports etc to access the app
ENTRYPOINT [“python”, “app.py”]