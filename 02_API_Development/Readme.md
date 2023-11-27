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

### Project Setup
The flask app used here is setup in a slightly different way. Unlike the `SQL_Data_modeling` module, the flask app is setup in an `__init__.py` file with a folder structure as below.
```bash
./Project_Folder/
├── Backend
│   └── flaskr
│       ├── __init__.py
│       ├── config.py
│       └── models.py
└── Frontend
```
Specify the environment variables on mac with `export FLASK_APP=flaskr FLASK_ENV=development FLASK_DEBUG=True` from the `Backend` directory. This only needs to be run once. Subsequently, the app can be launced with `flask run`.  <br><br>

The `00_API_Initial` has files with scripts on how to: 
- set up the flask app, 
- perform CORS, and 
- do pagination on the `plants` db. 
<br>

The remaining folders are for implementing the `Udacity bookshelf app` whichs uses the `books` db include
- `01_Requests_Starter` for creating requests. I also updated it to handle errors instead of creating a new folder.

<br>

To run the react app, 
```bash
# Go to the frontend directory
cd 01_Requests_Starter/frontend
# Delete the package-lock.json file
rm package-lock.json
# Install jquery
npm install jquery --save
# Install additional npm modules to create a node_modules directory
npm install
# Fix errors 
npm audit fix --force
# Launch the server
npm run start
```
<br><br>


#### CURL
- Use `Cmd+Shift+C` to go to Chrome developer tools in your browser or use the 3 buttons at the top right or use `Fn+F12`
- Check if curl is installed with `curl --version`. The documentation help can be accessed with `curl --help`.
- Test a url using curl with `curl -X POST <url_link>`. Specify *-X POST* lets curl know it's a post request otherwise it implementsa a GET request by default.
- You can also pipe the results to json format using the command line **jq** processor e.g. `curl https://restcountries.com/v3.1/currency/cop | jq "."`. This makes the response easier to read. jq is installed as part of conda on my mac.
- The command to return all of the books - `curl http://127.0.0.1:5000/books`
- The command to update a single book's rating - `curl http://127.0.0.1:5000/books/8 -X PATCH -H "Content-Type: application/json" -d '{"rating":"1"}'`
- The command to delete a single book - `curl -X DELETE http://127.0.0.1:5000/books/8`
- The command to create a new book - `curl -X POST -H "Content-Type: application/json" -d '{"title":"Neverwhere", "author":"Neil Gaiman", "rating":"5"}' http://127.0.0.1:5000/books`
<br><br>


#### Request Endpoints
- Endpoints should be organized by resource and in the structure of `collection/item/collection`. e.g. `genres/1/movies` should access all movies related to genre 1.
- collection names are usually plural in production e.g. `genres`,`tasks`,`messages`,`movies` etc.
- `http` and `https` are different protocols.
- To create the `plants` db locally that matches the udacity workspace. Run the script below
```bash
su - postgres bash -c "dropdb plants"
su - postgres bash -c "createdb plants"
su - postgres bash -c "psql < plantsdb_setup/plantsdb-setup.sql"
su - postgres bash -c "psql plants < plantsdb_setup/plants.psql"
```
<br><br>

#### App routes
- For performing requests - `@app.route("/<route_path_or_arguements>", methods=["<method_name>"])`
- For handiling errors - `@app.errorhandler(<error_number>)`. This returns a json response.
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