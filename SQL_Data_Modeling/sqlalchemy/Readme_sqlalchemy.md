### sqlachemy overview
This python package allows Object Relational Mapping (ORM) of sql database rows and columns into python classes and objects. <br>
**Dialects** allow it to work with multiple sql backends without changing the python code which is useful for testing e.g. use SQLite for developer environment since its lighter, and Postgres for production/ <br>
**Connection Pool** also allows it to open and close database connections automatically reducing the amount low-level sql code written and improving performance at scale. <br>
With sqlalchemy, the entire `fyyur` website project can be written with python.