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

        try:
            selection_category = Category.query.order_by(Category.id).all()
            current_categories = {cat.format()['id']:cat.format()['type'] for cat in selection_category}

            if len(current_categories) == 0:
                abort(404)
            
            else:
                # categories must be passed as a dictionary so that a loop can be applied on the keys and values
                # passing it as a list causes an error with the indexing
                return jsonify(
                    {
                        "success": True,
                        "categories": current_categories
                    }
                )
        except:
            abort(400)

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
        selection_question = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection_question)
        selection_category = Category.query.order_by(Category.id).all()
        all_categories =  {cat.format()['id']:cat.format()['type'] for cat in selection_category}

        if len(current_questions) == 0:
            abort(404)

        else:
            return jsonify(
                {
                    "success": True,
                    "questions": current_questions,
                    "total_questions": len(selection_question),
                    "categories": all_categories,
                    "current_category": 'None',
                }
            )

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route("/questions/<int:q_id>", methods=['DELETE'])
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
    @app.route("/questions", methods=['POST'])
    def post_question():
        '''
        This function implements the post requests for adding a new book and searching for trivia questions in the db
        '''
        body = request.get_json()

        # Parameters to create a new question
        new_question = body.get("question", None)
        new_answer = body.get("answer", None)
        new_difficulty = body.get("difficulty", None)
        new_category = body.get("category", None)

        # Parameters to search for a question in the db
        search_question = body.get("searchTerm", None)

        # Check the validity of the request to confirm there are no errors
        if search_question is None and new_question is None:
            abort(400)

        try:
            if search_question is not None:
                selection = Question.query.order_by(Question.id).filter(Question.question.ilike(f"%{search_question}%"))
                questions = paginate_questions(request, selection)
                return jsonify(
                    {
                        "success": True,
                        "questions": questions,
                        "total_questions": selection.count(),
                        "current_category": 'None',
                    })
            
            elif new_question is not None:
                    question = Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_difficulty)
                    question.insert()

                    selection_question = Question.query.order_by(Question.category).all()
                    current_questions = paginate_questions(request, selection_question)
                    selection_category = Category.query.order_by(Category.id).all()
                    all_categories =  {cat.format()['id']:cat.format()['type'] for cat in selection_category}

                    return jsonify(
                        {
                            "success": True,
                            "questions": current_questions,
                            "total_questions": len(selection_question),
                            "categories": all_categories,
                            "current_category": new_category,
                        }
                    )
            else:
                abort(422)
        except:
            abort(422)

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
        all_categories = Category.query.order_by(Category.id).all()
        category_ids = [cat.format()['id'] for cat in all_categories]

        # If the category id is not in the category table indicate that the request is bad
        if cat_id not in category_ids:
            abort(400)

        selection_question = Question.query.filter(Question.category == cat_id).order_by(Question.category).all()
        current_questions = paginate_questions(request, selection_question)
        current_category = Category.query.filter(Category.id == cat_id).one_or_none()

        # If there are no questions for the specified category, indicate the resource is not available
        if len(current_questions) == 0:
            abort(404)

        else:
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
    @app.route("/quizzes", methods=['POST'])
    def post_quiz_game():
        body = request.get_json()

        prev_questions =  body.get("previous_questions", None) # This is a list of previous question ids
        category =  body.get("quiz_category", None)

        if category is not None:
            # Extract the category name and id from the json data. The category type/name is not used
            cat_type = category['type']
            cat_id = int(category['id'])

        else:
            abort(400)
        

        try:
            if cat_id == 0:

                # This is for all the question categories
                category_questions = Question.query.all()
                all_question_ids = [question.format()['id'] for question in category_questions]

                # Extract the list of remaining questions that haven't been asked
                remaining_question_ids = list(set(all_question_ids).difference(prev_questions))

                # Randomly select a question id from the list of remaining question ids
                if len(remaining_question_ids) != 0 :
                    future_question_id = random.choice(remaining_question_ids)
                    question = Question.query.filter(Question.id == future_question_id).all()[0]

                    return jsonify(
                        {
                            "success": True,
                            "question": question.format(),
                        }
                    )
                
                # Else return an empty question key to the frontend
                else:
                    return jsonify(
                        {
                            "success": True,
                            "question": '',
                        }
                    )
            
            elif cat_id > 0:

                # This is for specific question categories
                category_questions = Question.query.filter(Question.category == cat_id).all()
                all_question_ids = [question.format()['id'] for question in category_questions]

                # Extract the list of remaining questions that haven't been asked
                remaining_question_ids = list(set(all_question_ids).difference(prev_questions))

                # Randomly select a question id from the list of remaining question ids
                if len(remaining_question_ids) != 0 :
                    future_question_id = random.choice(remaining_question_ids)
                    question = Question.query.filter(Question.id == future_question_id).all()[0]

                    return jsonify(
                        {
                            "success": True,
                            "question": question.format(),
                        }
                    )
                
                # Else return an empty question key to the frontend
                else:
                    return jsonify(
                        {
                            "success": True,
                            "question": '',
                        }
                    )

            else:
                abort(404)
        except:
            abort(422)

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "bad request"}), 400

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "resource not found"}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "unprocessable"}),
            422,
        )

    return app

