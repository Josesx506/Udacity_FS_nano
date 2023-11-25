from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
# Note: The todoapp db will have to be manually created in terminal with `createdb todoapp`
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://josesmac:@localhost:5432/todoapp'
db = SQLAlchemy(app)


class Drive (db.model):
  'Parent Table Class'
  __tablename__ = 'drivers'
  id = db.Column(db.Integer, primary_key=True)
  # lazy=True is default, and ensures the join function is done on-demand. This can be slow for an app with many requests.
  vehicles = db.relationship('Vehicle',backref='drivers',lazy=True)


class Vehicle (db.model):
  'Child Table Class'
  __tablename__ = 'vehicles'
  id = db.Column(db.Integer, primary_key=True)
  make = db.Column(db.String(), nullable=False)
  # Note the driver_id datatype of int must match the one in the parentTable `Drive.id` primary key column
  driver_id = db.Column(db.Integer, db.ForeignKey('drivers.id'),nullable=False)