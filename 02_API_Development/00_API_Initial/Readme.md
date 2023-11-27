### API Intro
The flask app used here is setup in a slightly different way. Unlike the `SQL_Data_modeling` module, the flask app is setup in an `__init__.py` file with a folder structure as below. Typically the `flaskr` folder will be placed in a *backend* directory but this chapter doesn't need one (because it doesn't have a frontend).
```bash
./Project_Folder/
└── flaskr
│   ├── __init__.py
│   ├── config.py
│   └── models.py
└── plantsdb_setup
    ├── plants.psql
    └── plantsdb-setup.sql
```
Specify the environment variables on mac with `export FLASK_APP=flaskr FLASK_ENV=development FLASK_DEBUG=True`. This only needs to be run once. Subsequently, the app can be launced with `flask run`.  <br><br>

This folder `00_API_Initial` has files with scripts on how to: 
[x] set up the flask app, 
[x] perform Cross-Origin Resource Sharing (CORS) 
    - With CORS, you can setup the 
        - The URLs that can call the api
        - The types of headers the app will accept e.g. ['Content-Type']
        - The types of request methods an app can accept e.g ['GET','POST']
[x] do pagination on the `plants` db.
    - This allows you to load data incrementatlly from the db onto pages.
    - E.g., if you have 100 items in your db, using pagination, you can load 10 items per page to make the app efficient
    - Additional pages can be accessed with a page argument `127.0.0.1:5000/plants?page=15`
Each file was originally named `__init__.py` and renamed after the item was completed.
<br><br>

#### Setup Database
In this chapter, we work with a `plants` db that is saved in the `plantsdb_setup` directory. To create the `plants` db locally that matches the udacity workspace. Run the script below
```bash
su - postgres bash -c "dropdb plants"
su - postgres bash -c "createdb plants"
su - postgres bash -c "psql < plantsdb_setup/plantsdb-setup.sql"
su - postgres bash -c "psql plants < plantsdb_setup/plants.psql"
```
<br><br>

#### Endpoint Intro
- Endpoints are the included as route names in `@app.route('/<endpoint>')` within flask apps.
- Endpoints should be organized by resource and in the structure of `collection/item/collection`. e.g. `genres/1/movies` should access all movies related to genre 1.
- collection names are usually plural in production e.g. `genres`,`tasks`,`messages`,`movies` etc.
- `http` and `https` are different protocols.
- Each endpoint can be initally tested with `curl` in terminal, and subsequent tests will be done with python's `unittests` in other chapters.
<br><br>

#### Perform API tests with CURL
- Use `Cmd+Shift+C` to go to Chrome developer tools in your browser or use the 3 buttons at the top right or use `Fn+F12`
- Check if curl is installed with `curl --version`. The documentation help can be accessed with `curl --help`.
- Test a url using curl with `curl -X POST <url_link>`. Specify *-X POST* lets curl know it's a post request otherwise it implementsa a GET request by default.
- You can also pipe the results to json format using the command line **jq** processor e.g. `curl https://restcountries.com/v3.1/currency/cop | jq "."`. This makes the response easier to read. jq is installed as part of conda on my mac.
- Only simple `GET` requests are tested in this chapter to confirm that the pagination implementation is successful.
