# Vehicle Parking Management System

**Project Submission**  
**Course:** MAD 1 
**Name:** RITURAJ
**Roll Number:** 23f2004390

## 📋 Project Overview

This is a web-based parking management system developed as part of my academic curriculum. The application is built using Flask framework and provides a complete solution for managing parking spaces in various locations. The system allows users to book parking spots, manage their bookings, and provides administrators with tools to oversee the entire parking operation.

### Objectives
- To develop a user-friendly parking booking system
- To provide comprehensive admin management features
- To demonstrate proficiency in web development technologies

## 🚗 Features

### User Features
- **User Registration & Authentication**: Secure login and registration system
- **Parking Spot Booking**: Reserve parking spots with vehicle details
- **Real-time Availability**: Check parking spot availability 
- **Booking Management**: View, modify, and cancel existing bookings
- **Profile Management**: Update personal information and change passwords
- **Feedback System**: Submit feedback and ratings for parking lots
- **Multiple Vehicle Types**: Support for different vehicle types (Car, Bike, etc.)

### Admin Features
- **User Management**: Create, edit, and delete user accounts
- **Parking Lot Management**: Add, modify, and remove parking lots
- **Spot Management**: Configure parking spots (regular and electric)
- **Booking Oversight**: Monitor and manage all bookings
- **System Analytics**: View parking lot statistics and usage data

### Technical Features
- **Responsive Design**: Modern, mobile-friendly interface
- **Database Management**: SQLite database with SQLAlchemy ORM
- **Session Management**: Secure user session handling
- **Flash Messages**: User-friendly notification system
- **Enum-based Status Tracking**: Structured booking and spot status management

## 🛠️ Technology Stack

### Programming Languages & Frameworks
- **Python 3.13+**: Core programming language
- **Flask**: Web framework for backend development
- **SQLAlchemy**: Object-Relational Mapping (ORM) for database operations

### Database
- **SQLite**: Lightweight, serverless database for data storage

### Frontend Technologies
- **HTML5**: Structure and content
- **CSS3**: Styling and responsive design
- **JavaScript**: Client-side interactivity
- **Remix Icons**: Modern icon library

### Development Tools
- **uv**: Modern Python package manager
- **Git**: Version control system

### Learning Outcomes
Through this project, I have gained hands-on experience with:
- Web application development using Flask
- Database design and management
- Frontend development with HTML, CSS, and JavaScript
- User authentication and session management
- Responsive web design principles
- Project structure organization

## 📋 Prerequisites

- Python 3.13 or higher
- uv package manager (recommended) or pip
- Modern web browser

## 🚀 Installation & Setup

### Prerequisites
- Python 3.13 or higher installed on your system
- Basic knowledge of command line operations
- A modern web browser (Chrome, Firefox, Safari, Edge)

### Step-by-Step Installation

1. **Download/Clone the Project**
   ```bash
   # If using Git
   git clone <repository-url>
   cd parking_app_23f2004390
   
   # Or download and extract the ZIP file
   ```

2. **Install Dependencies**
   ```bash
   # Method 1: Using uv (recommended)
   uv sync
   
   # Method 2: Using pip
   pip install flask flask-sqlalchemy flask-login flask-restful
   ```

3. **Run the Application**
   ```bash
   python main.py
   ```

4. **Access the Application**
   - Open your web browser
   - Navigate to: `http://localhost:5000`
   - The application will automatically create the database on first run

### Troubleshooting
- **Port already in use**: Change the port in `main.py` or close other applications using port 5000
- **Module not found**: Ensure all dependencies are installed correctly
- **Database errors**: Delete the `instance/site.db` file and restart the application

## 📁 Project Structure

```
parking_app_23f2004390/
├── main.py                 # Main Flask application
├── pyproject.toml         # Project configuration and dependencies
├── README.md              # This documentation file
├── .gitignore            # Git ignore rules
├── templates/            # HTML templates
│   ├── landing.html      # Landing page with login/register
│   ├── user.html         # User dashboard
│   └── admin.html        # Admin dashboard
├── static/               # Static assets
│   ├── css/             # Stylesheets
│   ├── js/              # JavaScript files
│   └── images/          # Image assets
└── instance/            # Instance-specific files (database)
    └── site.db          # SQLite database
```

## 🗄️ Database Schema

### Core Models

#### User
- `id`: Primary key
- `username`: Unique username
- `password`: User password
- `email`: Unique email address
- `address`: User address
- `is_admin`: Admin privileges flag
- `feedback`: User feedback
- `created_at`: Account creation timestamp

#### Parking_lot
- `id`: Primary key
- `prime_location_name`: Location name
- `address`: Physical address
- `pin_code`: Postal code
- `total_spots`: Total parking spots
- `electric_spots`: Number of electric vehicle spots
- `available_spots`: Currently available spots
- `rating`: Average rating
- `parking_cost`: Cost per hour

#### Parking_spot
- `id`: Primary key
- `is_occupied`: Availability status
- `lot_id`: Foreign key to Parking_lot
- `spot_type`: Regular or Electric

#### Booking
- `id`: Primary key
- `user_id`: Foreign key to User
- `spot_id`: Foreign key to Parking_spot
- `vehicle_number`: License plate
- `vehicle_type`: Type of vehicle
- `start_time`: Booking start time
- `duration`: Duration in hours
- `status`: Active/Completed/Cancelled
- `total_cost`: Total booking cost

## 🎯 How to Use the Application

### For Regular Users

1. **Registration**
   - Click "Sign Up" on the landing page
   - Enter a unique username, email, and password
   - Submit the registration form

2. **Login**
   - Enter your username and password
   - Click "Login" to access your dashboard

3. **Book a Parking Spot**
   - Browse available parking lots
   - Select a parking lot and view available spots
   - Choose your vehicle type and duration
   - Enter your vehicle number
   - Confirm the booking

4. **Manage Your Bookings**
   - View all your current and past bookings
   - Cancel active bookings if needed
   - Check booking status and costs

5. **Profile Management**
   - Update your personal information
   - Change your password
   - Provide feedback on parking lots

### For Administrators

1. **Admin Access**
   - Login with admin credentials
   - Access the admin dashboard

2. **User Management**
   - View all registered users
   - Create new user accounts
   - Edit user information
   - Delete user accounts

3. **Parking Lot Management**
   - Add new parking locations
   - Configure parking spots (regular/electric)
   - Set parking rates
   - Monitor availability

4. **System Overview**
   - View booking statistics
   - Monitor system usage
   - Manage all bookings

## 🔧 Technical Implementation

### Database Design
The application uses a relational database with four main tables:
- **Users**: Store user information and authentication details
- **Parking Lots**: Store parking location information
- **Parking Spots**: Individual parking spaces within lots
- **Bookings**: Track all parking reservations

### Key Features Implementation
1. **User Authentication**: Session-based login system
2. **Real-time Availability**: Dynamic spot status updates
3. **Booking System**: Complete reservation management
4. **Admin Panel**: Comprehensive management interface
5. **Responsive Design**: Mobile-friendly user interface

### Code Organization
- **Models**: Database table definitions using SQLAlchemy
- **Routes**: Flask route handlers for different pages
- **Templates**: HTML files for user interface
- **Static Files**: CSS, JavaScript, and images

## 🔒 Security & Limitations

### Current Security Features
- **Session Management**: Secure user session handling
- **Input Validation**: Form data validation and sanitization
- **SQL Injection Protection**: Uses SQLAlchemy ORM for safe database queries
- **User Authentication**: Login/logout functionality

### Known Limitations (For Academic Purposes)
- **Password Storage**: Passwords are stored in plain text
- **Basic Security**: This is a learning project with basic security measures
- **Local Database**: Uses SQLite



## 🚀 Running the Application

### Development Mode
```bash
python main.py
```
The application will start on `http://localhost:5000`

### Testing the Application
1. **User Testing**:
   - Register a new account
   - Login and explore the user dashboard
   - Try booking a parking spot
   - Test profile management features

2. **Admin Testing**:
   - Login with admin credentials
   - Test user management features
   - Add/modify parking lots
   - Monitor system statistics

### Demo Credentials (For Testing)
- **Regular User**: Register a new account
- **Admin User**: Create an admin account through the database or code

### Screenshots
Include screenshots of key features here:
- Landing page
- User dashboard
- Admin panel
- Booking interface

## 📚 Academic Context

### Learning Objectives Achieved
- **Web Development**: Practical experience with Flask framework
- **Database Management**: Design and implementation of relational databases
- **Frontend Development**: HTML, CSS, and JavaScript integration
- **User Interface Design**: Responsive and user-friendly design principles
- **Project Management**: Complete software development lifecycle

### Skills Demonstrated
- **Programming**: Python, Flask, SQLAlchemy
- **Web Technologies**: HTML5, CSS3, JavaScript
- **Database Design**: SQLite database schema design
- **Problem Solving**: Real-world parking management solution
- **Documentation**: Comprehensive project documentation

### Challenges Faced & Solutions
- **Database Design**: Learned to design efficient database schemas
- **User Authentication**: Implemented session-based login system
- **Real-time Updates**: Managed dynamic parking spot availability
- **Responsive Design**: Created mobile-friendly interface
- **Project Organization**: Structured code for maintainability

## 📝 Conclusion

This project demonstrates my understanding of web development concepts and my ability to create a functional, user-friendly application. Through this project, I have gained practical experience in:

- Full-stack web development
- Database design and management
- User interface design
- Problem-solving and debugging
- Project documentation

The parking management system successfully addresses the real-world problem of parking space management while showcasing various technical skills and concepts learned during my academic journey.

---

**Declaration**: This project is submitted as part of my academic curriculum. All code and documentation have been created by me for educational purposes.
