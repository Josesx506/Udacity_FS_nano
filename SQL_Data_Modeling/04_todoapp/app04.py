from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Note: The todoapp db will have to be manually created in terminal with `createdb todoapp`
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://josesmac:@localhost:5432/todoapp'
db = SQLAlchemy(app)



class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f'<Todo {self.id} {self.description}>'



with app.app_context():
    # Create the table in the database
    db.create_all()



# Function to use the form input to update the database by listening on the `/create` route name
@app.route('/todos/create', methods=['POST'])
def create_todo():
    # Read the json from the async fetch as a dictionary and access it using the input `name` attribute
    form_desc = request.get_json()['desc_name']
    # Assign it as a db.Model object, under the description column
    todo = Todo(description=form_desc)
    # Insert it into the table with SQLAlchemy as a transaction
    db.session.add(todo)
    # Commit the changes to a database
    db.session.commit()
    # Instead of using redirect, jsonify will return client data to url that we specify
    # Note: The dictionary key must match the form name in the html script
    return jsonify({'desc_name': todo.description})


# Function for the index page
@app.route('/')
def index():
    return render_template('index_form_async.html', 
                           data=Todo.query.all()) # SQL select all query


if __name__ == '__main__':
   app.debug = True
   app.run(host="0.0.0.0", port=3000)