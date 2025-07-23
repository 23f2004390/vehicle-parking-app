from flask import Flask, request, template, redirect, url_for, session,flash
from flask_sqlalchemy import SQLAlchemy

import os 
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secretkey000'
db = SQLAlchemy(app)



# =======================================================
#============== Models =================================
# =======================================================
import enum

class SpotType(enum.Enum):
    REGULAR = 'regular'
    ELECTRIC = 'electric'
    



class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    bookings = db.relationship('Booking', backref='user', lazy=True)


    def __repr__(self):
        return f"User('{self.username}', '{self.email}' {self.is_admin})"
class parking_lot(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    prime_location_name = db.Column(db.String(150), nullable=False)
    address = db.Column(db.String(150), nullable=False)
    pin_code = db.Column(db.Integer, nullable=False)
    total_spots = db.Column(db.Integer, nullable=False)
    available_spots = db.Column(db.Integer, nullable=False)

    spots = db.relationship('Parking_Spot', backref='parking_lot', lazy=True, cascade='all, delete-orphan')


    def __repr__(self):
        return f"ParkingLot('{self.prime_location_name}', '{self.address}', Total: {self.total_spots}, Available: {self.available_spots})"
    
class parking_spot(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    is_occupied = db.Column(db.Boolean, default=False)
    parking_cost = db.Column(db.Float, nullable=False)
    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lot.id'), nullable=False)
    # spot_type = db.Column(db.String(20), default='regular')  # regular, handicap, electric, etc.
    spot_type = db.Column(db.Enum(SpotType), default=SpotType.REGULAR)

    bookings = db.relationship('Booking', backref='parking_spot', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f"ParkingSpot('{self.lot_id}', Occupied: {self.is_occupied})"

class booking(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    spot_id = db.Column(db.Integer, db.ForeignKey('parking_spot.id'), nullable=False)
    vehicle_number = db.Column(db.String(50), nullable=False)
    vehicle_type = db.Column(db.String(50), nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='active')  # active orcompleted
    total_cost = db.Column(db.Float, nullable=False)
    bookings = db.relationship('Booking', backref='parking_spot', lazy=True, cascade='all, delete-orphan')
    user = db.relationship('User', backref='bookings')

    def __repr__(self):
        return f"Booking(User ID: {self.user_id}, Spot ID: {self.spot_id}, Start: {self.start_time}, End: {self.end_time})"
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lot.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False) 
    comment = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', backref='reviews')
    parking_lot = db.relationship('parking_lot', backref='reviews')
