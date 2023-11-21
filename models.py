"""SQLAlchmey models for Mappo-Pollo"""

from datetime import datetime

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt= Bcrypt()
db = SQLAlchemy()


class ItineraryComponent(db.Model):
    """links individual componenents to Itineraries."""

    __tablename__ = "itinerary_components"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    itinerary_id = db.Column(
        db.Integer,
        db.ForeignKey(
            'itineraries.id', 
            ondelete="cascade"
        ),
        nullable=False
    )

    flight_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "flights.id",
            ondelete="cascade"
        ),
        nullable=True
    )

    accommodation_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "accommodations.id",
            ondelete="cascade"
        ),
        nullable=True
    )

    transfer_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "transfers.id",
            ondelete="cascade"
        ),
        nullable=True
    )

    excursions_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "excursions.id",
            ondelete="cascade"
        ),
        nullable=True
    )

    activity_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "activities.id",
            ondelete="cascade"
        ),
        nullable=True
    )

class UserItinerary(db.Model):
    """relational table connecting users to their itineraries."""

    __tablename__ = "users_itineraries"
    
    user_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "users.id",
            ondelete="cascade"
        ),
        primary_key=True
    )

    itinerary_id = db.Column(
        db.Integer,
        db.ForeignKey(
            "itineraries.id",
            ondelete="cascade"
        ),
        primary_key=True
    )



class Itinerary(db.Model):
    """itineraries arranged by user, linked to travel parties and linked to commponents through relational table"""

    __tablename__ = "itineraries"

    id = db.Column(
        db.Integer,
        primary_key=True
    )
    
    name = db.Column(
        db.Text,
        nullable=False,
        default="New Itinerary"
    )

    created_by = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='cascade')
    )

    flights = db.relationship(
        "Flight",
        secondary="itinerary_components",
        backref="itineraries",
        lazy='subquery'
    )

    accommodations = db.relationship(
        "Accommodation",
        secondary='itinerary_components',
        backref='itineraries',
        lazy='subquery'
    )

    user = db.relationship(
        "User",
        lazy="subquery"
    )

    def __repr__(self):
        """repr should return readable info"""

        return f"Itinerary id: {self.id}, name: {self.name}, created_by: {self.created_by}"

class Flight(db.Model):
    """table for all saved flights obtained from API"""

    __tablename__ = "flights"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    origin = db.Column(
        db.Text,
        nullable=False
    )

    destination = db.Column(
        db.Text,
        nullable=False
    )

    departure_date = db.Column(
        db.String,
        nullable=False
    )

    arrival_date = db.Column(
        db.String,
        nullable=False
    )

    carrier = db.Column(
        db.String,
        nullable=False
    )

    price = db.Column(
        db.Float,
        nullable=True
    )

    currency = db.Column(
        db.String,
        nullable=True
    )

    segments = db.Column(
        db.Integer,
        nullable=False,
    )

    duration = db.Column(
        db.String,
        nullable=False
    )

    seats_remaining = db.Column(
        db.Integer,
        nullable=False
    )

    travelers = db.Column(
        db.Integer,
        nullable=False
    )

class Accommodation(db.Model):
    """Accomodations table for hotel stays/airbnb, etc. Component of Itinerary."""

    __tablename__ = "accommodations"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    hotel_name = db.Column(
        db.Text,
        nullable=False
    )

    hotel_amadeus_id = db.Column(
        db.String,
        nullable=False
    )

    check_in = db.Column(
        db.Text,
        nullable=False
    )

    check_out = db.Column(
        db.Text,
        nullable=False
    )

    latitude = db.Column(
        db.Text,
        nullable=False
    )

    longitude = db.Column(
        db.Text,
        nullable=False
    )

    number_of_guests = db.Column(
        db.Integer,
        nullable=False
    )

    price = db.Column(
        db.Float,
        nullable=False
    )

    currency = db.Column(
        db.String,
        nullable=False
    )

    

class Transfer(db.Model):
    """Table for transfers, perhaps not frequently used but for things more like taxis, ubers or otherwise connecting from airport to accommodation or otherwise."""

    __tablename__ = "transfers"

    id = db.Column(
        db.Integer,
        primary_key=True
    )
    
    company = db.Column(
        db.Text,
        nullable=False
    )

    date = db.Column(
        db.Text,
        nullable=False
    )

    origin = db.Column(
        db.Text,
        nullable=False
    )

    destination = db.Column(
        db.Text,
        nullable=False
    )

    price = db.Column(
        db.Float,
        nullable=True
    )

class Excursion(db.Model):
    """excursions table. for outings and events that a client will do while in a location. (Think swimming with pigs, something bookable. Not just going to a monument or something.)"""

    __tablename__ = "excursions"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    operator = db.Column(
        db.Text,
        nullable=True
    )
    
    tour = db.Column(
        db.Text,
        nullable=True
    )
    
    type = db.Column(
        db.Text,
        nullable=True
    ) 
    
    date = db.Column(
        db.Text,
        nullable=True
    )    
        
    time = db.Column(
        db.Text,
        nullable=True
    )

class Activity(db.Model):
    """Independent activities that a client may want to log but that was not a bookable event. (Went to a museum on a base ticket or saw a monument or something like Time Square)"""

    __tablename__ = "activities"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.Text,
        nullable=True
    )

    type = db.Column(
        db.Text,
        nullable=True,
    )

    location = db.Column(
        db.Text,
        nullable=False
    )

    date = db.Column(
        db.Text,
        nullable=True
    )

    time = db.Column(
        db.Text,
        nullable=True
    )

class User(db.Model):
    """Model of users"""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String,
        nullable=False
    )

    username = db.Column(
        db.String,
        nullable=False,
        unique=True
    )

    password = db.Column(
        db.Text,
        nullable=False
    )

    email = db.Column(
        db.Text,
        nullable=False,
        unique=True
    )

    phone = db.Column(
        db.Text,
        nullable=True,
    )
    
    itineraries = db.Relationship(
        "Itinerary",
        secondary="users_itineraries",
        backref="users",
        lazy="subquery"
    )


    # ---------- Instance Methods ------

    def __repr__(self):
        """Defines representation of instance of User"""

        return f"username: {self.username}, name: {self.name}, email: {self.email}"

    # ---------- Class method -----------

    @classmethod
    def authenticate(cls, username, password):
        """find user with matching username and check_hash_password.
        Returns instance of user if true,
        returns False if it does not find a matching user or if the password is inccorrect. 
        """

        user = cls.query.filter(username==username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False
    
    @classmethod
    def signup(cls, username, email, password, name, phone):
        """sign up user and hashes password to store, stores new user in db."""
        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
            name=name,
            phone=phone
        )

        db.session.add(user)

        return user
    

def connect_db(app):
    """Connect db to the Flask app"""

    db.app = app
    db.init_app(app)