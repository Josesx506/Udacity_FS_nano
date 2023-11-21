### Todo app Pt. 2
1. **`app01.py`** - Shows how to implement an update for a boolean column using a form checkbox. <br>
This mimics the UPDATE in CR**U**D (This app uses the *form* method with the `index.html` template). <br><br>

2. **`app02.py`** - Shows how to delete an item from the todo list using a button. <br> 
The steps taken to implement the delete button are:
    - Loop through every To-Do item and show a delete button.
    - Pressing the delete button sends a request that includes which to-do item to delete.
    - The controller takes the user input, and notifies the models to delete the To-Do object by ID. My implementation gets the item using the `session` instead of `model` that the udacity example used because of the SQLAlchemy 2.0 update.
    - On successful deletion by the models, the controller should notify the view to refresh the page (*This was implemented using a separate function*) and redirect to our homepage, showing a fresh fetch of all To-Do items to now exclude the removed item.

3. In db relationships between primary and foreign keys, the datatype of both columns across the different models must match each other for a relationship to be formed. <br>
The **`rel01.py`** script shows how to implement relationships between Parent and Child tables. It's not really part of the model but the concept is used in the next step.

4. **`app03.py`** - shows how to implement the db relationships into the todoapp model by creating multiple todo lists with different items per list. It's an example of a *one to many* relationship. I also used flask migrate to create the db and track changes instead of using only SQLAlchemy. <br>
We can establish maintenance windows during times when the app isn't well used and manipulate production data then, in order to prepare the data before a schema migration, and change it after a schema migration.
