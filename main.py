from flask import Flask, request, redirect, url_for, session, flash, render_template
from flask_sqlalchemy import SQLAlchemy
import os 
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'rituraj-secretkey'
db = SQLAlchemy(app)

# =======================================================
#============== Models =================================
# ======================================================
import enum

class SpotType(enum.Enum):
    REGULAR = 'regular'
    ELECTRIC = 'electric'

class BookingStatus(enum.Enum):
    ACTIVE = 'active'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    address = db.Column(db.Text, nullable=True, default="None")
    is_admin = db.Column(db.Boolean, default=False)
    feedback = db.Column(db.String(150), default="None")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    bookings = db.relationship('Booking', backref='user')

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', Admin: {self.is_admin})"

class Parking_lot(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    prime_location_name = db.Column(db.String(150), nullable=False)
    address = db.Column(db.Text, nullable=False)  
    pin_code = db.Column(db.Integer, nullable=False)
    total_spots = db.Column(db.Integer, nullable=False)
    electric_spots = db.Column(db.Integer, nullable=True, default=0)
    available_spots = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Float, nullable=True, default=0.0)
    parking_cost = db.Column(db.Float, nullable=False)

    spots = db.relationship('Parking_spot', backref='Parking_lot', cascade='all, delete-orphan')
    

    def __repr__(self):
        return f"ParkingLot('{self.prime_location_name}', '{self.address}', Total: {self.total_spots}, Available: {self.available_spots})"

class Parking_spot(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    is_occupied = db.Column(db.Boolean, default=False)
    lot_id = db.Column(db.Integer, db.ForeignKey('parking_lot.id'), nullable=False)
    spot_type = db.Column(db.Enum(SpotType), default=SpotType.REGULAR)

    # Relationship to bookings
    bookings = db.relationship('Booking', backref='Parking_spot')

    
    def __repr__(self):
        return f"ParkingSpot(Lot: {self.lot_id}, Type: {self.spot_type.value}, Occupied: {self.is_occupied})"

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    spot_id = db.Column(db.Integer, db.ForeignKey('parking_spot.id'), nullable=False)
    vehicle_number = db.Column(db.String(15), nullable=False)
    vehicle_type = db.Column(db.String(10), default="Car")  
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    duration = db.Column(db.Integer, nullable=False)  # Duration in hours
    status = db.Column(db.Enum(BookingStatus), default=BookingStatus.ACTIVE)  
    total_cost = db.Column(db.Float, nullable=False)
    

    def __repr__(self):
        return f"Booking(User ID: {self.user_id}, Spot ID: {self.spot_id}, Start: {self.start_time})"

# ======================================================
#============== Routes ==================================
# =====================================================

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
        password = request.form['password']
        email = request.form['email']
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists. Login instead.', 'danger')
            return redirect(url_for('index'))
        
        new_user = User(username=username, password=password, email=email)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('index'))
    return render_template('landing.html')

@app.route('/admin_dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    if 'is_admin' not in session or not session['is_admin']:
        flash('Access denied. Admins only.', 'danger')
        return redirect(url_for('index'))
    parking_lots = Parking_lot.query.all()
    users = User.query.all()
    bookings = Booking.query.all()
    print(parking_lots)
    return render_template("admin.html", parking_lots=parking_lots, users=users, bookings=bookings)

@app.route('/user_dashboard', methods=['GET', 'POST'])
def user_dashboard():
    if 'user_id' not in session:
        flash('Please log in to access your dashboard.', 'danger')
        return redirect(url_for('index'))
    
    user = User.query.get(session['user_id'])
    if not user:
        flash('User not found. Please log in again.', 'danger')
        session.pop('user_id', None)
        return redirect(url_for('index'))
    
    # Get bookings with parking lot information
    bookings = db.session.query(Booking).filter_by(user_id=user.id).all()
    parking_lots = Parking_lot.query.all()
    return render_template("user.html", user=user, bookings=bookings, parking_lots=parking_lots)

# ===== ADMIN USER MANAGEMENT =====

@app.route("/user_create", methods=['GET', 'POST'])
def user_create():
    if 'is_admin' not in session or not session['is_admin']:
        flash('Access denied. Admins only.', 'danger')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        address = request.form['address']
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists. Please choose a different username.', 'danger')
            return redirect(url_for('admin_dashboard'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists. Please use a different email address.', 'danger')
            return redirect(url_for('admin_dashboard'))
        
        new_user = User(username=username, password=password, email=email, address=address)
        db.session.add(new_user)
        db.session.commit()
        flash('User created successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    return redirect(url_for('index'))

@app.route("/user_edit", methods=['POST'])
def user_edit():
    if 'is_admin' not in session or not session['is_admin']:
        flash('Access denied. Admins only.', 'danger')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        user_id = request.form['user_id']
        name = request.form['name']
        email = request.form['email']
        address = request.form['address']
        password = request.form.get('password', '')
        
        user = User.query.get(user_id)
        if user:
            existing_user = User.query.filter_by(username=name).first()
            if existing_user and existing_user.id != int(user_id):
                flash('Username already exists. Please choose a different username.', 'danger')
                return redirect(url_for('admin_dashboard'))
            
            existing_email = User.query.filter_by(email=email).first()
            if existing_email and existing_email.id != int(user_id):
                flash('Email already exists. Please use a different email address.', 'danger')
                return redirect(url_for('admin_dashboard'))
            
            user.username = name
            user.email = email
            user.address = address
            if password:
                user.password = password
            db.session.commit()
            flash('User updated successfully!', 'success')
        else:
            flash('User not found!', 'danger')
        return redirect(url_for('admin_dashboard'))

@app.route("/user_delete", methods=['POST'])
def user_delete():
    if 'is_admin' not in session or not session['is_admin']:
        flash('Access denied. Admins only.', 'danger')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        user_id = request.form['user_id']
        user = User.query.get(user_id)
        if user:
            db.session.query(Booking).filter_by(user_id=user_id).delete()
            db.session.delete(user)
            db.session.commit()
            flash('User deleted successfully!', 'success')
        else:
            flash('User not found!', 'danger')
        return redirect(url_for('admin_dashboard'))

# ===== ADMIN PARKING LOT MANAGEMENT =====

@app.route("/lot_edit", methods=['POST'])
def lot_edit():
    if 'is_admin' not in session or not session['is_admin']:
        flash('Access denied. Admins only.', 'danger')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        id = request.form['lot_id']
        prime_location_name = request.form['prime_location_name']
        address = request.form['address']
        pin_code = request.form['pin_code']
        total_spots = int(request.form['total_spots'])
        cost = float(request.form['cost'])
        lot = db.session.get(Parking_lot, id)
        if lot:
            old_total_spots = lot.total_spots
            available_spots = lot.available_spots
            lot.prime_location_name = prime_location_name
            lot.address = address
            lot.pin_code = pin_code
            lot.parking_cost = cost
            spots_difference = total_spots - old_total_spots
            lot.available_spots = available_spots + spots_difference
            lot.total_spots = total_spots
            if spots_difference > 0:#spots added or incease
                for i in range(spots_difference):
                    new_spot = Parking_spot(is_occupied=False, spot_type=SpotType.REGULAR, Parking_lot=lot)
                    db.session.add(new_spot)
            elif spots_difference < 0: #spots removed or decrease
                spots_to_remove = abs(spots_difference)
                spots = Parking_spot.query.filter_by(lot_id=lot.id, is_occupied=False).limit(spots_to_remove).all()
                for spot in spots:
                    db.session.delete(spot)
            db.session.add(lot)
            
            db.session.commit()
            flash('Parking lot updated successfully!', 'success')
        else:
            flash('Parking lot not found!', 'danger')
        return redirect(url_for('admin_dashboard'))

@app.route("/lot_delete", methods=['POST'])
def lot_delete():
    if 'is_admin' not in session or not session['is_admin']:
        flash('Access denied. Admins only.', 'danger')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        lot_id = request.form['lot_id']
        lot = Parking_lot.query.get(lot_id)
        if lot:
            try :
                for spot in lot.spots:
                    spot.is_occupied = False
                    db.session.delete(spot)
                db.session.delete(lot)
                db.session.commit()
                flash('Parking lot deleted successfully!', 'success')
            except Exception as e:
                db.session.rollback()
                flash('Failed error!!! please release all bookings first', 'danger')
        else:
            flash('Parking lot not found!', 'danger')
        return redirect(url_for('admin_dashboard'))

@app.route('/create_parking_lot', methods=['POST'])
def create_parking_lot():
    if 'is_admin' not in session or not session['is_admin']:
        flash('Access denied. Admins only.', 'danger')
        return redirect(url_for('index'))

    prime_location_name = request.form['prime_location_name']
    address = request.form['address']
    pin_code = request.form['pin_code']
    total_spots = int(request.form['total_spots'])
    electric_spots = int(request.form['electric_spots'])
    price_per_hour = request.form['price_per_hour']
    
    if electric_spots > total_spots:
        flash('Electric spots cannot exceed total spots.', 'danger')
        return redirect(url_for('admin_dashboard'))
    
    new_lot = Parking_lot(
        prime_location_name=prime_location_name,
        address=address,
        pin_code=pin_code,
        total_spots=total_spots,
        available_spots=total_spots,
        parking_cost=price_per_hour
    )
    
    # Create parking spots for the new lot
    for i in range(total_spots):
        new_spot = Parking_spot(is_occupied=False, spot_type=SpotType.REGULAR, Parking_lot=new_lot)
        db.session.add(new_spot)
    
    db.session.add(new_lot)
    db.session.commit()
    
    flash('Parking lot created successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

# ===== USER PROFILE MANAGEMENT =====

@app.route("/update-profile", methods=['POST'])
def update_profile():
    if 'user_id' not in session:
        flash('Please log in to update your profile.', 'danger')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        user_id = session['user_id']
        username = request.form['username']
        email = request.form['email']
        address = request.form.get('address', '')
        
        user = User.query.get(user_id)
        if user:
            existing_user = User.query.filter_by(username=username).first()
            if existing_user and existing_user.id != user_id:
                flash('Username already exists. Please choose a different username.', 'danger')
                return redirect(url_for('user_dashboard'))
            
            existing_email = User.query.filter_by(email=email).first()
            if existing_email and existing_email.id != user_id:
                flash('Email already exists. Please use a different email address.', 'danger')
                return redirect(url_for('user_dashboard'))
            
            user.username = username
            user.email = email
            user.address = address if address else "None"
            db.session.commit()
            flash('Profile updated successfully!', 'success')
        else:
            flash('User not found!', 'danger')
        return redirect(url_for('user_dashboard'))

@app.route("/change-password", methods=['POST'])
def change_password():
    if 'user_id' not in session:
        flash('Please log in to change your password.', 'danger')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        user_id = session['user_id']
        current_password = request.form.get('current_password', '')
        new_password = request.form.get('new_password', '')
        confirm_password = request.form.get('confirm_password', '')
        
        user = User.query.get(user_id)
        if user and user.password == current_password:
            if new_password == confirm_password:
                user.password = new_password
                db.session.commit()
                flash('Password changed successfully!', 'success')
            else:
                flash('New passwords do not match!', 'danger')
        else:
            flash('Current password is incorrect!', 'danger')
        return redirect(url_for('user_dashboard'))

# ===== BOOKING MANAGEMENT =====

@app.route("/release_booking", methods=['POST'])
def release_booking():
    if 'user_id' not in session:
        flash('Please log in to release booking.', 'danger')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        booking_id = request.form.get('booking_id')
        booking = Booking.query.get(booking_id)
        
        # Allow admin to release any booking, or user to release their own
        if booking and (session.get('is_admin') or booking.user_id == session['user_id']):
            booking.status = BookingStatus.COMPLETED
            spot = Parking_spot.query.get(booking.spot_id)
            if spot:
                lot = Parking_lot.query.get(spot.lot_id)
                lot.available_spots = lot.available_spots + 1
                spot.is_occupied = False
            db.session.commit()
            flash('Booking released successfully!', 'success')
        else:
            flash('Booking not found or access denied!', 'danger')
        
        # Redirect based on user type
        if session.get('is_admin'):
            return redirect(url_for('admin_dashboard'))
        else:
            return redirect(url_for('user_dashboard'))
@app.route("/release_all", methods=['POST'])
def release_all():
    if request.method == 'POST':
        lots = Parking_lot.query.all()
        if lots:
            # Update all active bookings to completed
            active_bookings = Booking.query.filter_by(status=BookingStatus.ACTIVE).all()
            for booking in active_bookings:
                booking.status = BookingStatus.COMPLETED
            
            # Reset all spots and lot availability
            for lot in lots:
                for spot in lot.spots:
                    spot.is_occupied = False
                lot.available_spots = lot.total_spots
            
            db.session.commit()
            flash('All spots released successfully!', 'success')
        else:
            flash('Parking lot not found!', 'danger')
        return redirect(url_for('admin_dashboard'))


@app.route('/booking_lot', methods=['POST'])
def booking_lot():
    if 'user_id' not in session:
        flash('Please log in to book a spot.', 'danger')
        return redirect(url_for('index'))
    
    user_id = session['user_id']
    lot_id = request.form['spot_id']
    vehicle_number = request.form['vehicle_number']
    vehicle_type = request.form['vehicle_type']
    duration = request.form['duration']
    
    parking_lot = Parking_lot.query.get(lot_id)
    if not parking_lot:
        flash('Parking lot not found!', 'danger')
        return redirect(url_for('user_dashboard'))
    
    # Find an available parking spot in this lot
    available_spot = Parking_spot.query.filter_by(lot_id=lot_id, is_occupied=False).first()
    if not available_spot:
        flash('No available spots in this parking lot!', 'danger')
        return redirect(url_for('user_dashboard'))
    
    total_cost = int(parking_lot.parking_cost) * int(duration)
    
    new_booking = Booking(
        user_id=user_id, 
        spot_id=available_spot.id,  
        vehicle_number=vehicle_number, 
        vehicle_type=vehicle_type, 
        duration=int(duration), 
        total_cost=total_cost
    )   
    
    available_spot.is_occupied = True
    parking_lot.available_spots = parking_lot.available_spots - 1
    db.session.add(new_booking)

    db.session.commit()
    
    flash('Booking created successfully!', 'success')
    if session['is_admin']:
        return redirect(url_for('admin_dashboard'))
    else:
        return redirect(url_for('user_dashboard'))

# ===== FEEDBACK =====

@app.route("/feedback", methods=['POST'])
def feedback():
    if request.method == 'POST':
        feedback = request.form['feedback']
        user = User.query.get(session['user_id'])
        user.feedback = feedback
        db.session.commit()
        flash('Thank you for your feedback! We will get back to you soon.', 'success')
        return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # Create admin user if not exists
        if not User.query.filter_by(username='admin').first():
            admin_user = User(username='admin', password='admin', email='admin@test.com', address="admin", is_admin=True)
            db.session.add(admin_user)
            db.session.commit()
    
    app.run(debug=True, port=5000, host='0.0.0.0')
