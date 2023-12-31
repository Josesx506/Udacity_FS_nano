import os
from flask import Flask, request, abort, jsonify, render_template
from datetime import datetime
# from flask_moment import Moment
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix
import sys

# Setup the python file path to enable importing the system variables
sys.path.append(os.getcwd())
from models import setup_db, db, Booking, Service, Stylist,  database_path
db_name = database_path


# ---------------------------------------- Create the Flask app ----------------------------------------
def create_app(test_config=None, db_name=db_name):
  # create and configure the app
  app = Flask(__name__, template_folder='templates/')
  setup_db(app,db_name)
  migrate = Migrate(app, db) # Track changes
  CORS(app, resources={r"/api/*": {"origins": "*"}})
  return app


app: Flask = create_app()


@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization,true")
    response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,PATCH,DELETE,OPTIONS")
    return response

# date_string = "12-31-2023 09:00 AM"
# Convert the string to a datetime object
#  datetime_obj = datetime.strptime(date_string, '%m-%d-%Y %I:%M %p')

@app.route("/home")
def index():
   # return jsonify("This is the index")
   return render_template("index.html")

# ------------------------------------------------------ APPOINTMENTS ------------------------------------------------------
@app.route("/appointments")
def get_bookings():
   allEvents = Booking.query.order_by(Booking.id).all()
   currentEvents = [event.format() for event in allEvents]
   currentEvents = format_revocal_events(currentEvents)
   
   # currentEvents = [item['date']=]
   # pas = datetime.strftime(datetime(2024, 1, 4, 10, 0), '%m-%d-%Y %I:%M %p')
   print(currentEvents,"\n\n\n")
   # return jsonify("This is the index")
   return render_template("booking.html", eventsdb=currentEvents)


def format_revocal_events(items):
   '''Format the data from the db to match the required pattern to be rendered on the front end'''
   for k,v in enumerate(items):
      v['id'] = str(v["id"])
      v['name'] = "Hair Appointment"
      v['start_time'] = datetime.strftime( v['start_time'], '%m-%d-%Y %I:%M %p')
      v['date'] = v['start_time'].split(" ")[0].replace("-","/")
      v['time'] = " ".join(v['start_time'].split(" ")[1:])
      v['description'] = f"<b>Time:</b>{v['time']}\n <b>Name:</b> {v['first_name']} {v['last_name']}"
      v['type'] = 'event'
   return items


# POST new booking to the db
@app.route("/appointments/book", methods=['POST'])
def create_new_booking():
   resp = request.get_json()
   print(resp,"\n","\n","\n")

   # Check the validity of the request to confirm there are no errors
   if resp['date_time'] is None:
      abort(400)

   try:
      if resp['first'] is not None:
            new_booking=Booking(first_name=resp['first'],
                        last_name=resp['last'],
                        phone=resp['phone'],
                        email=resp['email'],
                        start_time= f"{datetime.strptime(resp['date_time'], '%m-%d-%Y %I:%M %p')}",
                        completed=False,
                        stylist_id=None)
            new_booking.insert()

            # Extract the last drink from the db
            recent_booking = Booking.query.order_by(Booking.id.desc()).first()
            latest_booking = [recent_booking.format()]

            # Create the additional attributes
            latest_booking = format_revocal_events(latest_booking)

            return jsonify(
               {
                  "success": True,
                  "event": latest_booking,
               })
      else:
         abort(422)
   except:
      abort(422)
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