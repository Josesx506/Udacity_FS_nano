import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink, Barista
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
db_drop_and_create_all(app)

# ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route("/drinks")
def get_drinks():
    '''
    Performs GET requests to access all the drinks in the db
    '''

    try:
        with app.app_context():
            all_drinks = Drink.query.order_by(Drink.id).all()
            current_drinks = [drink.short() for drink in all_drinks]

        if len(current_drinks) == 0:
            abort(404)
        
        else:
            # drinks are passed as a list that is formatted to return the short form of the drink type
            return jsonify(
                {
                    "success": True,
                    "drinks": current_drinks
                }
            )
    except:
        abort(400)

'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route("/drinks-detail")
@requires_auth('get:drinks-detail')
def get_drinks_details(jwt):
    '''
    Performs GET requests to access all the drinks in the db
    '''

    try:
        with app.app_context():
            all_drinks = Drink.query.order_by(Drink.id).all()
            current_drinks = [drink.long() for drink in all_drinks]

        if len(current_drinks) == 0:
            abort(404)
        
        else:
            # drinks are passed as a list that is formatted to return the long form of the drink type
            return jsonify(
                {
                    "success": True,
                    "drinks": current_drinks
                }
            )
    except:
        abort(400)

'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route("/drinks", methods=['POST'])
@requires_auth('post:drinks')
def post_drink(jwt):
    '''
    This function implements the post requests for adding a new drink to the db
    '''
    body = request.get_json()

    # Parameters to create a new drink
    new_title = body.get("title", None)
    new_recipe = str(body.get("recipe", None)).replace("'", '"') # Replace single quotes with double quotes

    # Check the validity of the request to confirm there are no errors
    if new_title is None:
        abort(400)

    try:
        if new_title is not None:
            with app.app_context():
                new_drink = Drink(title=new_title, recipe=new_recipe)
                new_drink.insert()

                # Extract the last drink from the db
                recent_drink = Drink.query.order_by(Drink.id.desc()).first()
                current_drink = [recent_drink.long()]

            return jsonify(
                {
                    "success": True,
                    "drinks": current_drink,
                }
            )
        else:
            abort(422)
    except:
        abort(422)

'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:d_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def patch_drinks(jwt, d_id):
    '''
    This function implements the patch requests for editing an existing drink in the db
    It uses a specified drink id (d_id)
    '''
    body = request.get_json()

    # Parameters to create a new drink
    updt_title = body.get("title", None)
    updt_recipe = str(body.get("recipe", None)).replace("'", '"')

    # Check the validity of the request to confirm there are no errors
    if d_id is None:
        abort(400)

    try:
         # This only works for valid drink ids
        with app.app_context():
            # Extract the drink that matches the specified id
            current_drink = Drink.query.filter(Drink.id == d_id).all()[0]

            # Parameters to create a new drink. Check for None values
            for key,value in body.items():
                if key!='id' and key!='recipe' and value is not None:
                    setattr(current_drink, key, value)
                elif key=="recipe" and value is not None:
                    setattr(current_drink, key, str(value).replace("'", '"'))
            
            # Update the row
            current_drink.update()
            
            # Extract the updated drink long format
            updated_drink = [current_drink.long()]

        return jsonify(
            {
                "success": True,
                "drinks": updated_drink,
            })
    except:
        abort(422)

'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route("/drinks/<int:d_id>", methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(jwt,d_id):
    '''
    Implements delete requests based on a drink id
    '''
    try:
        with app.app_context():
            drink = Drink.query.filter(Drink.id == d_id).one_or_none()

            if drink is None:
                abort(404)

            drink.delete()
        
        return jsonify(
            {
                "success": True,
                "delete": d_id,
            }
        )

    except:
        abort(422)

# ----------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------- Above and Beyond -----------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------
@app.route("/baristas")
def get_baristas():
    '''
    Performs GET requests to access all the baristas in the db
    '''
    try:
        with app.app_context():
            all_baristas = Barista.query.order_by(Barista.id).all()
            current_baristas = [barista.short() for barista in all_baristas]

        if len(current_baristas) == 0:
            abort(404)
        else:
            # baristas are passed as a list that is formatted to return the short form of the drink type
            return jsonify(
                {
                    "success": True,
                    "baristas": current_baristas
                }
            )
    except:
        abort(400)


@app.route("/baristas", methods=['POST'])
@requires_auth('post:baristas')
def post_barista(jwt):
    '''
    This function implements the post requests for adding a new barista to the db
    '''
    body = request.get_json()

    # Parameters to create a new drink
    new_name = body.get("name", None)
    new_flavors = str(body.get("flavors", None)).replace("'", '"') # Replace single quotes with double quotes
    new_proficiency = int(body.get("proficiency", None))
    new_image_url = body.get("image_url", None)

    # Check the validity of the request to confirm there are no errors
    if new_name is None:
        abort(400)

    try:
        if new_name is not None:
            with app.app_context():
                new_barista = Barista(name=new_name,
                                      flavors=new_flavors,
                                      proficiency=new_proficiency,
                                      image_url=new_image_url)
                new_barista.insert()

                # Extract the last drink from the db
                recent_barista = Barista.query.order_by(Barista.id.desc()).first()
                current_barista = [recent_barista.short()]

            return jsonify(
                {
                    "success": True,
                    "baristas": current_barista,
                }
            )
        else:
            abort(422)
    except:
        abort(422)


@app.route('/baristas/<int:b_id>', methods=['PATCH'])
@requires_auth('patch:baristas')
def patch_baristas(jwt, b_id):
    '''
    This function implements the patch requests for editing an existing barista in the db
    It uses a specified barista id (b_id)
    '''
    body = request.get_json()
    
    # Check the validity of the request to confirm there are no errors
    if b_id is None:
        abort(400)

    try:
        # This only works for valid barista ids
        with app.app_context():
            # Extract the barista that matches the specified id
            current_barista = Barista.query.filter(Barista.id == b_id).all()[0]

            # Parameters to create a new drink. Check for None values
            for key,value in body.items():
                if key!='id' and key!='flavors' and value is not None:
                    setattr(current_barista, key, value)
                elif key=="flavors" and value is not None:
                    setattr(current_barista, key, str(value).replace("'", '"'))
            
            # Update the row
            current_barista.update()
            
            # Extract the updated drink short format
            updated_barista = [current_barista.short()]

        return jsonify(
            {
                "success": True,
                "baristas": updated_barista,
            })
    except:
        abort(422)


@app.route("/baristas/<int:b_id>", methods=['DELETE'])
@requires_auth('delete:baristas')
def delete_baristas(jwt,b_id):
    '''
    Implements delete requests based on a barista id
    '''
    try:
        with app.app_context():
            barista = Barista.query.filter(Barista.id == b_id).one_or_none()

            if barista is None:
                abort(404)

            barista.delete()
        
        return jsonify(
            {
                "success": True,
                "delete": b_id,
            }
        )

    except:
        abort(422)

# ----------------------------------------------------------------------------------------------------------------------------


# Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({"success": False,"error": 422, "message": "unprocessable"}), 422


'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''
@app.errorhandler(400)
def bad_request(error):
    return (jsonify({"success": False, "error": 400, "message": "bad request"}), 400)

'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''
@app.errorhandler(404)
def not_found(error):
    return (jsonify({"success": False, "error": 404, "message": "resource not found, drinks not in the db"}), 404)

'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''
@app.errorhandler(AuthError)
def unprocessable(error):
    return (
        jsonify({"success": False, "error": error.status_code, "message": error.error['description']}),
        error.status_code,
    )