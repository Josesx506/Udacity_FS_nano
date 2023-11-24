#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
from datetime import datetime
import babel
from flask import render_template, request, flash, redirect, url_for, jsonify
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from models import *
import os



#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#
def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

# FLASK_WTF returns y/n instead of T/F and this dictionary helps to convert it.
talent_dict = {'y': True, None: False}

app.jinja_env.filters['datetime'] = format_datetime

# `Show` table filters (This is implemented here to avoid calling it every time)
# I also skipped repeatedly using the foreign keys of the Venue and Artist models for queries with this.
with app.app_context():
  # The upcoming_shows will be a query from the `Show` table with start_times that are after the current datetime
  # The past_shows will be a query from the `Show` table with start_times that are before the current datetime
  upcoming_shows_query = db.session.query(Show).filter(Show.start_time >= datetime.utcnow())
  past_shows_query = db.session.query(Show).filter(Show.start_time < datetime.utcnow())

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------
@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.

  # Get the distinct City and State names because city names can be replicated across states
  allCities = db.session.query(Venue.city, Venue.state).distinct().all()
  
  # Create an empty list to hold the venues data
  data = []

  for idx,city_state in enumerate(allCities):
    # Extract the city and state names from the tuple
    city_name,state_name = city_state
    # Perform a query to get the unique venues in each city and state
    cityVenues = db.session.query(Venue).filter(Venue.city==city_name, Venue.state==state_name).all()

    # Loop throught the unique venues and create a dictionary for each venue
    tmp = {
    "city": city_name,
    "state": state_name,
    "venues": [{"id": ven.id,
                "name": ven.name,
                "num_upcoming_shows": upcoming_shows_query.filter(Show.venue_id==ven.id).count(), # Filter the query by venue_id
                } for ven in cityVenues]}
    
    # Append the tmp dictionary to the empty data list above
    data.append(tmp)
  
  return render_template('pages/venues.html', areas=data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # search for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  searchKey = request.form.get('search_term')

  # Filter query that is case-insensitive with `.ilike`
  venueQuery = db.session.query(Venue).filter(Venue.name.ilike(f'%{searchKey}%'))
  # Extract the number of queries and query items
  count = venueQuery.count()
  allVenues = venueQuery.all()

  response={
    "count": count,
    "data": [{
      "id": _venue_.id,
      "name": _venue_.name,
      "num_upcoming_shows": upcoming_shows_query.filter(Show.venue_id==_venue_.id).count(),
    } for _venue_ in allVenues]
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  activeVenue = db.session.get(Venue, venue_id)
  upcomingShows = upcoming_shows_query.filter(Show.venue_id==venue_id)
  pastShows = past_shows_query.filter(Show.venue_id==venue_id)

  data = {
    "id": activeVenue.id,
    "name": activeVenue.name,
    "genres": activeVenue.genres,
    "address": activeVenue.address,
    "city": activeVenue.city,
    "state": activeVenue.state,
    "phone": activeVenue.phone,
    "website": activeVenue.website_link,
    "facebook_link": activeVenue.facebook_link,
    "seeking_talent": activeVenue.seeking_talent,
    "seeking_description": activeVenue.seeking_description,
    "image_link": activeVenue.image_link,
    "past_shows": [{
                    "artist_id": _show_.artist.id,
                    "artist_name": _show_.artist.name,
                    "artist_image_link": _show_.artist.image_link,
                    "start_time": str(_show_.start_time)
                  } for _show_ in pastShows.all()],
    "upcoming_shows": [{
                    "artist_id": _show_.artist.id,
                    "artist_name": _show_.artist.name,
                    "artist_image_link": _show_.artist.image_link,
                    "start_time": str(_show_.start_time)
                  } for _show_ in upcomingShows.all()],
    "past_shows_count": pastShows.count(),
    "upcoming_shows_count": upcomingShows.count(),
  }
  
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------
@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():

  try:
    # TODO: insert form data as a new Venue record in the db, instead
    newVenue = Venue(name = request.form['name'],
                    city = request.form['city'],
                    state = request.form['state'],
                    address = request.form['address'],
                    phone = request.form['phone'],
                    genres = request.form.getlist('genres'),
                    facebook_link = request.form['facebook_link'],
                    image_link = request.form['image_link'],
                    website_link = request.form['website_link'],
                    seeking_talent = talent_dict[request.form.get('seeking_talent')], # Get the form id instead
                    seeking_description = request.form['seeking_description'])
    
    # TODO: modify data to be the data object returned from db insertion
    data = newVenue

    # Add and commit db changes
    db.session.add(newVenue)
    db.session.commit()
    # on successful db insert, flash success
    flash('Venue ' + request.form['name'] + ' was successfully listed!')

  except():
    # TODO: on unsuccessful db insert, flash an error instead.,
    db.session.rollback()
    flash('An error occurred. Venue ' + data.name + ' could not be listed.')
    
  finally:
    db.session.close()
  
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>/delete', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  try:
      # Perform sqlalchemy query to get the row with the specified id
      venue = db.session.get(Venue, venue_id)
      # Delete the row of interest and commit the changes
      db.session.delete(venue)
      db.session.commit()

      # on successful db insert, flash success
      flash('This venue was successfully deleted')
  except:
      db.session.rollback()
  finally:
      db.session.close()

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage

  # The request and navigation were implemented in `pages/show_venue.html`
  # The <a> tag returns a GET request so I used the <button> outside of the hyperlink. Then I used
  # asynchronouse fetch to perform the DELETE request and navigate to the homepage
  return jsonify({'success': True})

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  data = Artist.query.order_by('id').all()
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # search for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  searchKey = request.form.get('search_term')

  # Filter query that is case-insensitive with `.ilike`
  artistQuery = db.session.query(Artist).filter(Artist.name.ilike(f'%{searchKey}%'))
  # Extract the number of queries and query items
  count = artistQuery.count()
  allArtists = artistQuery.all()

  response={
    "count": count,
    "data": [{
      "id": _artist_.id,
      "name": _artist_.name,
      "num_upcoming_shows": upcoming_shows_query.filter(Show.artist_id==_artist_.id).count(),
    } for _artist_ in allArtists]
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  activeArtist = db.session.get(Artist, artist_id)
  upcomingShows = upcoming_shows_query.filter(Show.artist_id==artist_id)
  pastShows = past_shows_query.filter(Show.artist_id==artist_id)

  data = {
    "id": activeArtist.id,
    "name": activeArtist.name,
    "genres": activeArtist.genres,
    "city": activeArtist.city,
    "state": activeArtist.state,
    "phone": activeArtist.phone,
    "website": activeArtist.website_link,
    "facebook_link": activeArtist.facebook_link,
    "seeking_venue": activeArtist.seeking_venue,
    "seeking_description": activeArtist.seeking_description,
    "image_link": activeArtist.image_link,
    "past_shows": [{
                    "venue_id": _show_.venue.id,
                    "venue_name": _show_.venue.name,
                    "venue_image_link": _show_.venue.image_link,
                    "start_time": str(_show_.start_time)
                  } for _show_ in pastShows.all()],
    "upcoming_shows": [{
                    "venue_id": _show_.venue.id,
                    "venue_name": _show_.venue.name,
                    "venue_image_link": _show_.venue.image_link,
                    "start_time": str(_show_.start_time)
                  } for _show_ in upcomingShows.all()],
    "past_shows_count": pastShows.count(),
    "upcoming_shows_count": upcomingShows.count()
  }
  
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  # Extract the active artist from the db
  activeArtist = db.session.get(Artist, artist_id)
  
  # Pass the artist attributes into a dictionary
  artist={
    "id": activeArtist.id,
    "name": activeArtist.name,
    "genres": activeArtist.genres,
    "city": activeArtist.city,
    "state": activeArtist.state,
    "phone": activeArtist.phone,
    "website": activeArtist.website_link,
    "facebook_link": activeArtist.facebook_link,
    "seeking_venue": activeArtist.seeking_venue,
    "seeking_description": activeArtist.seeking_description,
    "image_link": activeArtist.image_link
  }
  # TODO: populate form with fields from artist with ID <artist_id>
  form = ArtistForm(data=artist)

  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # Extract the active artist from the db
  activeArtist = db.session.get(Artist, artist_id)

  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  try:
    activeArtist.name = request.form['name']
    activeArtist.city = request.form['city']
    activeArtist.state = request.form['state']
    activeArtist.phone = request.form['phone']
    activeArtist.genres = request.form.getlist('genres')
    activeArtist.facebook_link = request.form['facebook_link']
    activeArtist.image_link = request.form['image_link']
    activeArtist.website_link = request.form['website_link']
    activeArtist.seeking_venue = talent_dict[request.form.get('seeking_venue')] # Get the form id instead
    activeArtist.seeking_description = request.form['seeking_description']

    db.session.commit()
    # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully updated!')

  except():
    # TODO: on unsuccessful db insert, flash an error instead.,
    db.session.rollback()
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be updated.')
    
  finally:
    db.session.close()

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  # Extract the active artist from the db
  activeVenue = db.session.get(Venue, venue_id)

  # Pass the venue attributes into a dictionary
  venue={
    "id": activeVenue.id,
    "name": activeVenue.name,
    "genres": activeVenue.genres,
    "address": activeVenue.address,
    "city": activeVenue.city,
    "state": activeVenue.state,
    "phone": activeVenue.phone,
    "website": activeVenue.website_link,
    "facebook_link": activeVenue.facebook_link,
    "seeking_talent": activeVenue.seeking_talent,
    "seeking_description": activeVenue.seeking_description,
    "image_link": activeVenue.image_link
  }
  # TODO: populate form with values from venue with ID <venue_id>
  form = VenueForm(data=venue)
  
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # Extract the active artist from the db
  activeVenue = db.session.get(Venue, venue_id)

  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  try:
    activeVenue.name = request.form['name']
    activeVenue.city = request.form['city']
    activeVenue.state = request.form['state']
    activeVenue.address = request.form['address']
    activeVenue.phone = request.form['phone']
    activeVenue.genres = request.form.getlist('genres')
    activeVenue.facebook_link = request.form['facebook_link']
    activeVenue.image_link = request.form['image_link']
    activeVenue.website_link = request.form['website_link']
    activeVenue.seeking_talent = talent_dict[request.form.get('seeking_talent')] # Get the form id instead
    activeVenue.seeking_description = request.form['seeking_description']

    db.session.commit()
    # on successful db insert, flash success
    flash('Venue ' + request.form['name'] + ' was successfully updated!')

  except():
    # TODO: on unsuccessful db insert, flash an error instead.,
    db.session.rollback()
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be updated.')
    
  finally:
    db.session.close()

  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------
@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  try:
    # TODO: insert form data as a new Artist record in the db, instead
    newArtist = Artist(name = request.form['name'],
                       city = request.form['city'],
                       state = request.form['state'],
                       phone = request.form['phone'],
                       genres = request.form.getlist('genres'),
                       facebook_link = request.form['facebook_link'],
                       image_link = request.form['image_link'],
                       website_link = request.form['website_link'],
                       seeking_venue = talent_dict[request.form.get('seeking_venue')], # Get the form id instead
                       seeking_description = request.form['seeking_description'])
    
    # TODO: modify data to be the data object returned from db insertion
    data = newArtist

    # Add and commit db changes
    db.session.add(newArtist)
    db.session.commit()
    # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully listed!')

  except():
    # TODO: on unsuccessful db insert, flash an error instead.,
    db.session.rollback()
    flash('An error occurred. Artist ' + data.name + ' could not be listed.')
    
  finally:
    db.session.close()
  
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------
@app.route('/shows')
def shows():
  # displays list of shows at /shows
  allShows = db.session.query(Show).all()

  # TODO: replace with real venues data.
  data = [{
    "venue_id":          _show_.venue.id,
    "venue_name":        _show_.venue.name,
    "artist_id":         _show_.artist.id,
    "artist_name":       _show_.artist.name,
    "artist_image_link": _show_.artist.image_link,
    "start_time":        str(_show_.start_time),
  } for _show_ in allShows]

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  try:
    # TODO: insert form data as a new Show record in the db, instead
    newShow = Show(artist_id = request.form['artist_id'],
                   venue_id = request.form['venue_id'],
                   start_time = request.form['start_time'])

    # Add and commit db changes
    db.session.add(newShow)
    db.session.commit()
    # on successful db insert, flash success
    flash('Show was successfully listed!')

  except():
    # TODO: on unsuccessful db insert, flash an error instead.,
    db.session.rollback()
    flash('An error occurred. Show could not be listed.')
    
  finally:
    db.session.close()
  
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
# if __name__ == '__main__':
#     app.run()

# Or specify port manually:
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port)
