# ASTU Digital Lost & Found System

A FullStack web application built with Flask for reporting, searching, and claiming lost and found items at ASTU (Adama Science and Technology University).

## Project Overview

This project includes all the required features for a complete lost and found system with proper security implementations.

## Features

- User Registration & Login
- Report Lost Items
- Report Found Items
- Image Upload for Items
- Search & Filter (by category, date, location)
- Claim Request Submission
- Admin Dashboard with Statistics
- Admin Approval/Rejection Workflow
- Role-Based Access Control (RBAC)

## Security Features

- Password hashing with Werkzeug
- CSRF protection with Flask-WTF
- Role-based access control
- Secure file upload handling
- Input validation
- Session management

## Tech Stack

- **Backend**: Python Flask
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML5, Bootstrap 5, Jinja2
- **Authentication**: Flask-Login

## Project Structure

```
astu_lost_found/
├── app/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── item.py
│   │   └── claim.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── auth.py
│   │   ├── items.py
│   │   └── admin.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── about.html
│   │   ├── auth/
│   │   │   ├── login.html
│   │   │   ├── register.html
│   │   │   └── profile.html
│   │   ├── items/
│   │   │   ├── report.html
│   │   │   ├── search.html
│   │   │   ├── detail.html
│   │   │   ├── claim.html
│   │   │   └── my_items.html
│   │   └── admin/
│   │       ├── dashboard.html
│   │       ├── claims.html
│   │       ├── items.html
│   │       └── users.html
│   └── static/
│       └── uploads/
├── config.py
├── requirements.txt
└── run.py
```

## Setup Instructions

1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python run.py
   ```

5. Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

## Demo Accounts

- **Admin**: admin@astu.edu / admin123
- **Student**: Register a new account

## License

This project is for educational purposes.
