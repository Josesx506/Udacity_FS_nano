import json
import math
import os
import unittest
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Book


class BookTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.database_name = "bookshelf_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format('student', 'student','localhost:5432', self.database_name)
        # Link the test database to the app instead of creating the db twice
        self.app = create_app(db_name=self.database_path)
        self.client = self.app.test_client

        self.new_book = {"title": "Anansi Boys", "author": "Neil Gaiman", "rating": 5}

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_paginated_books(self):
        res = self.client().get("/books")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_books"])
        self.assertTrue(len(data["books"]))

    def test_404_sent_requesting_beyond_valid_page(self):
        res = self.client().get("/books?page=1000", json={"rating": 1})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")

    def test_update_book_rating(self):
        res0 = self.client().get('/books')
        data0 = json.loads(res0.data)
        first_id = data0['books'][0]['id']
        rating = 4

        res = self.client().patch(f'/books/{first_id}',json={'rating': rating})
        data = json.loads(res.data)
        # Load the book rating from the db and confirm if it has been updated
        with self.app.app_context():
            book = Book.query.filter(Book.id == first_id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(book.format()["rating"], rating)

    def test_400_for_failed_update(self):
        res = self.client().patch('/books/1000',json={'ratata': 0})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "bad request")

    def test_delete_book(self):
        # Get the id of the last row in the test_db
        res0 = self.client().get('/books')
        data0 = json.loads(res0.data)
        max_pages = math.ceil(data0['total_books']/8)
        res1 = self.client().get(f'/books?page={max_pages}')
        data1 = json.loads(res1.data)
        last_id = data1['books'][-1]['id']

        res = self.client().delete(f"/books/{last_id}")
        data = json.loads(res.data)

        with self.app.app_context():
            book = Book.query.filter(Book.id == last_id).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], last_id)
        self.assertTrue(data["total_books"])
        self.assertTrue(len(data["books"]))
        self.assertEqual(book, None)

    def test_404_if_book_does_not_exist(self):
        res = self.client().delete("/books/1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    def test_create_new_book(self):
        res = self.client().post("/books", json=self.new_book)
        data = json.loads(res.data)
        pass

    def test_422_if_book_creation_fails(self):
        res = self.client().post("/books", json=self.new_book)
        data = json.loads(res.data)
        pass
    

    # ------------------------------------------------------ Search Query tests ------------------------------------------------------
    # @TODO: Write tests for search - at minimum two
    #        that check a response when there are results and when there are none
    def test_search_existing_book_title(self):
        '''
        This function tests that a valid search request will return the books 
        from the db that match the title name
        '''
        res = self.client().post("/books/search", json={'search_title': 'Anansi Boys'})
        data = json.loads(res.data)

        # Check that the number of return book names match the ones in the db
        with self.app.app_context():
            count = Book.query.filter(Book.title.ilike(f"%{data['title']}%")).count()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["count"],count)
        self.assertTrue(data["title"])
        self.assertTrue(len(data["books"]))

    
    def test_search_nonexistent_book_title(self):
        '''
        This function checks that the correct error status code is reached if an 
        invalid book title search is performed
        '''

        res = self.client().post("/books/search", json={'searches': None})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "bad request")





# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
