import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category, database_path

QUESTIONS_PER_PAGE = 10
db_name = database_path

def paginate_questions(request, selection):
    '''
    Paginate the questions shown on the page
    '''
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions

def create_app(test_config=None,db_name=db_name):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app,db_name)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization,true")
        response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,PATCH,DELETE,OPTIONS")
        
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route("/categories")
    def get_categories():
        '''
        Performs GET requests to access all the categories in the db
        '''
        selection_category = Category.query.order_by(Category.id).all()
        current_categories = {cat.format()['id']:cat.format()['type'] for cat in selection_category}

        if len(current_categories) == 0:
            abort(404)

        # categories must be passed as a dictionary so that a loop can be applied on the keys and values
        # passing it as a list causes an error with the indexing
        return jsonify(
            {
                "success": True,
                "categories": current_categories
            }
        )

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route("/questions")
    def get_questions():
        '''
        Performs GET requests to access all the questions in the db
        '''
        selection_question = Question.query.order_by(Question.category).all()
        current_questions = paginate_questions(request, selection_question)
        selection_category = Category.query.order_by(Category.id).all()
        all_categories =  {cat.format()['id']:cat.format()['type'] for cat in selection_category}

        if len(current_questions) == 0:
            abort(404)

        return jsonify(
            {
                "success": True,
                "questions": current_questions,
                "totalQuestions": len(Question.query.all()),
                "categories": all_categories,
                "currentCategory": None,
            }
        )

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route("/questions/<int:q_id>")
    def delete_question(q_id):
        '''
        Implements delete requests based on a question id
        '''
        try:
            question = Question.query.filter(Question.id == q_id).one_or_none()

            if question is None:
                abort(404)

            question.delete()

            # The front end is used to call the `get_questions()` again which refreshes the view
            # Hence there's no need to query the db to return remaining question
            return jsonify(
                {
                    "success": True,
                    "deleted": q_id,
                }
            )

        except:
            abort(422)

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route("/categories/<int:cat_id>/questions")
    def get_questions_by_category(cat_id):
        '''
        I added 1 to the id because the react app is using zero indexing to call the category ids, while the id numbers start from 1 in the db
        '''
        dict_ids = {0:1,1:2,2:3,3:4,4:5,5:6}
        selection_question = Question.query.filter(Question.category == cat_id).order_by(Question.category).all()
        current_questions = paginate_questions(request, selection_question)
        current_category = Category.query.filter(Category.id == cat_id).one_or_none()

        if len(current_questions) == 0:
            abort(404)

        return jsonify(
            {
                "success": True,
                "questions": current_questions,
                "totalQuestions": len(selection_question),
                "currentCategory": current_category.type,
            }
        )


    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    return app

