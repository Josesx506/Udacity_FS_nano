## Module Overview
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