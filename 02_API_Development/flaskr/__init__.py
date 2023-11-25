from flask import Flask,jsonify
import os

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite')
    )

    @app.route('/')
    def hello_world():
        return jsonify({'message':'Hello, World!'})

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

# $env:FLASK_APP="flaskr"
# $env:FLASK_ENV="development"
