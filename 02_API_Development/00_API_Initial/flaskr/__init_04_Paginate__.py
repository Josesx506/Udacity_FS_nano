from flask import Flask,jsonify, request, abort
from flask_cors import CORS
from flaskr.models import setup_db, Plant
import os

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    # Setup the db. Note: This is not using flask-migrate
    setup_db(app)
    # Initialize CORS without a resources argument
    cors = CORS(app)

    # Define CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, PATCH, POST, DELETE, OPTIONS')
        return response
    
    @app.route('/plants', methods=['GET','POST'])
    def get_plants():
        # Use `Pagination` to print out only the first 10 results.
        # # This can help to reduce the amount of data shown on a webpage at once 
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * 10
        end = start + 10
        plants = Plant.query.all()
        formatted_plants = [plant.format() for plant in plants]

        return jsonify({'success': True, 
                        # It applies an index filter to the list to limit the curl response with pagination
                        'plants': formatted_plants[start:end], 
                        'total_plants': len(formatted_plants)})
    
    @app.route('/plants/<int:plant_id>')
    def get_specific_plant(plant_id):
        plant = Plant.query.filter(Plant.id == plant_id).one_or_none()

        # Include error messages in tests
        if plant is None:
            abort(404)
        
        return jsonify({'success': True, 
                        'plant': plant.format()})
    
    return app
