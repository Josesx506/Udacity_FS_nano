import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy  # , or_
from flask_cors import CORS
import random

from models import setup_db, Book

BOOKS_PER_SHELF = 8

def paginate_books(request, selection):
    # Helper function that is used repeatedly
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * BOOKS_PER_SHELF
    end = start + BOOKS_PER_SHELF

    books = [book.format() for book in selection]
    current_books = books[start:end]

    return current_books

# @TODO: General Instructions
#   - As you're creating endpoints, define them and then search for 'TODO' within the frontend to update the endpoints there.
#     If you do not update the endpoints, the lab will not work - of no fault of your API code!
#   - Make sure for each route that you're thinking through when to abort and with which kind of error
#   - If you change any of the response body keys, make sure you update the frontend to correspond.


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    # @TODO: Write a route that retrivies all books, paginated.
    #         You can use the constant above to paginate by eight books.
    #         If you decide to change the number of books per page,
    #         update the frontend to handle additional books in the styling and pagination
    #         Response body keys: 'success', 'books' and 'total_books'
    # TEST: When completed, the webpage will display books including title, author, and rating shown as stars
    @app.route("/books")
    def retrieve_books():
        selection = Book.query.order_by(Book.id).all()
        # Use `Pagination` to print out only the first 8 books per page.
        current_books = paginate_books(request, selection)
        
        # Return a 404 error if the page number is invalid
        if len(current_books) == 0:
            abort(404)

        return jsonify(
            {
                "success": True,
                "books": current_books,
                "total_books": len(Book.query.all()),
            }
        )

    # @TODO: Write a route that will update a single book's rating.
    #         It should only be able to update the rating, not the entire representation
    #         and should follow API design principles regarding method and route.
    #         Response body keys: 'success'
    # TEST: When completed, you will be able to click on stars to update a book's rating and it will persist after refresh
    @app.route("/books/<int:book_id>", methods=["PATCH"])
    def update_book(book_id):

        body = request.get_json()

        try:
            book = Book.query.filter(Book.id == book_id).one_or_none()
            if book is None:
                abort(404)

            # Check if the request has a 'rating' key and convert it from string to integer
            if "rating" in body:
                book.rating = int(body.get("rating"))

            # Update the db
            book.update()

            # Alert the user about the id of the book that was changed
            return jsonify({"success": True, "id": book.id})

        except:
            abort(400)

    # @TODO: Write a route that will delete a single book.
    #        Response body keys: 'success', 'deleted'(id of deleted book), 'books' and 'total_books'
    #        Response body keys: 'success', 'books' and 'total_books'

    # TEST: When completed, you will be able to delete a single book by clicking on the trashcan.
    @app.route("/books/<int:book_id>", methods=["DELETE"])
    def delete_book(book_id):
        try:
            book = Book.query.filter(Book.id == book_id).one_or_none()

            if book is None:
                abort(404)

            book.delete()
            selection = Book.query.order_by(Book.id).all()
            # The pagination helps to refresh the number of books shown after each deletion
            current_books = paginate_books(request, selection)

            return jsonify(
                {
                    "success": True,
                    "deleted": book_id,
                    "books": current_books,
                    "total_books": len(Book.query.all()),
                }
            )

        except:
            abort(422)

    # @TODO: Write a route that create a new book.
    #        Response body keys: 'success', 'created'(id of created book), 'books' and 'total_books'
    # TEST: When completed, you will be able to a new book using the form. Try doing so from the last page of books.
    #       Your new book should show up immediately after you submit it at the end of the page.
    @app.route("/books", methods=["POST"])
    def create_book():
        body = request.get_json()

        new_title = body.get("title", None)
        new_author = body.get("author", None)
        new_rating = body.get("rating", None)

        try:
            # Create the new book
            book = Book(title=new_title, author=new_author, rating=new_rating)
            # Insert it into the db
            book.insert()

            # Reload all the books for the home page view
            selection = Book.query.order_by(Book.id).all()
            current_books = paginate_books(request, selection)

            return jsonify(
                {
                    "success": True,
                    "created": book.id,
                    "books": current_books,
                    "total_books": len(Book.query.all()),
                }
            )

        except:
            abort(422)

    # -----------------------------------------------------------------------------------------------------------------------------
    # ------------------------------------- handling errors in the app instead of using abort -------------------------------------
    # -----------------------------------------------------------------------------------------------------------------------------
    @app.errorhandler(400)
    def bad_request(error):
        # If book cannot be updated
        return jsonify({
            "success": False, 
            "error": 400,
            "message": "bad request, update error"
            }), 400  
    
    @app.errorhandler(404)
    def not_found(error):
        # If a book is not found in the db
        return jsonify({
            "success": False, 
            "error": 404,
            "message": "resource not found"
            }), 404
    
    @app.errorhandler(405)
    def not_allowed(error):
        # If a book is not found in the db
        # This can handle request like `curl -X POST http://127.0.0.1:5000/books/200`
        # Because /books/<book_id> endpoint is defined to handle only PATCH and DELETE requests, it'll raise an error for POST.
        return jsonify({
            "success": False, 
            "error": 405,
            "message": "method not allowed"
            }), 405
    
    @app.errorhandler(422)
    def unprocessable(error):
        # If a book cannot be created or delted from the db
        return jsonify({
            "success": False, 
            "error": 422,
            "message": "unprocessable"
            }), 422

    return app
