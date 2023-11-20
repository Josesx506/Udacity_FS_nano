### Todo app Pt. 2
1. **`app01.py`** - Shows how to implement an update for a boolean column using a form checkbox. <br>
This mimics the UPDATE in CR**U**D (This app uses the *form* method with the `index.html` template). <br><br>

2. **`app02.py`** - Shows how to delete an item from the todo list using a button. <br> 
The steps taken to implement the delete button are:
    - Loop through every To-Do item and show a delete button.
    - Pressing the delete button sends a request that includes which to-do item to delete.
    - The controller takes the user input, and notifies the models to delete the To-Do object by ID. My implementation gets the item using the `session` instead of `model` that the udacity example used because of the SQLAlchemy 2.0 update.
    - On successful deletion by the models, the controller should notify the view to refresh the page (*This was implemented using a separate function*) and redirect to our homepage, showing a fresh fetch of all To-Do items to now exclude the removed item.

