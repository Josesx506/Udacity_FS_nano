# ----------------------------- Database migration and updating via html -----------------------------
# This script is linked to an index.html template that allows you to update the db with a html form page.
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Define the app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://josesmac:@localhost:5432/udacity_test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Link the database to SQLAlchemy
db = SQLAlchemy(app)
# Link the app and db to the migrate function
migrate = Migrate(app, db)

# When using migrations, we don't use db.create_all() anymore.

class Person(db.Model):
    __tablename__ = 'persons'
    # Define the column names
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    age = db.Column(db.Integer, db.CheckConstraint('age>0'))
    weight = db.Column(db.Float, db.CheckConstraint('weight>0'))
    # Add a height column and use the flask_migrate to upgrade the db
    height = db.Column(db.Float, db.CheckConstraint('height>0'))

    def __repr__(self):
        return f'<Person ID:{self.id}, name:{self.name}, age:{self.age}, weight{self.weight}>'


@app.route('/persons/create', methods=['POST'])
def create_todo():   
   body={}
   error = False
   try: 
       name =  request.get_json()['name']
       person = Person(name=name)
       body['name'] = person.name
       db.session.add(person)
       db.session.commit()
   except:        
        error = True
        db.session.rollback()
        print(sys.exc_info())
   finally:
        db.session.close()           
        if  error == True:
            abort(400)
        else:            
            return jsonify(body)

@app.route('/')
def index():
    return render_template('index.html', data=Person.query.all())



#always include this at the bottom of your code
if __name__ == '__main__':
   app.run(host="0.0.0.0", port=3000)