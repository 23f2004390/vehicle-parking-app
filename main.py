from flask import Flask, request, redirect, url_for, session,flash
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse, fields, marshal_with, marshal

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
    parking_cost = db.Column(db.Float, nullable=False, default=-1.0)
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
#============== API ==================================
# =======================================================   
api = Api(app)
class UserResource(Resource):
    def get(self):
        user = User.query.all()
        # if not user:
        #     return {'message': 'User not found'}, 404
        return {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'is_admin': user.is_admin
        }

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True, help='Username cannot be blank')
        parser.add_argument('password', required=True, help='Password cannot be blank')
        parser.add_argument('email', required=True, help='Email cannot be blank')
        args = parser.parse_args()

        new_user = User(username=args['username'], password=args['password'], email=args['email'])
        db.session.add(new_user)
        db.session.commit()
        return {'message': 'User created successfully'}, 201
class ParkingLotResource(Resource):
    def get(self, lot_id):
        lot = parking_lot.query.get_or_404(lot_id)
        return {
            'id': lot.id,
            'prime_location_name': lot.prime_location_name,
            'address': lot.address,
            'pin_code': lot.pin_code,
            'total_spots': lot.total_spots,
            'available_spots': lot.available_spots
        }

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('prime_location_name', required=True, help='Location name cannot be blank')
        parser.add_argument('address', required=True, help='Address cannot be blank')
        parser.add_argument('pin_code', type=int, required=True, help='Pin code cannot be blank')
        parser.add_argument('total_spots', type=int, required=True, help='Total spots cannot be blank')
        args = parser.parse_args()

        new_lot = parking_lot(
            prime_location_name=args['prime_location_name'],
            address=args['address'],
            pin_code=args['pin_code'],
            total_spots=args['total_spots'],
            available_spots=args['total_spots']  # Initially all spots are available
        )
        db.session.add(new_lot)
        db.session.commit()
        return {'message': 'Parking lot created successfully'}, 201
class ParkingSpotResource(Resource):
    def get(self, spot_id):
        spot = parking_spot.query.get_or_404(spot_id)
        return {
            'id': spot.id,
            'is_occupied': spot.is_occupied,
            'parking_cost': spot.parking_cost,
            'lot_id': spot.lot_id,
            'spot_type': spot.spot_type.value
        }

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('lot_id', type=int, required=True, help='Parking lot ID cannot be blank')
        parser.add_argument('parking_cost', type=float, required=True, help='Parking cost cannot be blank')
        parser.add_argument('spot_type', type=str, choices=[e.value for e in SpotType], default=SpotType.REGULAR.value)
        args = parser.parse_args()

        new_spot = parking_spot(
            lot_id=args['lot_id'],
            parking_cost=args['parking_cost'],
            spot_type=SpotType(args['spot_type'])
        )
        db.session.add(new_spot)
        db.session.commit()
        return {'message': 'Parking spot created successfully'}, 201
class BookingResource(Resource):
    def get(self, booking_id):
        booking = booking.query.get_or_404(booking_id)
        return {
            'id': booking.id,
            'user_id': booking.user_id,
            'spot_id': booking.spot_id,
            'vehicle_number': booking.vehicle_number,
            'vehicle_type': booking.vehicle_type.value,
            'start_time': booking.start_time.isoformat(),
            'end_time': booking.end_time.isoformat(),
            'status': booking.status.value,
            'total_cost': booking.total_cost
        }

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int, required=True, help='User ID cannot be blank')
        parser.add_argument('spot_id', type=int, required=True, help='Parking spot ID cannot be blank')
        parser.add_argument('vehicle_number', required=True, help='Vehicle number cannot be blank')
        parser.add_argument('vehicle_type', type=str, choices=[e.value for e in VehicleType], required=True)
        parser.add_argument('end_time', type=str, required=True, help='End time cannot be blank')
        args = parser.parse_args()

        new_booking = booking(
            user_id=args['user_id'],
            spot_id=args['spot_id'],
            vehicle_number=args['vehicle_number'],
            vehicle_type=VehicleType(args['vehicle_type']),
            end_time=datetime.fromisoformat(args['end_time']),
            total_cost=0.0  # Placeholder for cost calculation
        )
        db.session.add(new_booking)
        db.session.commit()
        return {'message': 'Booking created successfully'}, 201 
api.add_resource(UserResource, '/users/', '/users')
api.add_resource(ParkingLotResource, '/parking_lots/<int:lot_id>', '/parking_lots')
api.add_resource(ParkingSpotResource, '/parking_spots/<int:spot_id>', '/parking_spots')
api.add_resource(BookingResource, '/bookings/<int:booking_id>', '/bookings')    
# =======================================================
#============== Routes =================================
@app.route('/')
def index():
    return "Welcome to the Parking Management System!"

if __name__ == '__main__':
    
    
    app.run(debug=True)
