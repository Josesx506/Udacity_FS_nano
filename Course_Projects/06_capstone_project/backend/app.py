import os
import json
from flask import Flask, request, abort, jsonify, render_template, session
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
from auth.auth import AuthError, requires_auth
from auth.views import auth_bp
from settings import AUTH0_DOMAIN, LOCAL_SECRET_KEY
db_name = database_path

# Rendering format for Jinja
def to_pretty_json(obj: dict) -> str:
    return json.dumps(obj, default=lambda o: o.__dict__, indent=4)


# ---------------------------------------- Create the Flask app ----------------------------------------
def create_app(test_config=None, db_name=db_name):
  # create and configure the app
  app = Flask(__name__, template_folder='templates/')

  # Setup app authentication
  app.jinja_env.filters['to_pretty_json'] = to_pretty_json
  app.register_blueprint(auth_bp, url_prefix='/')
  app.secret_key = LOCAL_SECRET_KEY

  # Setup app database
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


@app.route("/home")
def index():
   # return jsonify("This is the index")
   return render_template("index.html")



# ------------------------------------------------------ APPOINTMENTS ------------------------------------------------------
def format_revocal_events(items,user_id=''):
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
      if v['user_id'] == user_id:
         v['verified'] = True
      else:
         v['verified'] = False
   return items


@app.route("/appointments")
def get_bookings():
   '''
   This is a simple get request to create the first page
   I limited the Jinja use to a minimum because it was causing interference with js
   '''
   allEvents = Booking.query.order_by(Booking.id).all()
   currentEvents = [event.format() for event in allEvents]
   user_id = session.get('user').get('userinfo')['sub']
   currentEvents = format_revocal_events(currentEvents,user_id)

   roles = session.get('role')
   
   return render_template("booking.html", user_role=roles)



@app.route("/appointments/refresh")
def update_appointments_page():
   allEvents = Booking.query.order_by(Booking.id).all()
   currentEvents = [event.format() for event in allEvents]
   user_id = session.get('user').get('userinfo')['sub']
   currentEvents = format_revocal_events(currentEvents, user_id)
   roles = session.get('role')

   return jsonify({'booked_slots': currentEvents,
                   'roles': roles})





# POST new booking to the db
@app.route("/appointments/book", methods=['POST'])
@requires_auth('post:bookings')
def create_new_booking(jwt):
   '''Get the responses'''
   resp = request.get_json()

   # Check the validity of the request to confirm there are no errors
   if resp['date_time'] is None:
      abort(400)

   # Identify the user id
   user_id = jwt['sub']

   try:
      if resp['first'] is not None:
            new_booking=Booking(first_name=resp['first'],
                        last_name=resp['last'],
                        phone=resp['phone'],
                        email=resp['email'],
                        start_time= f"{datetime.strptime(resp['date_time'], '%m-%d-%Y %I:%M %p')}",
                        completed=False,
                        user_id=user_id,
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
@requires_auth('patch:bookings')
def update_existing_booking(jwt,b_id):
   '''Update parameters for an existing timeslot in the db'''
   resp = request.get_json()

   # Check the validity of the request to confirm there are no errors
   if b_id is None:
      abort(400)

   # Identify the user role and id
   user_role = jwt[f'{AUTH0_DOMAIN}/roles'][0]
   user_id = jwt['sub']

   try:
      # This only works for valid booking ids
      # Extract the booking that matches the specified id
      current_booking = Booking.query.filter(Booking.id == b_id).all()[0]

      # Admin patch update
      if user_role == 'SalonAdmin' or user_role == 'SalonStylist':
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
      
      # User Patch update
      elif user_role == 'SalonUser' and user_id == current_booking.user_id:
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
   
      else:
         abort(403)
   except:
      abort(422)

   

# DELETE existing booking in the db
@app.route("/appointments/book/<int:b_id>", methods=['DELETE'])
@requires_auth('delete:bookings')
def delete_existing_booking(jwt,b_id):

   # Check the validity of the request to confirm there are no errors
   if b_id is None:
      abort(400)
   
   # Identify the user role and id
   user_role = jwt[f'{AUTH0_DOMAIN}/roles'][0]
   user_id = jwt['sub']

   try:
      del_booking = Booking.query.filter(Booking.id == b_id).one_or_none()

      if del_booking is None:
            abort(404)

      # Include permissions for general user to delete
      if user_role == 'SalonAdmin' or user_role == 'SalonStylist':
         del_booking.delete()

         return jsonify({'success': True,
                         "delete": b_id})

      elif user_role == 'SalonUser' and user_id == del_booking.user_id:
         del_booking.delete()

         return jsonify({'success': True,
                         "delete": b_id})
      else:
         abort(403)
   except:
        abort(422)

@app.route('/appointments/verify/<b_id>')
@requires_auth('get:bookings')
def verify_user_event(jwt, b_id):
   '''This function verifies that a user was the one that created an entry'''

   # Check the validity of the request to confirm there are no errors
   if b_id is None:
      abort(400)
   
   # Identify the user role and id
   user_role = jwt[f'{AUTH0_DOMAIN}/roles'][0]
   user_id = jwt['sub']

   try:
      booking_db = Booking.query.filter(Booking.id == b_id,Booking.user_id == user_id).one_or_none()
      booking_id = booking_db.format()['id'] # [event.format()['id'] for event in booking_db]
      if booking_db is not None:
         return jsonify({'success': True,
                         "verified": True,
                         "numbered_id": booking_id})
      else:
         return jsonify({'success': True,
                         "verified": False,
                         "numbered_ids":""})
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
   


# ----------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------ Error Handling ------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------------
'''
Implement error handlers using the @app.errorhandler(error) decorator
   each error handler should return (with approprate messages):
      jsonify({
               "success": False,
               "error": 404,
               "message": "resource not found"
            }), 404

'''


'''
error 400 handler for poorly formatted requests
'''
@app.errorhandler(400)
def bad_request(error):
    return (jsonify({"success": False, "error": 400, "message": "bad request"}), 400)

'''
error 403 handler for mising items in backend
'''
@app.errorhandler(404)
def not_found(error):
    return (jsonify({"success": False, "error": 403, "message": "Forbidden request, you did not create this item"}), 404)

'''
error 404 handler for mising items in backend
'''
@app.errorhandler(404)
def not_found(error):
    return (jsonify({"success": False, "error": 404, "message": "resource not found, booking/service/stylist not in the db"}), 404)


'''
error 422 handler for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({"success": False,"error": 422, "message": "unprocessable"}), 422


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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)