from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

# Define configuration file for database connection. 
# You can include an optional DBAPI e.g.  postgresql+psycopg2. psycopg2 is the default for postgres.
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://josesmac:@localhost:5432/udacity_test'
# Use this line to silence the `SQLALCHEMY_TRACK_MODIFICATIONS adds significant overhead` warning
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Link database to flask app
db = SQLAlchemy(app)

# Create a class using db.model
# By inheriting from db.Model, we map from our classes to tables via SQLAlchemy ORM
class Person(db.Model):
    # Specify the table name or allow sqlalchemy to set it to a lower-case version of your class's name
    __tablename__ = 'persons'
    # Define the column names

    # This is the primary key column with integer type.
    id = db.Column(db.Integer, primary_key=True)  

    # This is the person's name class that is a string and NOT NULL
    # Other constraints like unique can a;sp be enforced to maintain data integrity across columns
    name = db.Column(db.String(), nullable=False)

    # Additional contraints can also be enforced to avoid negative values in a columns
    age = db.Column(db.Float, db.CheckConstraint('age>0'))

    def __repr__(self):
        '''
        This function determines how the print statement represents a row of data from the class.
        It is useful for debugging but it wanted me to include app.app_context()
        '''
        return f'<Person ID:{self.id}, name:{self.name}, age:{self.age}>'


# As of Flask-SQLAlchemy 3.0, all access to db.engine (and db.session) requires an active Flask application context
with app.app_context():
    # Detects models and creates tables for the models (if they don't exist).
    db.create_all()

    # Perform INSERT transactions with sqlalchemy. 
    # Note: The table has to be created before insert statements can be performed
    p1 = Person(name='Jadin',age=45.0)
    db.session.add(p1)
    db.session.commit()

# Other queries that can be executed are
# Person.query.all() # Get all the rows
# Person.query.filter(Person.name == 'Amy').first() # Perform a filter and select the first row

@app.route('/')
def index():
    # Perform a query to retrieve the first row of the table that was manually inserted in sql
    person = Person.query.first()
    all = Person.query.all()        # Select all rows. Returns a list
    return f'Hello, {person}'

if __name__ == '__main__':
   app.debug = True
   app.run(host="0.0.0.0",port=5000)