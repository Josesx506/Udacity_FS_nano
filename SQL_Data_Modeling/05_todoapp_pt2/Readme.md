### Todo app Pt. 2
1. **`app01.py`** - Shows how to implement an update for a boolean column using a form checkbox. <br>
This mimics the UPDATE in CR**U**D (This app uses the *form* method with the `index.html` template). <br><br>

2. **`app02.py`** - Shows how to delete an item from the todo list using a button. <br>
This mimics the DELETE in CRU**D** (This app uses the *form* method with the `index_delete.html` template).
The steps taken to implement the delete button are:
    - Loop through every To-Do item and show a delete button.
    - Pressing the delete button sends a request that includes which to-do item to delete.
    - The controller takes the user input, and notifies the models to delete the To-Do object by ID. My implementation gets the item using the `session` instead of `model` that the udacity example used because of the SQLAlchemy 2.0 update.
    - On successful deletion by the models, the controller should notify the view to refresh the page (*This was implemented using a separate function*) and redirect to our homepage, showing a fresh fetch of all To-Do items to now exclude the removed item.
<br>

3. In db relationships between primary and foreign keys, the datatype of both columns across the different models must match each other for a relationship to be formed. <br>
The **`rel01.py`** script shows how to implement relationships between Parent and Child tables. It's not really part of the model but the concept is used in the next step.<br><br>

4. **`app03.py`** - shows how to implement the db relationships into the todoapp model by creating multiple todo lists with different items per list. It's an example of a *one to many* relationship. I also used flask migrate to create the db and track changes instead of using only SQLAlchemy (This app uses the *form* method with the `index_rela.html` template). <br>
We can establish maintenance windows during times when the app isn't well used and manipulate production data then, in order to prepare the data before a schema migration, and change it after a schema migration.
    - **This was the most complex step so far.**
    - A `parent` and `child` table was created.
        - Rows in the parent table were manually defined in psql
        - The new column in the child table was initially set to allow NULL values in SQLAlchemy with `nullable=True`, then it was updated in psql with `UPDATE todos SET list_id=1 WHERE list_id IS NULL;`
        - Then the new column was changed to reject NULL values (`nullable=False`) and the db was migrated.
        - A second parent row was defined and some dummy child items were assigned to it with SQLAlchemy.
            ```python
            # The child table can access this column by calling <child_table>.<back_ref>.
            parent1 = TodoList(name='One')      # Parent Table row
            item1 = Todo(description='Item 1')  # Child Table row
            item2 = Todo(description='Item 2')  # Child Table row
            # Associate the child tables to the parent table
            item1.list = parent1
            item2.list = parent1

            with app.app_context():
                # Adding only the parent table row adds all the associate child table rows 
                db.session.add(parent1)
                db.session.commit()
            ```
    - The `html` allowed creation of multiple todo items attached to different list names. The list items were create manually in `psql`.
    - The `js script` allowed the checkbox, text, and delete button to be appended asynchronously each time a todo entry was created.
        - It also allowed the parent element of the todo item to be deleted from the UI when the button is clicked.
    - The `python` file used list filters to update the todo items from the two lists from the html form.
        - The python file also allowed creation of multiple pages based on the id column of the parent table, with the homepage set to the first item.
        - Additional variables were added to the `render_template()` function in flask instead of using only data. New variable names included the values of the parent table id column, the active list id, and the filtered todo list that belongs to the active id.
