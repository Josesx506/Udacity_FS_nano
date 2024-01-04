import os
import json
from flask import Flask, request, abort, jsonify, render_template
from datetime import datetime,timedelta
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
def format_revocal_events(items):
   '''Format the data from the db to match the required pattern to be rendered on the front end'''
   class str2(str):
      def __repr__(self):
         return ''.join(('"', super().__repr__()[1:-1], '"'))
   
   for k,v in enumerate(items):
      v['id'] = str(v["id"])
      v['name'] = f"Hair Appointment #{v['id']}"
      v['start_time'] = datetime.strftime( v['start_time'], '%m-%d-%Y %I:%M %p')
      v['date'] = str2(v['start_time'].split(" ")[0].replace('-','/'))
      v['time'] = " ".join(v['start_time'].split(" ")[1:])
      # v['description'] = f"<span><b>Time:</b>{v['time']}\t <b>Name:</b> {v['first_name']} {v['last_name']}</span>"
      v['description'] = f"Time: {v['time']}\t Name: {v['first_name']} {v['last_name']}"
      v['type'] = 'event'
   return items


@app.route("/appointments")
def get_bookings():
   '''
   This is a simple get request to create the first page
   I limited the Jinja use to a minimum because it was causing interference with js
   '''
   allEvents = Booking.query.order_by(Booking.id).all()
   currentEvents = [event.format() for event in allEvents]
   currentEvents = format_revocal_events(currentEvents)
   
   return render_template("booking.html" )


@app.route("/appointments/refresh")
def update_appointments_page():
   allEvents = Booking.query.order_by(Booking.id).all()
   currentEvents = [event.format() for event in allEvents]
   currentEvents = format_revocal_events(currentEvents)

   return jsonify({'booked_slots': currentEvents})





# POST new booking to the db
@app.route("/appointments/book", methods=['POST'])
def create_new_booking():
   '''Get the responses'''
   resp = request.get_json()

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



# PATCH existing booking in the db
@app.route("/appointments/book/<int:b_id>", methods=['PATCH'])
def update_existing_booking(b_id):
   '''Update parameters for an existing timeslot in the db'''
   resp = request.get_json()

   # Check the validity of the request to confirm there are no errors
   if b_id is None:
      abort(400)

   try:
      # This only works for valid booking ids
      # Extract the booking that matches the specified id
      current_booking = Booking.query.filter(Booking.id == b_id).all()[0]

      # Parameters to create a new drink. Check for None values
      for key,value in resp.items():
         if key!='id' and key!='start_time' and value is not None:
            setattr(current_booking, key, value)
         elif key=="start_time" and value is not None:
            setattr(current_booking, key, f"{datetime.strptime(value, '%m-%d-%Y %I:%M %p')}")
         
         # Update the row
         current_booking.update()
         
         # Extract the updated drink long format
         updated_booking = [current_booking.format()]

         # Create the additional attributes
         fmtrd_booking = format_revocal_events(updated_booking)


      return jsonify(
         {
               "success": True,
               "event": fmtrd_booking,
         })
   except:
      abort(422)

   

# DELETE existing booking in the db
@app.route("/appointments/book/<int:b_id>", methods=['DELETE'])
def delete_existing_booking(b_id):
   # Check the validity of the request to confirm there are no errors
   if b_id is None:
      abort(400)

   try:
      del_booking = Booking.query.filter(Booking.id == b_id).one_or_none()

      if del_booking is None:
            abort(404)

      del_booking.delete()
        
      return jsonify({'success': True,
                      "delete": b_id})

   except:
        abort(422)



# GET existing booking from the DB
@app.route('/appointments/<date>')
def create_availability(date):
   '''
   This function returns booked timeslots that the frontend can use to restrict booking availability.
      booked_times = ["01:00 PM", "02:00 PM", "03:00 PM"]
   '''
   # List of all available times
   all_times = ["09:00 AM", "10:00 AM", "11:00 AM", 
                           "12:00 PM", "01:00 PM", "02:00 PM", 
                           "03:00 PM", "04:00 PM", "05:00 PM", "06:00 PM"]
   
   # In a real application, you would query your database to get the list of booked times
   booked_times = get_booked_times_from_database(date)
   
   return jsonify({'all_times': all_times, 'booked_times': booked_times})





def get_booked_times_from_database(date):
   '''
   Query the database for the particular date and get all the booked timeslots which affects 
   what future timeslots that the customer can select
   '''
   fmt_date = datetime.strptime(date, "%m-%d-%Y")
   start_of_day = datetime.combine(fmt_date, datetime.min.time())
   end_of_day = datetime.combine(fmt_date + timedelta(days=1), datetime.min.time())
   
   # Perform the sql query
   booked_events = Booking.query.filter(Booking.start_time.between(start_of_day.date(), 
                                                end_of_day.date())).order_by(Booking.start_time).all()
   
   if len(booked_events)>0:
      booked_events = [event.format() for event in booked_events]
      booked_events = format_revocal_events(booked_events)
      unavailable_timeslots = [event['time'] for event in booked_events]
      return unavailable_timeslots

   else:
      return []
   

# @TODO - Patch and Delete requests


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)