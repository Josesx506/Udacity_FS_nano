from datetime import datetime
import os
import sys
# Setup the python file path to enable importing the system variables
sys.path.append(os.getcwd())
from models import db, Booking, Service, Stylist
from app import app


def single_entry_db(app):
   """Insert template entries into the db"""
   event_1 =  Booking(first_name="Julius",
                      last_name='Agu',
                      phone='+4494041098',
                      email='jugu@gmail.com',
                      start_time=f"{datetime(2023, 12, 1, 12, 0)}",
                      completed=True,
                      stylist_id=1,
                      user_id='demo')
   event_2 =  Booking(first_name="Elizabeth",
                      last_name='Tyler',
                      phone='+4494041098',
                      email='eller@yahoo.com',
                      start_time=f"{datetime(2023, 12, 6, 14, 0)}",
                      completed=True,
                      stylist_id=1,
                      user_id='demo')
   event_3 =  Booking(first_name="Reina",
                      last_name='Akurus',
                      phone='+4494041098',
                      email='rerus@zinmo.com',
                      start_time=f"{datetime(2024, 1, 4, 10, minute=0)}",
                      completed=False,
                      stylist_id=1,
                      user_id='demo')
   stylist1 = Stylist(name="King Ella",
                      phone="+2275499450",
                      email="stylist1@luxehair.com",
                      salon_role='Stylist',
                      bio="Lorem ipsum dolor sit amet consectetur adipisicing elit. Excepturi nostrum voluptas repudiandae consequatur animi eos natus laudantium deserunt enim. Accusantium perferendis eaque neque reprehenderit magni dolore molestiae. Officiis, impedit. Labore.",
                      image_link='https://pbs.twimg.com/media/DnZXDYyXcAYsPyj.jpg',
                      user_id='demo')
   service1 = Service(name="Hair Reconstruction",
                      price=50,
                      duration=1,
                      image_link="https://carolinahairsurgery.com/wp-content/uploads/PaulaBA.jpg")

   ### There has to be a stylist before t
   entries = [stylist1,service1]
   db.session.add_all(entries)
   db.session.commit()
   events = [event_1,event_2,event_3]
   db.session.add_all(events)
   db.session.commit()

   return "All entries successfully committed"


# Insert the manual entries first before launching the app
single_entry_db(app)