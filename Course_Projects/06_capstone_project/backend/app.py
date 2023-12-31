import os
from flask import Flask, request, abort, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix
# from flask.request import get


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__, template_folder='templates/')
  CORS(app, resources={r"/api/*": {"origins": "*"}})

  return app

app: Flask = create_app()


@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization,true")
    response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,PATCH,DELETE,OPTIONS")
    
    return response

# Use the ProxyFix middleware to handle the reverse proxy
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1)

SITE_NAME = '127.0.0.1'

# Define proxy server.
# @app.route('/', defaults={'path': ''})
# @app.route('/<path:path>', methods=['GET','POST','PUT','DELETE'])
# def proxy(path):
#   response = request.get_json(f'{SITE_NAME}{path}')
#   print(response)
#   return response

@app.route("/home")
def index():
   # return jsonify("This is the index")
   return render_template("index.html")

@app.route("/appointments")
def get_bookings():
   # return jsonify("This is the index")
   return render_template("booking.html")


# POST new booking to the db
@app.route("/appointments/book", methods=['POST'])
def create_new_booking():
   resp = request.get_json()
   print(resp)
   return jsonify("The post request is working")
#    return render_template("booking.html")


# GET existing booking fro the DB
@app.route('/appointments/<date>')
def create_availability(date):
   # List of all available times
   all_times = ["09:00 AM", "10:00 AM", "11:00 AM", 
                           "12:00 PM", "01:00 PM", "02:00 PM", 
                           "03:00 PM", "04:00 PM", "05:00 PM", "06:00 PM"]
   
   # In a real application, you would query your database to get the list of booked times
   booked_times = ["01:00 PM", "02:00 PM", "03:00 PM"]#get_booked_times_from_database(date)
   # return render_template('booking.html', available_times=available_times, booked_times=booked_times)
   # Send JSON response containing available times to the client
   return jsonify({'all_times': all_times, 'booked_times': booked_times})

# @TODO
def get_booked_times_from_database(date):
   # Query the database for the particular date and get all the booked timeslots
   pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)