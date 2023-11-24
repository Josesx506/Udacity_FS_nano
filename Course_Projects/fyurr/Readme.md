### Fyurr Implementation Checklist
Here are the lists of Todo Items I've completed. They were not completed sequentially but it helped me keep track. <br>
Note: **POST** requests are handled with request.form['<form_label_name>'] unlike dom from javascript.
- [x] Link app with local psql db in `config` file.
- [x] Initialize and monitor db changes with Flask-Migrate.
    - I encountered some issues with the flask version and from werkzeug. 
    - To fix it, I upgraded SQLAlchemy=3.1.1 and some other packages (documented in *requirements.txt*). 
    - Then I used `python3 -m flask db migrate` to track db changes.
- [x] Setup missing columns for `Artists` and `Venues` models including Foreign keys
- [x] Setup `Shows` model that links to the Artists and Venues that were booked for the show.
- [x] Link `create_venue_submission()` to psql db
    - [x] Update `venues` page with data from the psql db
    - [x] Update `show_venues()` function with data from psql db
    - [x] Populate `edit_venue` form with psql db
    - [x] Update psql db when the button is submitted with `edit_venue_submission()`
    - [x] Implement case-insentitive search of venue table from psql with `search_venues`
    - [x] Implement delete button for show_venues page with `delete_venue()` as a Bonus. This was done using AJAX fetch and flask. 
    <br>
- [x] Link `create_artist_submission()` to psql db
    - [x] Update `artists` page with data from psql db
    - [x] Update `show_artist()` function with data from psql db
    - [x] Populate `edit_artist` form with psql db
    - [x] Update psql db when the button is submitted with `edit_artist_submission()`
    - [x] Implement case-insentitive search of artist table from psql with `search_artists`
    <br>
- [x] Link `create_show_submission` to psql db
    - [x] Update `shows` page with data from psql db
    <br>
- [x] All models have been moved to the `models.py` file.
- [ ] I didn't go above and beyond because I'm 3 days behind the submission schedule. Would probably tackle it after the nanodegree is completed.
