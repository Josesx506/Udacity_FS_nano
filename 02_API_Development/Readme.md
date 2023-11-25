## Module Overview
1. Application Programming Interface (API)s - Learn what APIs are and how do they work. Gain insights into the Internet protocols and RESTful APIs.
2. Handling HTTP Requests - Introduction you to HTTP, Flask, and writing and accessing endpoints.
3. Routing and API Endpoints - How to use endpoints and payloads (information passed along with the request) to extend the functionality of your API. Learn to organize API endpoints, handling Cross-Origin Resource Sharing (CORS) requests, parsing different request types, and handling errors.
4. Documentation - Learn to write documentation to enable others to use your API or contribute to your project.
5. Testing - Learn unit testing and test-driven development (TDD). Unit testing will ensure that each function is working as expected and handling errors. TDD will teach you to write tests even before defining the functions in your code.

### Python Packages used.
- Flask
- Flask-CORS
- SQLAlchemy
- JSONify
- Unittest

### Project Setup
The flask app used here is setup in a slightly different way. Unlike the `SQL_Data_modeling` module, the flask app is setup in an `__init__.py` file with a folder structure as below.
```bash
./Project_Folder/
├── Backend
│   └── flaskr
│       ├── __init__.py
│       └── config.py
└── Frontend
```
Specify the environment variables on mac with `export FLASK_APP=flaskr FLASK_ENV=development FLASK_DEBUG=True` from the `Backend` directory. This only needs to be run once. Subsequently, the app can be launced with `flask run`. <br><br>


#### CURL
- Use `Cmd+Shift+C` to go to Chrome developer tools in your browser or use the 3 buttons at the top right or use `Fn+F12`
- Check if curl is installed with `curl --version`. The documentation help can be accessed with `curl --help`.
- Test a url using curl with `curl -X POST <url_link>`. Specify *-X POST* lets curl know it's a post request otherwise it implementsa a GET request by default.
- You can also pipe the results to json format using the command line **jq** processor e.g. `curl https://restcountries.com/v3.1/currency/cop | jq "."`. This makes the response easier to read. jq is installed as part of conda on my mac.
