from flask import Flask, render_template, request, jsonify, abort, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import sys

app = Flask(__name__)
# Note: The todoapp db will have to be manually created in terminal with `createdb todoapp`
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://josesmac:@localhost:5432/todoapp'
db = SQLAlchemy(app)


class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Todo {self.id} {self.description}>'



with app.app_context():
    # Create the table in the database
    db.create_all()


# ----------------------------------------- Update form row -----------------------------------------
# Function to use the form input to update the database by listening on the `/create` route name
@app.route('/todos/create', methods=['POST'])
def create_todo():
    # Define an error flag
    error = False
    # Read the json from the async fetch as a dictionary and access it using the input `name` attribute
    form_desc = request.get_json()['desc_name']
    # Create a body dictionary to capture the db session values, so it can be accessed after the session is closed
    body = {}
    try:
        # Assign it as a db.Model object, under the description column
        todo = Todo(description=form_desc)
        # Insert it into the table with SQLAlchemy as a transaction
        db.session.add(todo)
        # Commit the changes to a database
        db.session.commit()
        # Note: The dictionary key must match the form name in the html script
        body['desc_name'] = todo.description
    except:
        db.session.rollback()
        error=True
        print(sys.exc_info())
    finally:
        # Close the database connection
        db.session.close()
        if error:
            # In the event of an error, we can use flask to print an error code of choice
            abort(400)
        else:
            # This way, jsonify is returning a temporary dictionary object after the session is closed which avoids errors
            return jsonify(body)


# ----------------------------------------- Update form checkbox -----------------------------------------
# Because <todo_id> is set as a placeholder in the route name, it can be used as a function arg
@app.route('/todos/<todo_id>/set-completed', methods=['POST'])
def set_completed_todo(todo_id):
    try:
        completed = request.get_json()['completed']
        # Perform sqlalchemy query to get the row with the specified id
        todo = Todo.query.get(todo_id)
        # Update the completed column of the selected row
        todo.completed = completed
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('index'))


# ----------------------------------------- Delete form button -----------------------------------------
# Because <todo_id> is set as a placeholder in the route name, it can be used as a function arg
@app.route('/todos/<todo_id>/delete-row', methods=['DELETE'])
def delete_todo_item(todo_id):
    try:
        # Perform sqlalchemy query to get the row with the specified id
        todo = db.session.get(Todo, todo_id)
        # Delete the row of interest and commit the changes
        db.session.delete(todo)
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return jsonify({ 'success': True })


# Function for the index page
@app.route('/')
def index():
    return render_template('index_delete.html', 
                           # SQL select all query that is ordered by id to preserve the list arrangement
                           data=Todo.query.order_by('id').all()) 


if __name__ == '__main__':
   app.debug = True
   app.run(host="0.0.0.0", port=3000)