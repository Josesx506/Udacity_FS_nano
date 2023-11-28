### Importance of Testing
As with all tests, writing unittests for your API verifies the behavior. For APIs, test should be written:
1. To confirm expected request handling behavior
2. To confirm success-response structure is correct
3. To confirm expected errors are handled appropriately
4. To confirm CRUD operations persist
This module provides an intro to `unittests` with python in-lieu of writing manual `curl` tests.

#### Chapter Setup
It's a continuation of the project from the previous chapter and the old `bookshelf` db can be used. The flask app environment variables also need to be set. **Note**: The additional `test_flaskr.py` file in the folder structure
```bash
├── backend
│   ├── flaskr
│   │   └── __init__.py
│   ├── models.py
│   ├── requirements.txt
│   ├── books.psql
│   ├── setup.sql
│   └── test_flaskr.py
└── frontend
    ├── node_modules
    ├── package-lock.json
    ├── package.json
    ├── public
    └── src
```
The psql db script also created a `bookshelf_test` which we'll be using in this chapter. <br>

#### Running tests
**Note**: all test functions must start with `test_` for them to run
- Modified the `create_app()` function in `flaskr/__init__.py` to accept a db_name as an argument.
- Changed the db from the `bookshelf` development db to the `bookshelf_test` in the `test_flaskr.py` `setUp()` function
- The tests can be implemented whether the flask app is running or not.
- I implemented tests to evaluate successful and unsuccessful requests for the GET,PATCH,POST and DELETE requests
- Synced multiple functions to keep the test db length static. I might be able to implement this once I learn `tearDown` later in this chapter.
