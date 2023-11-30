### Chapter Setup
The flask app in this chapter is setup in an `__init__.py` file with a folder structure as below.
```bash
./Project_Folder/
├── backend
│   ├── flaskr
│   │   └── __init__.py
│   ├── books.psql
│   ├── models.py
│   ├── requirements.txt
│   └── setup.sql
├── frontend
│   ├── node_modules
│   ├── package-lock.json
│   ├── package.json
│   ├── public
│   └── src
└── setup.sh
```
Specify the environment variables on mac with `export FLASK_APP=flaskr FLASK_ENV=development FLASK_DEBUG=True` from the `backend` directory. This only needs to be run once. Subsequently, the app can be launced with `flask run`. The `node_modules` folder is large and was excluded in the .gitignore file <br><br>

#### App Requirements
This is the first part of the `Udacity bookshelf` app that handles creating api endpoints and handling errors. 
- It uses the `bookshelf` db that can be installed with 
```bash
psql < backend/setup.sql
psql bookshelf < backend/books.psql
```
<br>

- It also uses a react app for its front end which can be set up with 
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
- **NOTE**: The flask server must be running for the react app to work
<br>

#### Chapter Deliverables
This chapter was originally for only creating requests, however I merged it with the error handling chapter because that chapter was short. <br> The **TODO** items in this chapter included.
- [x] Setup a flask app that is connected to the `bookshelf` db.
- [x] Use CORS to define the valid request headers and methods.
- [x] Create API endpoints for
    - [x] **GET**ting all the books from the db and rendering them with pagination
    - [x] **UPDATE** the book ratings from the db interactively using the frontend or manually with curl requests
    - [x] **DELETE** a book from the db interactively using the frontend or manually with curl requests
    - [x] **POST** a new book to the db interactively using the frontend or manually with curl requests
- [x] Create error handlers to return *human-readable* response messages when errors are encountered.
    - Error messages were accessed using a different route handler `@app.errorhandler(<error_status_code)` that replaces the default html message from flask's abort with a json message.
[x] Test all the endpoints using curl.
<br><br>

#### API tests with CURL
API tests were performed to validate the endpoints. The command to 
- GET all of the books - `curl http://127.0.0.1:5000/books`
- Update a single book's rating - `curl http://127.0.0.1:5000/books/8 -X PATCH -H "Content-Type: application/json" -d '{"rating":"1"}'`
- Delete a single book - `curl -X DELETE http://127.0.0.1:5000/books/8`
- Create/Post a new book - `curl -X POST -H "Content-Type: application/json" -d '{"title":"Neverwhere", "author":"Neil Gaiman", "rating":"5"}' http://127.0.0.1:5000/books`
- Curl requests can be piped to a terminal json formatter `jq` with `curl http://127.0.0.1:5000/books | jq '.'`
- Testing endpoints manually with curl is tiresome and an updated test method is introduced in subsequent chapters.
<br><br>

#### App routes
- For performing requests - `@app.route("/<route_path_or_arguements>", methods=["<method_name>"])`
- For handiling errors - `@app.errorhandler(<error_number>)`. This returns a json response.
