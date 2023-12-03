#!/bin/bash

# This sets up the FLASK app. Execute it with `source setup_flask.sh`
export FLASK_APP=backend/flaskr;
export FLASK_DEBUG=True; 
export FLASK_ENV=development;
echo $FLASK_APP