### Sqlachemy overview
This python package allows Object Relational Mapping (ORM) of sql database rows and columns into python classes and objects. <br>
There are 4 levels of abstraction which sqlalchemy uses to make database interactions easier.
- Dialect
- Connection Pool
- Engine
- SQL Expressions
<br><br>

**Dialects** allow it to work with multiple sql backends without changing the python code which is useful for testing e.g. use SQLite for developer environment since its lighter, and Postgres for production. <br><br>
**Connection Pool** also allows it to open and close database connections automatically reducing the amount low-level sql code written. It improves performance at scale by:
1. Handing dropped connections.
2. Avoiding very small calls to the db.
3. Avoiding opening and closing connections for every data change. 


**Engine** allows it to work with low level sql like `psycopg2`.
```python
from sqlalchemy import create_engine

engine = create_engine('postgres://...')
conn = engine.connect()
result = conn.execute('SELECT * vehicles')

result.close()
```
This can be used for small tests to validate queries etc.<br><br>
**SQL Expressions**

With sqlalchemy, the entire `fyyur` website project can be written with python.