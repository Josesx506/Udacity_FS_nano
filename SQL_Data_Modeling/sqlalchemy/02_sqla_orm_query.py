'''
This script shows how to perform different queries with sqlalchemy ORM.
It's built on top of the `flask_hello_app.py` script with a lot of repeated lines.
A flush takes pending changes and translates them into commands ready to be committed. It occurs:
    - when you call Query. Or
    - on db.session.commit()
- `db.Model.query` offers us the Query object. The Query object lets us generate SELECT statements 
    that let us query and return slices of data from our database
- Queries can be used to filter, joins, count, and even delete rows that meet a particular criteria
- Queries also allow method chaining e.g. filter and join 2 tables. This is equivalent to using 
    multiple WHERE statements. You can chain query methods to another (indefinitely), getting back 
    more query objects, until you chain it with a terminal method that returns a non-query object 
    like count(), all(), first(), delete(), etc
- The Query object can be accessed on a model using either:
    `MyModel.query` directly on the model (e.g. The `Person` class), or
    `db.session.query(MyModel)` using db.session.query instead
- Describe why a query is not necessarily considered a transaction.
    A database transaction changes (or potentially changes) data in one or more places in a database. At any point 
    during processing, if there was a disconnect, it is possible that part of the transaction was completed, when 
    part of it did not. This is the essence of CRUD development because data is constantly changing. A query simply 
    reflects data as it rests in the database, so if there was a disconnect during processing, the data is still 100% 
    fully intact.
'''

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://josesmac:@localhost:5432/fyyur'
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
    p2 = Person(name='Bob',age=16,weight=70.1)
    p3 = Person(name='Sarah',age=5,weight=12.2)
    p4 = Person(name='Jadin',age=32,weight=65.5)
    db.session.add_all([p1,p2,p3,p4])

    # Commit the session
    db.session.commit()

    # Perform queries
    # -------------------------- SELECT records --------------------------
    # all() - Equivalent to `SELECT * FROM <table>;`
    all_rows = Person.query.all()
    # first() - Equivalent to `SELECT * FROM <table> LIMIT 1;`
    first_row = Person.query.first()

    # -------------------------- Filtering records --------------------------
    # filter_by()- Equivalent to SELECT * FROM table WHERE column == <filter_key>
    filt_by = Person.query.filter_by(name='Amy').all()
    # filter() - This is more flexible than filter_by() and allows you to specify attributes on a given Model
    # Attributes from another model class can also be used. The OR synthax is not working
    # It works with =,!=,>,<,like,ilike,in,not in,is null, is not null,and,or,match
    filt1 = Person.query.filter(Person.weight>8).all()
    filt2 = Person.query.filter(Person.name.in_(['Bob','Sarah'])).all()
    filt3 = db.session.query(Person).filter(Person.name=='Bob',Person.age==16).all()   # AND statement
    #filt4 = db.session.query(Person).filter(Person.name=='Bob' | Person.name=='Jadin') # OR statement

    # -------------------------- Sorting records --------------------------
    # Can be done in ascending or descending order
    ord1 = db.session.query(Person).order_by(Person.id).all()
    ord2_desc = db.session.query(Person).order_by(db.desc(Person.id)).all()

    # -------------------------- Limit records -------------------------- 
    lim = Person.query.limit(2).all()

    # -------------------------- Aggregation --------------------------
    # Note: You shouldn't include select methods like all, first, etc if you intend to perform aggregation 
    query = Person.query.filter(Person.name.in_(['Bob','Sarah']))
    count = query.count()

    # -------------------------- Bulk Deletes --------------------------
    query = Table1.query.filter_by(col_name='<filter_key>')
    query.delete()

    # -------------------------- JOINS --------------------------
    # I only have one table here so I didn't implement this
    # Table1.query.join('Table2')

    # Udacity query quiz
    # Implement a query to filter all users by name 'Bob'.
    q1 = Person.query.filter(Person.name=='Bob').all()
    # Implement a LIKE query to filter the users for records with a name that includes the letter "b".
    q2 = Person.query.filter(Person.name.like('%b%')).all()
    # Return only the first 5 records of the query above.
    q3 = Person.query.filter(Person.name.like('%b%')).limit(5).all()
    # Re-implement the LIKE query using case-insensitive search.
    q4 = Person.query.filter(Person.name.ilike('%b%')).all()
    # Return the number of records of users with name 'Bob'.
    q5 = Person.query.filter(Person.name=='Bob').count()
    # print(q1,q2,q3,q4,q5,sep='\n')