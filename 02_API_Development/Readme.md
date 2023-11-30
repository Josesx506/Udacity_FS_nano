## Module Overview
This module focused on workflows to create a *RESTful API*, test it, and create documentation for ease of use. REST stands for representational state transfer.
1. Application Programming Interface (API)s - Learn what APIs are and how do they work. Gain insights into the Internet protocols and RESTful APIs.
2. Handling HTTP Requests - Introduction you to HTTP, Flask, and writing and accessing endpoints.
3. Routing and API Endpoints - How to use endpoints and payloads (information passed along with the request) to extend the functionality of your API. Learn to organize API endpoints, handling Cross-Origin Resource Sharing (CORS) requests, parsing different request types, and handling errors.
4. Documentation - Learn to write documentation to enable others to use your API or contribute to your project.
5. Testing - Learn unit testing and test-driven development (TDD). Unit testing will ensure that each function is working as expected and handling errors. TDD will teach you to write tests even before defining the functions in your code.

### Python Packages used.
- Flask
- Flask-CORS (Cross-Origin Resource Sharing)
- SQLAlchemy
- JSONify
- Unittest

### Chapter Folders
- **00_API_Initial** for setting up the flask app within functions and integrating CORS for api development.
- **01_Requests_Starter** for creating requests and handing errors with FLASK-CORS for the `Udacity bookshelf` app.
- **02_Errors_Starter** for creating route-names that handle errors in the `Udacity bookshelf` app, and returns human readable messages.
    - In this chapte they also provided an intro to `unittests`. This enables running all the tests for the api endpoints in a single python script. Error tests were written to mimic successful and unsuccessful requests to assess how the app handles errors.
- **04_TDD_Starter** for learning how test driven development is done. A test for a search request was first written in the `backend/test_flaskr.py` file. 
    - The initial test will fail because no route name is specified in the `backend/flaskr/__init__.py` file.
    - The route_name function was designed to pass the test, and future tests designs will be used to refactor the code that handles each search request.
- **05_API_Documentation** for describing what the bookshelf api does as a simple readme file. *Note: This is different from Project Documenetation.*
- The front end uses React, and the backend code follows <a src='https://peps.python.org/pep-0008/'>PEP8 style guidelines</a>.
<br><br>

#### Terminal Tips
- Kill a process with 
```bash
ps -a
sudo kill <pid>
```
- Check if a port is already occuppied and kill the process
```bash
sudo su - 
ps -ef | grep postmaster | awk '{print $2}'
kill <PID> 
```
- Search whole word, recursively in a folder, case-insensitive, and display the files having the keyword `grep -wril "todo" ./frontend/src/`