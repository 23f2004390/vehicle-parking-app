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
class VehicleType(enum.Enum):
    wheeler = '2-wheeler'
    four_wheeler = '4-wheeler'
    heavy_vehicle = 'heavy-vehicle'
class BookingStatus(enum.Enum):
    ACTIVE = 'active'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    bookings = db.relationship('booking', backref='user', lazy=True)
    reviews = db.relationship('Review', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', Admin: {self.is_admin})"


class parking_lot(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    prime_location_name = db.Column(db.String(150), nullable=False)
    address = db.Column(db.Text, nullable=False)  
    pin_code = db.Column(db.Integer, nullable=False)
    total_spots = db.Column(db.Integer, nullable=False)
    available_spots = db.Column(db.Integer, nullable=False)

    spots = db.relationship('parking_spot', backref='parking_lot', lazy=True, cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='parking_lot', lazy=True)

    def __repr__(self):
        return f"ParkingLot('{self.prime_location_name}', '{self.address}', Total: {self.total_spots}, Available: {self.available_spots})"
    

class parking_spot(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    is_occupied = db.Column(db.Boolean, default=False)
    parking_cost = db.Column(db.Float, nullable=False default=-1.0)
    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lot.id'), nullable=False)
    spot_type = db.Column(db.Enum(SpotType), default=SpotType.REGULAR)

    # Relationship to bookings
    bookings = db.relationship('booking', backref='parking_spot', lazy=True)

    
    def __repr__(self):
        return f"ParkingSpot(Lot: {self.lot_id}, Spot: {self.spot_number}, Type: {self.spot_type.value}, Occupied: {self.is_occupied})"


class booking(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    spot_id = db.Column(db.Integer, db.ForeignKey('parking_spot.id'), nullable=False)
    vehicle_number = db.Column(db.String(15), nullable=False)
    vehicle_type = db.Column(db.Enum(VehicleType), nullable=False)  
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.Enum(BookingStatus), default=BookingStatus.ACTIVE)  
    total_cost = db.Column(db.Float, nullable=False)
    user = db.relationship('User', backref='bookings')
    parking_spot = db.relationship('parking_spot', backref='bookings')


    def __repr__(self):
        return f"Booking(User ID: {self.user_id}, Spot ID: {self.spot_id}, Start: {self.start_time}, End: {self.end_time})"


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lot.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    

    __table_args__ = (db.CheckConstraint('rating >= 1 AND rating <= 5'), )

    def __repr__(self):
        return f"Review(User ID: {self.user_id}, Lot ID: {self.lot_id}, Rating: {self.rating})"

# =======================================================
#============== Routes ==================================
# =======================================================   
@app.route('/')
def index():
    return "Welcome to the Parking Management System!"

if __name__ == '__main__':
    app.run(debug=True)
