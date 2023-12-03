import json
import math
import os
import unittest
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}/{}".format('localhost:5432', self.database_name)
        # Link the test database to the app instead of creating the db twice
        self.app = create_app(db_name=self.database_path)
        self.client = self.app.test_client

        # Parameters to create a new question
        self.new_question = {"question": "Which organ is responsible for pumping blood in the body", "answer": "The Heart", "difficulty": 3, "category": 1}
    

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    # ------------------------------------------------------------ Tests for getting categories ------------------------------------------------------------
    def test_get_all_existing_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["categories"])
    

    def test_get_non_existent_categories(self):
        '''Perform a get request for a wrong route name'''
        res = self.client().get("/category")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")



    # ------------------------------------------------------------ Tests for getting questions from specific categories ------------------------------------------------------------
    def test_get_question_from_valid_category(self):
        cat_id = 2
        res = self.client().get(f"/categories/{cat_id}/questions")
        data = json.loads(res.data)

        # Get the name of the category from the db
        with self.app.app_context():
            cat_type = Category.query.filter(Category.id == cat_id).all()[0].type

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertTrue(data["totalQuestions"])
        self.assertTrue(data["currentCategory"],cat_type)
    
    def test_get_question_from_invalid_category(self):
        cat_id = 1000
        res = self.client().get(f"/categories/{cat_id}/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "bad request")



    # ------------------------------------------------------------ Tests for getting questions ------------------------------------------------------------
    def test_get_all_existing_questions(self):
        res = self.client().get("/questions?page=2")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["categories"])


    def test_404_get_all_nonexistent_questions(self):
        '''Perform a get request for a page that doesn't exist'''
        res = self.client().get("/questions?page=1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")
    


    # ------------------------------------------------------------ Tests for deleting questions ------------------------------------------------------------
    def test_delete_existing_question(self):
        '''
        This test verifies that an existing question can be deleted 
            - It's configured to delete the last entry to the db
            - To keep the `trivia_test` db length static, I post a new book before calling DELETE
        '''
        # POST request to keep db length static
        post_question = self.client().post('/questions',json=self.new_question)

        # Get the id of the last row in the test_db
        res0 = self.client().get('/questions')
        data0 = json.loads(res0.data)
        max_pages = math.ceil(data0['total_questions']/10) # 10 is the number of questions per page

        # Perform a get request on the last page of questions
        res1 = self.client().get(f'/questions?page={max_pages}')
        data1 = json.loads(res1.data)
        # Extract the id of the last question on the last page. 
        # The original question list is sorted by id, sorting it by category willnot delete the last added question
        last_id = data1['questions'][-1]['id'] 

        # Perform the delete request on the last id. This should default
        res = self.client().delete(f'/questions/{last_id}')
        data = json.loads(res.data)

        # Load the book rating from the db and confirm if it has been deleted
        with self.app.app_context():
            question = Question.query.filter(Question.id == last_id).one_or_none()
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        # Check that the deleted book.id matches the id specified in the request
        self.assertEqual(data['deleted'], last_id)
        # Check that the deleted book id from the db is None
        self.assertEqual(question, None)

    def test_422_delete_nonexistent_question(self):
        res = self.client().delete(f'/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")


    
    # ------------------------------------------------------------ Tests for posting questions ------------------------------------------------------------
    def test_post_valid_question(self):
        '''
        This test verifies that a new question can be posted successfully
            - The POST request always includes a new entry to the db, so I included a 
              DELETE request beneath it to keep the trivia_test db length static
        '''
        res = self.client().post('/questions',json=self.new_question)
        data = json.loads(res.data)

        # Delete step
        max_pages = math.ceil(data['total_questions']/10)
        get_res = self.client().get(f'/questions?page={max_pages}')
        get_data = json.loads(get_res.data)
        last_id = get_data['questions'][-1]['id']
        del_res = self.client().delete(f'/questions/{last_id}')

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])
        self.assertTrue(data["current_category"])
    
    def test_400_post_invalid_question(self):
        '''
        This test verifies that an question cannot be posted to the db
            - The question value in the JSON is set to None
        '''
        invalid_question = self.new_question.copy()
        invalid_question['question'] = None

        res = self.client().post('/questions',json=invalid_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "bad request")


    
    # ------------------------------------------------------------ Tests for searching for questions ------------------------------------------------------------
    def test_post_search_existing_question(self):
        question_search = 'What is'
        res = self.client().post('/questions',json={'searchTerm': question_search})
        data = json.loads(res.data)

        # Check that the number of returned questions match the ones in the db
        with self.app.app_context():
            count_questions = Question.query.filter(Question.question.ilike(f"%{question_search}%")).count()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'],count_questions)

    
    def test_post_search_nonexistent_question(self):
        question_search = 'Paleontology'
        res = self.client().post('/questions',json={'searchTerm': question_search})
        data = json.loads(res.data)

        # Check that the number of returned questions match the ones in the db
        with self.app.app_context():
            count_questions = Question.query.filter(Question.question.ilike(f"%{question_search}%")).count()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['questions'],[])
        self.assertEqual(data['total_questions'],count_questions)


    
    # ------------------------------------------------------------ Tests for playing the trivia game ------------------------------------------------------------
    def test_play_trivia_using_all_categories(self):
        '''
        This test is for playing the trivia game when all the categories are selection
        '''

        res = self.client().post('/quizzes',json={"previous_questions":[], "quiz_category":{ "type": "all", "id": "0" }})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
    
    def test_play_trivia_specific_category_with_remaining_questions(self):
        '''
        This test is for playing the trivia game when questions are available in the specified category
        '''

        res = self.client().post('/quizzes',json={"previous_questions":[20], "quiz_category":{ "type": "science", "id": "1" }})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
    
    def test_play_trivia_without_remaining_questions(self):
        '''
        This test is for playing the trivia game when all questions in the specified category have been exhausted.
        The frontend triggers the end of the game
        '''

        res = self.client().post('/quizzes',json={"previous_questions":[20,21,22], "quiz_category":{ "type": "science", "id": "1" }})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['question'], '')
    
    def test_400_play_trivia_unspecified_category(self):
        '''
        This test is for checking that the code returns an error if the request is incorrect
        '''

        res = self.client().post('/quizzes',json={"previous_questions":[]})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "bad request")
    


    def tearDown(self):
        """Executed after reach test"""
        pass


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()