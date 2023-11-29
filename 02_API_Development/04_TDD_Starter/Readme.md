### Test-Driven Development (TDD) for APIs
This exercise required me to first write unsuccessful tests for a search query to the database. <br>
1. I had to consider the json keys that would be in the response file before writing the functions and route names.
2. After writing the tests, I specified a route name with necessary db calls, error codes, and response keys that would enable a successful test.
3. I verified the tests were successful to complete this exercise.<br>

**Note**: The format() function under `backend/models.py` is not serializable, and needs to be called within a for loop to serialize across a SQLAlchemy expression (e.g. query.all()).