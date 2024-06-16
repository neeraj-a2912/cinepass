from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(40), unique=True)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(10), default="user")
    last_logged = db.Column(db.DateTime)
    bookings = db.relationship('Booking', backref='user')

class Theatre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    place = db.Column(db.String(50), nullable=False)
    screens = db.Column(db.Integer, nullable=False)
    shows = db.relationship('Show', backref='theatre')

class Show(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    ratings = db.Column(db.Integer, nullable=False)
    tags = db.Column(db.String(200), nullable=False) 
    ticket_price = db.Column(db.Integer, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    show_date = db.Column(db.String, nullable=False)
    show_timing = db.Column(db.String, nullable=False)
    screen_number = db.Column(db.Integer, nullable=False)
    theatre_id = db.Column(db.Integer, db.ForeignKey('theatre.id'))
    bookings = db.relationship('Booking', backref='show')

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    show_id = db.Column(db.Integer, db.ForeignKey('show.id'))
    number_of_tickets = db.Column(db.Integer, default=1)
    total_price = db.Column(db.Integer)
    current_price = db.Column(db.Integer)
    booking_time = db.Column(db.DateTime, default= datetime.utcnow, nullable=False)





