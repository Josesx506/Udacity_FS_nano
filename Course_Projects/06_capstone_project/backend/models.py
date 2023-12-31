import os
from flask_sqlalchemy import SQLAlchemy
import json
import sys

# Setup the python file path to enable importing the system variables
sys.path.append(os.getcwd())
from settings import DB_NAME,DB_USER,DB_PASSWORD


# SQLite creates a local db within this folder so only the name has to be specified
database_filename = DB_NAME
project_dir = os.path.dirname(os.path.abspath(__file__))
# database_path = "sqlite:///{}".format(os.path.join(project_dir, database_filename))
database_path = f'postgresql://{DB_USER}:{DB_PASSWORD}@localhost:5432/{database_filename}'


db = SQLAlchemy()


# SETUP the db
def setup_db(app,  database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.app_context().push()
    db.app = app
    db.init_app(app)

class Booking(db.Model):
    '''
    This is the table that stores all the hair bookings made on the website
    '''
    __tablename__ = 'Bookings'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    phone = db.Column(db.String(120))
    email = db.Column(db.String(500))
    start_time = db.Column(db.DateTime)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    # stylists = db.relationship('Stylist', backref='bookings', lazy=True)
    # stylist_id = db.Column(db.Integer, nullable=False)
    stylist_id = db.Column(db.Integer, db.ForeignKey('Stylists.id'), nullable=False)

    def __init__(self, first_name, last_name, phone, email, start_time, completed, stylist_id):
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.email = email
        self.start_time = start_time
        self.completed = completed
        self.stylist_id = stylist_id
    
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def format(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone': self.phone,
            'email': self.email,
            'start_time': self.start_time,
            'completed': self.completed,
            'stylist_id': self.stylist_id
            }



class Service(db.Model):
    '''
    This is the table that stores all the services that can be completed on the website
    '''
    __tablename__ = 'Services'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Integer)
    duration = db.Column(db.String)
    image_link = db.Column(db.String(500))

    def __init__(self, name, price, duration, image_link):
        self.name = name
        self.price = price
        self.duration = duration
        self.image_link = image_link
    
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'duration': self.duration,
            'image_link': self.image_link,
            }


class Stylist(db.Model):
    '''
    This is the table that stores all the stylists working in the business. Stylists
    are linked to the bookings that they complete
    '''
    __tablename__ = 'Stylists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    phone = db.Column(db.String(120))
    email = db.Column(db.String(500))
    skills = db.Column(db.ARRAY(db.String(120)))
    image_link = db.Column(db.String(500))
    # booking_id = db.Column(db.Integer, db.ForeignKey('Bookings.id'), nullable=False)
    # bookings = db.relationship('Booking', backref='stylist', lazy=True) 

    def __init__(self, name, phone, email, skills, image_link):
        self.name = name
        self.phone = phone
        self.email = email
        self.skills = skills
        self.image_link = image_link
        # self.bookings = bookings
    
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'email': self.email,
            'skills': self.skills,
            'image_link': self.image_link
            }