from flask import Flask,jsonify
from flask_cors import CORS
import os

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite')
    )

    # Implement CORS by calling the class and including the app as an argument
    # Setting the origins to "*" will allow all websites, which is not recommended for security
    # The keys or the resource dictionary are uri's that can access a resource.
    # In this example, any uri with /api can accessed by any origin for public use of the api
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    # CORS Headers - After a request is received, run these methods
    @app.after_request
    def after_request(response):
        # This first command allows you to specify the content type and authorization in a request
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        # The second command allows you to implement the `methods` below. Note: It doesn't support PUT requests
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        # The response must be return
        return response
    
    # To implement CORS on a specific route-name, use the @cross_origin() decorator
    @app.route('/messages')
    @cross_origin()
    def get_messages():
        return 'GETTING MESSAGES'

    @app.route('/')
    def hello_world():
        return jsonify({'message':'Hello, World!'})
    
    def create_greeting():
        return jsonify({'message':'Greeting'})
    
    def send_greeting():
        # If there was a db connected it'll commit to the db
        return None
    
    @app.route('/', methods=['GET', 'POST'])
    def multi_greeting():
        if request.method == 'POST':
            return create_greeting()
        else:
            return send_greeting()

    @app.route('/smiley')
    def smiley():
        return (':)')
    
    # Include a config file
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    
    # Make the instance path directory. The app will create the database file within that directory so it needs to exist.
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    return app
