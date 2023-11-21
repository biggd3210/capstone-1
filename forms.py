"""file for creating forms for Mappo-Pollo"""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, DateField, IntegerField, TimeField, SelectField
from wtforms.validators import DataRequired, InputRequired, Email, Length, Optional

class UserAddForm(FlaskForm):
    """form for user signup"""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    name = StringField("Name", validators=[DataRequired()])
    phone = StringField("Phone Number", validators=[Optional()])

class LoginForm(FlaskForm):
    """form for user login"""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class SearchFlightsForm(FlaskForm):
    """form for searching API for flights."""

    origin = StringField("Origin", validators=[DataRequired()])
    destination = StringField("Destination", validators=[DataRequired()])
    adult_px = IntegerField("Adult Passengers", validators=[DataRequired()])
    departureDate = DateField("Departure Date", validators=[DataRequired()])
    returnDate = DateField("Return Date - (Leave empty for one-way flight.)", validators=[Optional()], render_kw={'placeholder': "Leave empty for one way flights"})
    # time = TimeField("Desired Time", validators=[Optional()])

class SearchHotelsForm(FlaskForm):
    """form for searching hotels given a location code."""

    cityCode = StringField("City", validators=[DataRequired()])
    radius = IntegerField("Search Radius", validators=[Optional()], default=5)
    radiusUnit = SelectField("Radius Unit", choices=[('MILE', 'Miles'), ('KM', 'Kilometers')], validators=[Optional()], default='MILE')
    checkInDate = DateField("Check-in Date", validators=[DataRequired()])
    checkOutDate = DateField("Check-out Date", validators=[DataRequired()])
    adults = IntegerField("Number of Guests", validators=[Optional()], default=2)

class ItineraryForm(FlaskForm):
    """form for creating new or editing itinerary."""

    name=StringField("Name", validators=[DataRequired()])