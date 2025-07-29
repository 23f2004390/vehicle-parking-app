from flask import Flask, request, redirect, url_for, session,flash,jsonify, render_template, make_response
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
    username = db.Column(db.String(50), nullable=False,unique=True)
    password = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    pin_code = db.Column(db.String(50), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    feedback = db.Column(db.String(150), default="None")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    bookings = db.relationship('Booking', backref='user', lazy=True)
    reviews = db.relationship('Review', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', Admin: {self.is_admin})"


class Parking_lot(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    prime_location_name = db.Column(db.String(150), nullable=False)
    address = db.Column(db.Text, nullable=False)  
    pin_code = db.Column(db.Integer, nullable=False)
    total_spots = db.Column(db.Integer, nullable=False)
    available_spots = db.Column(db.Integer, nullable=False)

    spots = db.relationship('Parking_spot', backref='Parking_lot', lazy=True, cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='Parking_lot', lazy=True)

    def __repr__(self):
        return f"ParkingLot('{self.prime_location_name}', '{self.address}', Total: {self.total_spots}, Available: {self.available_spots})"
    

class Parking_spot(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    is_occupied = db.Column(db.Boolean, default=False)
    parking_cost = db.Column(db.Float, nullable=False, default=-1.0)
    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lot.id'), nullable=False)
    spot_type = db.Column(db.Enum(SpotType), default=SpotType.REGULAR)

    # Relationship to bookings
    bookings = db.relationship('Booking', backref='Parking_spot', lazy=True)

    
    def __repr__(self):
        return f"ParkingSpot(Lot: {self.lot_id}, Spot: {self.spot_number}, Type: {self.spot_type.value}, Occupied: {self.is_occupied})"


class Booking(db.Model):
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
#============== Routes ==================================
# =======================================================



@app.route('/')
def index():
    return render_template('landing.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['user_id'] = user.id
            session['username'] = user.username
            session['is_admin'] = user.is_admin
            flash('Login successful!', 'success')
            return redirect(url_for('user_dashboard') if not user.is_admin else url_for('admin_dashboard'))
        else:
            flash('Invalid credentials. Please try again.', 'danger')
            return redirect(url_for('index'))
    return render_template('landing.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('is_admin', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))
@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        pin_code = request.form['pin_code']
        password = request.form['password']
        email = request.form['email']
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists. Login instead.', 'danger')
            return redirect(url_for('index'))
        
        new_user = User(username=username,pin_code=pin_code, password=password, email=email)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('index'))
    return render_template('landing.html')

@app.route('/admin_dashboard',methods=['GET','POST'])
def admin_dashboard():
    if 'is_admin' not in session or not session['is_admin']:
        flash('Access denied. Admins only.', 'danger')
        return redirect(url_for('index'))
    return render_template("admin.html")

@app.route('/user_dashboard',methods=['GET','POST'])
def user_dashboard():
    return render_template("user.html")



@app.route('/test', methods=['GET'])
def test():
    return render_template('test.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        db.session.commit()
    app.run(debug=True)
