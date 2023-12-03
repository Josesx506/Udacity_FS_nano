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
    - [x] API test for successful & unsuccessful GET `categories/<int:cat_id>/questions` endpoint.
    - [x] API test for successful & unsuccessful GET `questions` endpoint.
    - [x] API test for successful & unsuccessful DELETE `questions/<int:q_id>` endpoint.
    - [x] API test for successful & unsuccessful POST new `questions` endpoint (Allows creation of new questions in db).
    - [x] API test for successful & unsuccessful POST search `questions` endpoint (Allows search of existing/non-existing question sub-string in db).
    - [x] API test for successful & unsuccessful POST play trivia `quizzes` endpoint (Allows users to play the game).
        - [x] Test for playing game with all categories
        - [x] Test for playing game with specific categories
        - [x] Test for ending game when questions have been exhausted
        - [x] Test for raising `400` error when request is improperly formatted
    - [x] Error tests are already included in API tests above
<br><br><br><br>


The hardest endpoint I had trouble implementing was creating a post request to the play the trivia game. 

- **Note**: Even if all categories are selected, only 5 questions are asked before a final score is returned.


##### ----------------------------------------------------------------------------------------------------------------------------------------------------------------------
## API Documentation
### Introduction
The Trivia API is organized around REST. Our API accepts form-encoded request bodies and returns json-encoded responses. It also uses standard HTTP response codes and verbs. <br>
The Trivia api allows users to save questions from different categories and play trivia games to support their applications.

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1/5000`, which is set as a proxy in the frontend configuration. <br>
- Authentication: This version of the application does not require authentication or API keys. Future API keys will be configured from <a src="">here</a>.<br>

### Errors
The Trivia api uses conventional HHTP response codes to indicate the success or failure of an API request. Errors are returned as json objects. Codes in the `2.x.x` range indicate success. Codes in the `4.x.x` range indicate an error from the request body.

#### Attributes
**success** *string* <br>
The status of the error as a boolean. This can be True or False. <br>

**error** int <br>
This indicates the HTTP error status code. It is usually in the `2.x.x` and `4.x.x` range. <br>

**message** *string* <br>
The error description returned as a string An example is `unprocessable`. <br><br>

<table>
    <thead>
        <tr>
            <th colspan=2 style="text-align: center;">HTTP STATUS CODE SUMMARY</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td style="text-align: right;"><b>200 - OK</b></td>
            <td style="text-align: left;">Request was successful, and the server has responded</td>
        </tr>
        <tr>
            <td style="text-align: right;"><b>400 - Bad request</b></td>
            <td style="text-align: left;">The request cannot be processed because required fields are missing</td>
        </tr>
        <tr>
            <td style="text-align: right;"><b>404 - Resource not found</b></td>
            <td style="text-align: left;">The requested result doesn't exist</td>
        </tr>
        <tr>
            <td style="text-align: right;"><b>422 - Unprocessable</b></td>
            <td style="text-align: left;">The server understands the content type but it is unable to process the request.</td>
        </tr>
    </tbody>
</table>


### Resource Endpoint Library
#### Retrieve All Categories, All Questions, and Category Specific Questions
- **GET /categories**
    - Arguments
        - base_url (*required*) <br><br>
    - Example
        - `curl http://127.0.0.1:5000/categories` <br><br>
    - Returns: A dictionary of all categories, and success value. .
    ```bash
    {
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "success": true
    }
    ```
<br><br>

- **GET /questions**
    - Arguments
        - base_url (*required*) <br><br>
    - Example
        - `curl http://127.0.0.1:5000/questions` <br><br>
    - Returns: A dictionary of all categories, the current category, list of question objects arranged by question ID, success value, and total number of question. Results are paginated in groups of 10. You can also include a request argument to choose page number, starting from 1.
    ```bash
    {
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "current_category": "None",
    "questions": [
        {
        "answer": "Apollo 13",
        "category": 5,
        "difficulty": 4,
        "id": 2,
        "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },...
    ],
    "success": true,
    "total_questions": 20
    }
    ```
<br><br>

- **GET /categories/{category_id}/questions**
    - Arguments
        - base_url (*required*) <br><br>
    - Example
        - `curl http://127.0.0.1:5000/categories/3/questions` <br><br>
    - Returns: The current category name as a string, a list of questions that belong to the specified category, success value, and total number of questions. Results are paginated in groups of 10.
    ```bash
    {
    "currentCategory": "Geography",
    "questions": [
        {
        "answer": "Lake Victoria",
        "category": 3,
        "difficulty": 2,
        "id": 13,
        "question": "What is the largest lake in Africa?"
        },
        {
        "answer": "The Palace of Versailles",
        "category": 3,
        "difficulty": 3,
        "id": 14,
        "question": "In which royal palace would you find the Hall of Mirrors?"
        },
        {
        "answer": "Agra",
        "category": 3,
        "difficulty": 2,
        "id": 15,
        "question": "The Taj Mahal is located in which Indian city?"
        }
    ],
    "success": true,
    "totalQuestions": 3
    }
    ```
<br><br>

#### Delete Question
- **DELETE /questions/{question_id}**
- Delete a specific question from your database.
    - Arguments 
        - base_url (*required*)
        - question_id (*required*) <br><br>
    - Example
        - `curl -X DELETE http://127.0.0.1:5000/questions/27` <br><br>
    - Returns: The id of the deleted question, and  success value. The react frontend updates the page automatically
    ```bash
    {
    "deleted": 27,
    "success": true,
    }
    ```


<br><br>

#### Create a Question
- **POST /questions**
- Creates a new question using the submitted question, answer, difficulty and category.
    - Arguments 
        - base_url (*required*)
        - question (*required*)
        - answer (*required*)
        - difficulty (*required*)
        - category (*required*) <br><br>
    - Example
        - `curl -X POST -H "Content-Type: application/json" -d '{"question": "Which organ is responsible for pumping blood in the body", "answer": "The Heart", "difficulty": 3, "category": 1}' http://127.0.0.1:5000/questions` <br><br>
    - Returns: A dictionary of all the existing categories, the category type for the new question, list of all the questions with pagination, success value, and total questions to update the frontend.
    ```bash
    {
    "categories": {
        "1": "Science",
        "2": "Art",...
    },
    "current_category": "Science",
    "questions": [
        {
        "answer": "The Liver",
        "category": 1,
        "difficulty": 4,
        "id": 20,
        "question": "What is the heaviest organ in the human body?"
        },...
    ],
    "success": true,
    "total_questions": 22
    }
    ```
<br><br>

#### Search for a question using a substring in the question value
- **POST /questions**
    - Arguments 
        - base_url (*required*)
        - searchTerm (*required*)<br><br>
    - Example
        - `curl -X POST -H "Content-Type: application/json" -d '{"searchTerm":"Title"}' http://127.0.0.1:5000/questions` <br><br>
    - Returns: The current category as None, the list of questions that contain the search term, success value, the number of questions retrieved.
    ```bash
    {
    "current_category": "None",
    "questions": [
        {
        "answer": "Maya Angelou",
        "category": 4,
        "difficulty": 2,
        "id": 5,
        "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },
        {
        "answer": "Edward Scissorhands",
        "category": 5,
        "difficulty": 3,
        "id": 6,
        "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        }
    ],
    "success": true,
    "total_questions": 2
    }
    ```
<br><br>

#### Play the trivia game
- **POST /quizzes**
- Retruns random questions from a specific category or all the categories for the user to play the trivia game.
- Arguments 
        - previous_questions (*required*)
        - quiz_category (*required*)<br><br>
    - Example
        - The *previous_questions* argument can be an empty list
        - `curl -X POST -H "Content-Type: application/json" -d '{"previous_questions":[20], "quiz_category":{ "type": "science", "id": "1" }}' http://127.0.0.1:5000/quizzes` <br><br>
    - Returns: The success state and remaining questions (if they exist).
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
        - If all the questions have been exhausted, it returns an empty question and the game ends
        - ```bash
            {
            "question": "",
            "success": true
            }
            ```
<br><br>

