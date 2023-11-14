"""Main app control file for Mappo-Pollo"""

import os

from flask import Flask, render_template, request, flash, redirect, session, g, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from datetime import datetime
from forms import UserAddForm, LoginForm, SearchFlightsForm, ItineraryForm, SearchHotelsForm
from comms import request_amadeus_auth, search_available_flights, search_accommodations, search_hotel_offers
from models import db, connect_db, User, Itinerary, Flight, UserItinerary, ItineraryComponent
from helpers import format_date, format_time
from dotenv import load_dotenv
import json

# login_manager = LoginManager()
load_dotenv()

CURR_USER_KEY = "curr_user"

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///mappo_pollo')
)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "KEY_CURRENTLY_UNSET")
toolbar = DebugToolbarExtension(app)

connect_db(app)

img_path = os.getenv("BASE_URL") + os.getenv("LOGO_IMG")

# -------- Login requirements before refactoring. --------
@app.before_request
def add_user_to_g():
    """If logged in, add current user to global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None

def do_login(user):
    """Perform user login."""

    session[CURR_USER_KEY] = user.id

def do_logout():
    """Perform user logout."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

# -------- User signup, login, and logout routes ------------

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Show form on GET request.
    Process form and login user for POST requests."""

    form = LoginForm()
    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)
        if user:
            do_login(user)
            flash(f"Welcome back, {user.username}", 'success')
            return redirect('/')
    return render_template('users/login.html', form=form)

        

@app.route('/signup', methods=['GET', 'POST'])
def user_signup():
    """Signup Form Handle and commit user to db. redirect to secure homepage."""

    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                name=form.name.data,
                phone=form.phone.data
            )
            db.session.commit()
        except IntegrityError:
            flash("Username and/or email already taken. Please try another.", "danger")
            return render_template("users/signup.html", form=form)
        
        do_login(user)

        flash("Successfully created new user", 'success')
        return redirect('/')
    return render_template('users/signup.html', form=form)

@app.route('/logout')
def logout_user():
    """Handle user logout and redirect to main."""

    do_logout()
    flash("Thanks for visiting! See you soon!", 'success')
    return redirect('/login')

#---------- Users and Profiles ----------------

@app.route('/users/profile', methods=['GET', 'POST'])
def edit_user():
    """Allow user to edit profile."""

    if not g.user:
        flash("Unauthorized. Cannot edit user profile. Please login!", 'danger')
        return redirect('/')
        
    form = UserAddForm(obj=g.user)

    if form.validate_on_submit():
        user = User.authenticate(g.user.username, form.password.data)

        if (session[CURR_USER_KEY] == user.id):
            user.username = form.username.data
            user.email = form.email.data
            user.phone = form.phone.data
            user.name = form.name.data

            db.session.commit()
            flash("Successfully updated user information", 'info')
            return redirect(f'/')

        flash("Please validate your password", 'info')
    return render_template('users/user_profile.html', form=form, user_id=g.user.id)

#---------- Trips and Components Routes ----------

@app.route('/itineraries')
def show_user_itineraries():
    """Shows current users created itineraries"""

    if not g.user:
        flash("Unauthorized action. You may not view user itineraries without being signed in.", 'danger')
        return redirect('/login')
    
    return render_template('components/itineraries.html')

@app.route("/itineraries/add", methods=['GET', 'POST'])
def add_new_itinerary():
    """Grabs form info and creates new itinerary."""

    if not g.user:
        flash("Unauthorized. Must be logged in to create itineraries.", 'danger')
        return redirect('/login')

    form = ItineraryForm()

    if form.validate_on_submit():
        try:
            itinerary = Itinerary(name=form.name.data, created_by=g.user.id)
            db.session.add(itinerary)
            db.session.commit()
            
        except:
            raise
            flash("There was an issue.", 'info')
            return render_template('components/add_itinerary.html', form=form)
        
        itin_relation = UserItinerary(user_id=g.user.id, itinerary_id=itinerary.id)
        db.session.add(itin_relation)
        db.session.commit()

        flash("Successfully created new itinerary", "success")
        return redirect('/itineraries')
    
    return render_template('components/add_itinerary.html', form=form)

@app.route("/itineraries/<int:itinerary_id>/view")
def show_unique_itinerary(itinerary_id):
    """Display's info for particular itinerary as well as ability to edit information/delete components."""

    itin = Itinerary.query.get_or_404(itinerary_id)

    return render_template("components/itinerary.html", itin=itin)

@app.route('/itineraries/add-component', methods=['GET', 'POST'])
def add_component_to_itin():
    """Adds component from search feature to designated """

    if not g.user:
        flash("Unauthorized. Please login to view itinerary.", 'danger')
        return redirect('/login')
    
    if request.method == "POST":

        flight = eval(request.form.get('component-info'))
        itin_id = request.form.get('itin_id')
        try:
            new_flight = Flight(
                origin=flight['origin'],
                destination=flight['destination'],
                departure_date=flight['departure date'],
                arrival_date=flight['arrival date'],
                carrier=flight['carrier'],
                price=flight['price'],
                currency=flight['currency'],
                segments=flight['segments'],
                duration=flight['duration'],
                seats_remaining=flight['seats remaining'],
                travelers=flight['travelers']
            )
            db.session.add(new_flight)
        except:
            flash("sorry, there was an error", "danger")
            return redirect('/flights/search')
        
        if itin_id == "new":
            itin = Itinerary(
                name="New Itinerary",
                created_by=g.user.id,
            )
            db.session.add(itin)
            db.session.commit()
            itin_link = UserItinerary(user_id=g.user.id, itinerary_id=itin.id)
            db.session.add(itin_link)
            db.session.commit()
        else:
            itin = Itinerary.query.get_or_404(itin_id)
        
        flight_link = ItineraryComponent(itinerary_id=itin.id, flight_id=new_flight.id)
        db.session.add(flight_link)
        db.session.commit()
        
        flash("Successfully updated itinerary!", "success")
        return redirect(f'/itineraries/{itin.id}/view')
    return "No flight data"

@app.route('/itineraries/delete-component', methods=['GET', 'POST', 'DELETE'])
def remove_component():
    """removes specified component from itinerary."""
    
    flight = Flight.query.get_or_404(request.form.get('flight_id'))
    itin = Itinerary.query.get_or_404(request.form.get('itin_id'))
    print('flight is ', flight)
    print('itin is ', itin)
    
    db.session.delete(flight)
    db.session.commit()

    return redirect(f'/itineraries/{itin.id}/view')

@app.route('/itineraries/<int:itin_id>/edit', methods=['GET', 'POST'])
def edit_itinerary(itin_id):
    """allows user to edit name and certain info of itinerary."""

    itin = Itinerary.query.get_or_404(itin_id)

    form = ItineraryForm(itin)



    
@app.route('/itineraries/<int:itin_id>/delete', methods=['GET', 'POST'])
def delete_itinerary(itin_id):
    """deletes full itinerary."""

    itin = Itinerary.query.get_or_404(itin_id)

    db.session.delete(itin)
    db.session.commit()

    return redirect('/itineraries')

#----------- Search Routes -------------

@app.route('/flights/search', methods=['GET', 'POST'])
def search_flights():
    """Show form for searching flights, return results from API"""

    if not g.user:
        flash("Unauthorized. Must be logged in to search flights.", 'danger')
        return redirect('/login')
    
    form = SearchFlightsForm()

    if form.validate_on_submit():
        
        params = {
            "origin" : form.origin.data,
            'destination' : form.destination.data,
            'px_num' : str(form.adult_px.data),
            'departureDate' : format_date(form.departureDate.data),
            'returnDate' : ''
        }

        if form.returnDate.data != None:
            params['returnDate'] = format_date(form.returnDate.data)
        # if form.time.data != None:
        #     params['time'] = format_time(form.time.data)

        resp = search_available_flights(params)
        itineraries = g.user.itineraries
        
        return render_template("/components/results.html", resp=resp, itineraries=itineraries, type="Flight")
        
        
    return render_template("components/search.html", form=form, type="Flight")


# --------- Accommodations and Hotels -------

@app.route('/hotels/search', methods=['GET', 'POST'])
def search_hotels():
    """Searches API for hotels which a user can select to view available room offers."""
    
    if not g.user:
        flash("Sorry. You must be logged in to search hotels.", "danger")
        return redirect('/login')
    
    form = SearchHotelsForm()

    if form.validate_on_submit():
        params = {
            "cityCode" : form.cityCode.data.upper(),
            "radius" : form.radius.data,
            "radiusUnit" : form.radiusUnit.data,
            "checkInDate" : format_date(form.checkInDate.data),
            "checkOutDate" : format_date(form.checkOutDate.data),
            "adults" : form.adults.data
        }

        resp = search_accommodations(params)

        return render_template('/components/results.html', resp=resp, type="Hotel")
    
    return render_template('/components/search.html', form=form, type='Hotel')

@app.route('/hotels/rooms/search', methods=['GET', 'POST'])
def search_rooms():
    """uses axios from client side to make request to Amadeus API to gather room offer data."""
    
    params = {
        'hotelIds' : request.form['hotelId'],
        'adults' : '2'
    }

    resp = search_hotel_offers(params)
    print('resp is ', resp)

    return resp


# -------- Main Page ----------

@app.route('/')
def show_main():
        
    return render_template('home.html')