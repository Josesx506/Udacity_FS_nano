'''
This script shows how to insert single and multiple rows into a database using sqlalchemy ORM.
It's built on top of the `flask_hello_app.py` script with a lot of repeated lines.
Note: When rows are inserted, a rollback() can only be performed before the changes are `flushed`.
    i.e. before .query(),.first() or .all() are called on a db.Model object.
    Flushing is the translation from python to SQL code.
Typically changes are `flushed` before `.commit()` pushes the changes to the db. This is a kind of temporary staging.
'''

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://josesmac:@localhost:5432/udacity_test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Person(db.Model):
    __tablename__ = 'persons'
    # Define the column names
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    age = db.Column(db.Integer, db.CheckConstraint('age>0'))
    weight = db.Column(db.Float, db.CheckConstraint('weight>0'))

    def __repr__(self):
        return f'<Person ID:{self.id}, name:{self.name}, age:{self.age}, weight{self.weight}>'

with app.app_context():
    db.create_all()

    # Perform INSERT transactions with sqlalchemy. 
    # session.add() is used to insert a single row
    p1 = Person(name='Amy',age=10,weight=50.1)
    db.session.add(p1)
    # session.add_all() is used to insert a multiple rows. It can take in a list
    p2 = Person(name='Bob',age=16,weight=70.1)
    p3 = Person(name='Sarah',age=5,weight=12.2)
    p4 = Person(name='Jadin',age=32,weight=65.5)
    db.session.add_all([p2,p3,p4])

    # Commit the session
    db.session.commit()

    # Perform filter_by queries
    # This returns a list that can be printed and it only works with '='
    # class.filter_by is the equivalent to SELECT * FROM table WHERE column == <filter_key>
    results = Person.query.filter_by(name='Amy').all()