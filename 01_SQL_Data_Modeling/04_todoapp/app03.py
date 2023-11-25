from flask import Flask, render_template, request, redirect, url_for
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

# Function to use the form input to update the database by listening on the /create route name
@app.route('/todos/create', methods=['POST'])
def create_todo():
  # Read in the input.name attribute that is equal to description from the html form
  form_desc = request.form.get('description', '')
  # Assign it as a db.Model object
  todo = Todo(description=form_desc)
  # Insert it into the table with SQLAlchemy as a transaction
  db.session.add(todo)
  # Commit the changes to a database
  db.session.commit()
  # In the return statement, tell it to redirect the output the /index route which updates the page view in html
  # A clumsy replacement of indirect will be to make the function `return render_template('index.html', data=Todo.query.all())`
  return redirect(url_for('index'))

# Function for the index page
@app.route('/')
def index():
    return render_template('index_form.html', 
                           data=Todo.query.all()) # SQL select all query




    # The rows were inserted manually into the table via psql and not SQLAlchemy for this exercise
    # INSERT INTO todos (description) VALUES ('Do a thing 1')
    # A total of five rows were inserted and the flask app automatically updates the list from the db
    # Note: the html template was the same for app0 and app1.

if __name__ == '__main__':
   app.debug = True
   app.run(host="0.0.0.0", port=3000)