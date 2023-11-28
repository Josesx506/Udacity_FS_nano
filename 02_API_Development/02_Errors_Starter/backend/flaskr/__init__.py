from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Book, database_path

BOOKS_PER_SHELF = 8
db_name = database_path


def paginate_books(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * BOOKS_PER_SHELF
    end = start + BOOKS_PER_SHELF

    books = [book.format() for book in selection]
    current_books = books[start:end]

    return current_books


def create_app(test_config=None,db_name=db_name):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app,db_name)
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

    @app.route("/books")
    def retrieve_books():
        selection = Book.query.order_by(Book.id).all()
        current_books = paginate_books(request, selection)

        if len(current_books) == 0:
            abort(404)

        return jsonify(
            {
                "success": True,
                "books": current_books,
                "total_books": len(Book.query.all()),
            }
        )

    @app.route("/books/<int:book_id>", methods=["PATCH"])
    def update_book(book_id):

        body = request.get_json()

        try:
            book = Book.query.filter(Book.id == int(book_id)).one_or_none()
            if book is None:
                abort(404)

            if "rating" in body:
                book.rating = int(body.get("rating"))

            book.update()

            return jsonify(
                {
                    "success": True,
                }
            )

        except:
            abort(400)

    @app.route("/books/<int:book_id>", methods=["DELETE"])
    def delete_book(book_id):
        try:
            book = Book.query.filter(Book.id == book_id).one_or_none()

            if book is None:
                abort(404)

            book.delete()
            selection = Book.query.order_by(Book.id).all()
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

    @app.route("/books", methods=["POST"])
    def create_book():
        body = request.get_json()

        new_title = body.get("title", None)
        new_author = body.get("author", None)
        new_rating = body.get("rating", None)

        try:
            book = Book(title=new_title, author=new_author, rating=new_rating)
            book.insert()

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

    # TEST: Practice writing curl requests. Write some requests that you know will error in expected ways.
    #       Make sure they are returning as expected. Do the same for other misformatted requests or requests missing data.
    #       If you find any error responses returning as HTML, write new error handlers for them.

    return app
