from flask import Flask, render_template
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

    # The rows were inserted manually into the table via psql and not SQLAlchemy for this exercise
    # INSERT INTO todos (description) VALUES ('Do a thing 1')
    # A total of five rows were inserted and the flask app automatically updates the list from the db
    # Note: the html template was the same for app0 and app1.


@app.route('/')
def index():
    return render_template('index.html', 
                           data=Todo.query.all()) # SQL select all query


if __name__ == '__main__':
   app.debug = True
   app.run(host="0.0.0.0", port=3000)