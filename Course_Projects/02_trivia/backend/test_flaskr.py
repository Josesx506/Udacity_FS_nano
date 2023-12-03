import os
import unittest
import json
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

    def test_get_all_existing_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["categories"])
    

    def test_get_non_existent_categories(self):
        res = self.client().get("/category")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")
    
    def tearDown(self):
        """Executed after reach test"""
        pass


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()