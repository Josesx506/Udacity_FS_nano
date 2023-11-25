from flask import Flask, render_template, request, jsonify, abort, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys

app = Flask(__name__)
# Note: The todoapp db will have to be manually created in terminal with `createdb todoapp`
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://josesmac:@localhost:5432/todoapp'
db = SQLAlchemy(app)
# Link the app and db to the migrate function
migrate = Migrate(app, db)


class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    list_id = db.Column(db.Integer, db.ForeignKey('todolists.id'), nullable=False)

    def __repr__(self):
        return f'<Todo {self.id} {self.description} {self.completed} list {self.list_id}>'

class TodoList(db.Model):
    __tablename__ = 'todolists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    # The child table can access this column by calling <child_table>.<back_ref> e.g 
    # Lazy is set to True to enable on demand joins
    todos = db.relationship('Todo', backref='list', lazy=True)

    def __repr__(self):
        return f'<TodoList {self.id} {self.name}>'


# ----------------------------------------- Update form row -----------------------------------------
# Function to use the form input to update the database by listening on the `/create` route name
@app.route('/todos/create', methods=['POST'])
def create_todo():
    # Define an error flag
    error = False
    # Create a body dictionary to capture the db session values, so it can be accessed after the session is closed
    body = {}
    try:
        # Read the json from the async fetch as a dictionary and access it using the input `name` attribute
        form_desc = request.get_json()['desc_name']
        list_id = request.get_json()['list_id']
        todo = Todo(description=form_desc, completed=False)
        active_list = db.session.get(TodoList, list_id)
        todo.list = active_list                 # Assign the list id of the todo item
        # Insert it into the table with SQLAlchemy as a transaction
        db.session.add(todo)
        # Commit the changes to a database
        db.session.commit()
        # Note: The dictionary key must match the form name in the html script
        body['id'] = todo.id                     # Set by default by SQLAlchemy
        body['completed'] = todo.completed       # Set by default to False on the first line of try statement
        body['desc_name'] = todo.description
    except:
        error=True
        db.session.rollback()
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


# Function for any page that will be specified by a list id
@app.route('/lists/<list_id>')
def get_list_todos(list_id):
    return render_template('index_rela.html', 
                           lists=TodoList.query.all(),
                           active_list=db.session.get(TodoList, list_id),
                           # SQL select all query that is filtered by the list id, and ordered
                           # by the id of the selected list to preserve the arrangement
                           todos=Todo.query.filter_by(list_id=list_id).order_by('id').all()) 


# Function for the index or home page. It navigates to the first uncategorized list by default
@app.route('/')
def index():
    return redirect(url_for('get_list_todos', list_id=1))


if __name__ == '__main__':
   app.debug = True
   app.run(host="0.0.0.0", port=3000)