from datetime import datetime
import os,sys
# Setup the python file path to enable importing the system variables
sys.path.append("..")
from models import db, Booking, Service, Stylist


def single_entry_db():
   """Insert template entries into the db"""
   event_1 =  Booking(first_name="Julius",
                      last_name='Agu',
                      phone='+4494041098',
                      email='jugu@gmail.com',
                      start_time=datetime(2023, 12, 1, 12, 0),
                      completed=True,
                      stylist_id=1,
                      user_id='demo')
   event_2 =  Booking(first_name="Elizabeth",
                      last_name='Tyler',
                      phone='+4494041098',
                      email='eller@yahoo.com',
                      start_time=datetime(2023, 12, 6, 14, 0),
                      completed=True,
                      stylist_id=1,
                      user_id='demo')
   event_3 =  Booking(first_name="Reina",
                      last_name='Akurus',
                      phone='+4494041098',
                      email='rerus@zinmo.com',
                      start_time=datetime(2024, 1, 4, 10, minute=0),
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
   stylist2 = Stylist(name="Akurus Mafor",
                      phone="+432443456655",
                      email="stylist2@luxehair.com",
                      salon_role='Stylist / Manager',
                      bio="Lorem ipsum dolor sit amet consectetur adipisicing elit. Similique aliquid debitis tempora quas excepturi, ipsum vero quasi tenetur facere alias?",
                      image_link='https://images.squarespace-cdn.com/content/v1/5f53b4244830fe79cec6a66c/3acd5d3d-f1ad-4dcb-89d3-760ae04ad508/professional-binghamton-headshots-photographer.jpg',
                      user_id='demo')
   stylist3 = Stylist(name="Perpernado Jedia",
                      phone="+2334584495",
                      email="stylist3@luxehair.com",
                      salon_role='Stylist / Barber',
                      bio="Lorem ipsum dolor sit amet consectetur adipisicing elit. Similique aliquid debitis tempora quas excepturi, ipsum vero quasi tenetur facere",
                      image_link='https://i.pinimg.com/736x/9b/66/b3/9b66b3f70435a8eadc471e8071c094e3.jpg',
                      user_id='demo')
   service1 = Service(name="Hair Reconstruction",
                      price=50,
                      duration=1,
                      image_link="https://carolinahairsurgery.com/wp-content/uploads/PaulaBA.jpg")

   ### There has to be a stylist before t
   entries = [stylist1,stylist2,stylist3,service1]
   db.session.add_all(entries)
   db.session.commit()
   events = [event_1,event_2,event_3]
   db.session.add_all(events)
   db.session.commit()