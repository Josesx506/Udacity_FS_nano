import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
import json
import sys

# Setup the python file path to enable importing the system variables
sys.path.append(os.getcwd())
from backend.src.settings import DB_NAME

# SQLite creates a local db within this folder so only the name has to be specified
database_filename = DB_NAME
project_dir = os.path.dirname(os.path.abspath(__file__))
database_path = "sqlite:///{}".format(os.path.join(project_dir, database_filename))

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    with app.app_context():
        db.app = app
        db.init_app(app)


'''
db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
    !!NOTE you can change the database_filename variable to have multiple verisons of a database
'''


def db_drop_and_create_all(app):
    with app.app_context():
        db.drop_all()
        db.create_all()
        # --------------------- add six demo row which is helping in POSTMAN test ---------------------
        drink1 = Drink(title='Hot Water',
                       recipe='[{"name": "water", "color": "lightblue", "parts": 1}]')
        drink2 = Drink(title='Hot Milk',
                       recipe='[{"name": "water", "color": "lightblue", "parts": 1},{"name": "milk", "color": "beige", "parts": 1}]')
        drink3 = Drink(title='Hot Chocolate',
                       recipe='[{"name": "water", "color": "lightblue", "parts": 1},{"name": "milk", "color": "beige", "parts": 1},{"name": "chocolate", "color": "#C0856B", "parts": 2}]')
        drink4 = Drink(title='Mocha',
                       recipe='[{"name": "water", "color": "lightblue", "parts": 1},{"name": "milk", "color": "beige", "parts": 1},{"name": "coffee", "color": "#6f4e37", "parts": 1},{"name": "chocolate", "color": "#C0856B", "parts": 4}]')
        drink5 = Drink(title='Latte',
                       recipe='[{"name": "milk", "color": "beige", "parts": 1},{"name": "coffee", "color": "#6f4e37", "parts": 1}]')
        drink6 = Drink(title='Water',
                       recipe='[{"name": "water", "color": "blue", "parts": 1}]')
        # Insert all the drinks into the db and replace drink.insert()
        drinks = [drink1,drink2,drink3,drink4,drink5,drink6]
        db.session.add_all(drinks)
        db.session.commit() 

        # --------------------- Baristas ---------------------
        # add two demo row to the Barista table - barista.insert()
        barista1 = Barista(name='John Doe',
                           flavors='["Americano", "Latte", "Mocha"]',
                           proficiency=3,
                           image_url='https://seattleheadshotpro.com/wp-content/uploads/2018/08/Brandon-Seattle-Headshot-Pro-Headshots-Seattle-500px.jpg')
        barista2 = Barista(name='Jane Doe',
                           flavors='["Americano", "Latte", "Mocha", "Chocolate"]',
                           proficiency=4,
                           image_url='https://pbs.twimg.com/profile_images/1687103676438269952/zNqrw_eY_400x400.jpg')
        baristas = [barista1,barista2]
        db.session.add_all(baristas)
        db.session.commit() 

# ROUTES

'''
Drink
a persistent drink entity, extends the base SQLAlchemy Model
'''


class Drink(db.Model):
    # Autoincrementing, unique primary key
    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    # String Title
    title = Column(String(80), unique=True)
    # the ingredients blob - this stores a lazy json blob
    # the required datatype is [{'color': string, 'name':string, 'parts':number}]
    recipe = Column(String(250), nullable=False)

    def __init__(self, title, recipe):
        self.title = title
        self.recipe = recipe

    '''
    short()
        short form representation of the Drink model
    '''

    def short(self):
        # print(json.loads(self.recipe))
        short_recipe = [{'color': r['color'], 'parts': r['parts']} for r in json.loads(self.recipe)]
        return {
            'id': self.id,
            'title': self.title,
            'recipe': short_recipe
        }

    '''
    long()
        long form representation of the Drink model
    '''

    def long(self):
        return {
            'id': self.id,
            'title': self.title,
            'recipe': json.loads(self.recipe)
        }

    '''
    insert()
        inserts a new model into a database
        the model must have a unique name
        the model must have a unique id or null id
        EXAMPLE
            drink = Drink(title=req_title, recipe=req_recipe)
            drink.insert()
    '''

    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes a new model into a database
        the model must exist in the database
        EXAMPLE
            drink = Drink(title=req_title, recipe=req_recipe)
            drink.delete()
    '''

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update()
        updates a new model into a database
        the model must exist in the database
        EXAMPLE
            drink = Drink.query.filter(Drink.id == id).one_or_none()
            drink.title = 'Black Coffee'
            drink.update()
    '''

    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.short())


class Barista(db.Model):
    # Autoincrementing, unique primary key
    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    # String Title
    name = Column(String(80), unique=True)
    # the coffee flavors each barista can prepare - this stores a lazy json blob
    # the required datatype is '["Americana", "Latte", "Mocha"]'
    flavors = Column(String(250), nullable=False)
    proficiency = Column(Integer().with_variant(Integer, "sqlite"), default=3)
    image_url = Column(String(250), nullable=True)

    def __init__(self, name, flavors, proficiency, image_url):
        self.name = name
        self.flavors = flavors
        self.proficiency = proficiency
        self.image_url = image_url
    
    def short(self):
        short_flavors = [flvr for flvr in json.loads(self.flavors)]
        return {
            'id': self.id,
            'name': self.name,
            'flavors': short_flavors,
            'proficiency': self.proficiency,
            'image_url': self.image_url,
        }
    
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.short())


