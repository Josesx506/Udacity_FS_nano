### Trivia Implementation Checklist
Here are the lists of Todo Items I've completed. They were not completed sequentially but it helped me keep track. <br>

Note: all requests are handled with *REACT* with asynchronous fetch.
- [x] Create local trivia db with `backend/trivia.psql` script.
- [x] Setup the db and app in `backend/models.py`, and ensure they match with the local db that was created.
- [x] Setup the CORS app in `backend/flaskr/__init__.py` script.
<br>

- [x] Implement a function to paginate over the *questions* in the return 10 questions per page. 
- [x] Implement request endpoints in `backend/flaskr/__init__.py` script.
    - [x] Create a GET endpoint that allows the *react app* to retrieve all the question `categories`.
    - [x] Create a GET endpoint that allows the *react app* to retrieve all the saved `questions` and show them using pagination (10 questions per page).
    - [x] Create a DELETE endpoint that allows users to delete saved `questions` from the db based on the question id.
    - [x] Create a POST endpoint that allows users to add new `questions` to the db.
    - [x] Create a POST endpoint that allows users to search for existing `questions` from the db.
    - [x] Create a POST endpoint that allows users to play the trivia game.
        - [x] The frontend indicates which `category` the user will like to play as well as the total number of questions that should be asked (Defaults to 5 but it can be modified).
        - [x] The backend checks the selected category, randomly selects a question for the user till all the questions in that category are exhausted or the max. number of game questions has been reached.
    - [x] Create endpoints for the errors to return human readable messages.
<br>

- [x] Perform api tests for all the request and error endpoints in `backend/test_flaskr.py`
    - [x] Create a `trivia_test` db that mimics the trivia db structure for testing purposes
    - [x] API test for successful & unsuccessful GET `categories` endpoint.
<br><br><br><br>


The hardest endpoint I had trouble implementing was creating a post request to the play the trivia game. An api example for this endpoint is `curl -X POST -H "Content-Type: application/json" -d '{"previous_questions":[20,21,22], "quiz_category":{ "type": "science", "id": "1" }}' http://127.0.0.1:5000/quizzes`
- *previous_questions* is a list of the question id's that have already been asked. It defaults to []
- *quiz_category* is a dictionary object that contains the name and id of the selected trivia category. If all categories are selected, the id defaults to 0.
- This request returns the success state and remaining questions. 
- An example of a successful request with remaining questions is
    - ```bash
        {
        "question": {
            "answer": "The Liver",
            "category": 1,
            "difficulty": 4,
            "id": 20,
            "question": "What is the heaviest organ in the human body?"
        },
        "success": true
        }
    ```
<br>

- An example of a successful request when all the questions have been exhausted is 
    - ```bash
        {
        "question": "",
        "success": true
        }
    ```
<br>

- **Note**: Even if all categories are selected, only 5 questions are asked before a final score is returned.