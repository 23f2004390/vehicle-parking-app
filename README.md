# Vehicle Parking App - Project Overview and Guide

## Project Name: WhereMyCarApp

This project is a web-based Vehicle Parking App designed to simplify the process of finding and booking parking spots. It provides a user-friendly platform for drivers to locate available spaces and for administrators to manage the parking lot efficiently. The system is built with Python, Flask, and SQLAlchemy.

## About

**Name:** RITURAJ  
**Student ID / Roll Number:** 23f2004390  
**Email ID:** 23f2004390@ds.study.iitm.ac.in  
**Course:** MAD 1 projects (vehicle parking app)

##vedio link :
[text](https://drive.google.com/file/d/1H1DbyURpYwboSBKUN4sO499omZuvefg1/view?usp=sharing)
https://drive.google.com/file/d/1H1DbyURpYwboSBKUN4sO499omZuvefg1/view?usp=sharing



This application was created as part of the curriculum requirements, demonstrating skills in web development, database management, and backend programming.

## Key Features

### Two Main Parts
The application provides separate views for users and administrators.

### User Features
- **Account Management:** Easy sign-up and login functionality
- **Parking Search:** View the list of available parking spots and book one
- **Booking System:** Book an available spot for a specific duration
- **History:** View past and active parking spot bookings
- **Profile Management:** Update personal information and password
- **Feedback System:** Submit feedback about the service

### Administrator Features
- **Secure Login:** Using sessions, secure login for the management dashboard for both user and admin
- **Lot Overview:** See the status of all parking spots at a glance (occupied vs free)
- **User Management:** View and manage all registered user accounts
- **Booking Tracking:** Monitor all active and past bookings
- **Parking Lot Management:** Create, update, and delete parking lots
- **Manual Updates:** Manually change the status of any parking spot
- **Bulk Operations:** Release all bookings at once

## The Technology Behind the App

### Backend (The Engine)
- Built with **Python** and the **Flask** framework (Core functionality)
- Handles all server-side logic, including user management, booking processing, and database communication
- Uses **Flask-SQLAlchemy** for ORM and database operations

### Frontend (What You See)
- **HTML:** Provides the basic structure of the web pages
- **CSS:** Used for all styling, including colors, fonts, and layout
- **JavaScript:** Makes the pages interactive and dynamic

### Database
- Uses **SQLite**
- Stores all user information, parking spot data, booking records, and parking lot information

## How to Get the App Running

### Prerequisites
Make sure you have Python installed on your system, then install the required packages:

```bash
pip install Flask Flask-SQLAlchemy
```

### Start the Application
1. Navigate to the project directory in your terminal
2. Run the following command:
   ```bash
   python main.py
   ```

### Use the App in Your Browser
- The terminal will show the server is running, usually at `http://127.0.0.1:5000/`
- Open this address in your web browser to see the application's landing page

### Default Admin Access
- **Username:** admin
- **Password:** admin
- **Email:** admin@test.com

## Database Schema

The database consists of four main tables to manage the application's data:

### User Table
Stores information about registered users.
- `id`: Unique ID for each user (Primary Key)
- `username`: The user's unique name for logging in
- `email`: The user's unique email address
- `password`: The user's password
- `address`: User's address (optional)
- `is_admin`: A flag to check if the user is an administrator (True/False)
- `feedback`: User feedback storage
- `created_at`: Account creation timestamp

### Parking Lot Table
Stores information about each parking facility.
- `id`: Unique ID for each parking lot (Primary Key)
- `prime_location_name`: Short name or nickname
- `address`: The address or description of the lot's location
- `pin_code`: Postal code of the location
- `total_spots`: Total number of parking spots
- `electric_spots`: Number of electric vehicle spots
- `available_spots`: Currently available spots
- `rating`: Average rating of the parking lot
- `parking_cost`: Cost per hour for parking

### Parking Spot Table
Stores information about each individual spot within a lot.
- `id`: Unique ID for each parking spot (Primary Key)
- `lot_id`: Links to the Parking Lot this spot belongs to (Foreign Key)
- `is_occupied`: A flag to check if the spot is currently occupied (True/False)
- `spot_type`: Type of spot (regular/electric)

### Booking Table
Links users to the parking spots they have booked.
- `id`: Unique ID for each booking (Primary Key)
- `user_id`: The ID of the user who made the booking (links to the User table)
- `spot_id`: The ID of the parking spot that was booked (links to the Parking Spot table)
- `vehicle_number`: License plate number of the vehicle
- `vehicle_type`: Type of vehicle (Car, Bike, etc.)
- `start_time`: The date and time when the booking begins
- `duration`: Duration of booking in hours
- `status`: Current status (active/completed/cancelled)
- `total_cost`: Total cost of the booking

## File Structure

The project is organized into several key folders and files:

```
/
|-- main.py                 # Main Flask application file
|-- instance/
|   |-- site.db             # SQLite database file
|-- static/
|   |-- css/                # Stylesheets for the application
|   |   |-- admin.css
|   |   |-- landing.css
|   |   `-- user.css
|   |-- js/                 # JavaScript files for interactivity
|   |   |-- dashboard.js
|   |   |-- landing.js
|   |   |-- user.js
|   |   `-- user_search.js
|   `-- images/             # Image assets used in the app
|       |-- available_spot.jpg
|       |-- bg_landing_page.jpg
|       |-- landing-page.png
|       |-- parking_ui.png
|       `-- phone_parking.jpg
|-- templates/              # HTML templates for different pages
|   |-- admin.html          # Admin dashboard page
|   |-- landing.html        # Main landing page
|   `-- user.html           # User dashboard page
|-- .python-version         # Specifies the Python version
`-- README.md               # Project documentation
```



## Application Features
### User Registration and Authentication
- New users can register with username, email, and password
- Secure login system with session management
- Password change functionality for existing users

### Parking Lot Management (Admin)
- Create new parking lots with location details
- Edit existing parking lot information
- Delete parking lots (with proper booking cleanup)
- View all parking lots with availability status

### Booking System
- Users can book available parking spots
- Real-time availability updates
- Cost calculation based on duration and hourly rate
- Booking history tracking

### Administrative Controls
- User management (create, edit, delete users)
- Booking oversight and management
- System-wide operations (release all bookings)
- Comprehensive dashboard with statistics

## Quick Start

1. **Install Dependencies:**
   ```bash
   pip install Flask Flask-SQLAlchemy
   ```

2. **Run the App:**
   ```bash
   python main.py
   ```

3. **Open in Browser:**
   Go to `http://127.0.0.1:5000/` in your web browser

4. **Access Admin Panel:**
   Login with username: `admin`, password: `admin`

