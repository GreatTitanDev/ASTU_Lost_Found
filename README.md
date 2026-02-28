# ASTU Digital Lost & Found System

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.3.x-000000?style=for-the-badge&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)
![Deployed on Render](https://img.shields.io/badge/Render-Deployed-46E3B7?style=for-the-badge&logo=render&logoColor=white)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

A full-stack web application built for **Adama Science and Technology University (ASTU)** to help students report, search, and claim lost and found items on campus. The system streamlines the process of reuniting students with their belongings through an intuitive interface and role-based workflow.

<div align="center">
  <img src="https://via.placeholder.com/800x400/2c3e50/ffffff?text=ASTU+Lost+Found+System" alt="ASTU Lost & Found System Screenshot" width="800"/>
  <br><small>Placeholder for system screenshot (replace with real screenshot later)</small>
</div>

## Live Demo

The application is live and accessible at:  
👉 https://astu-lostfound.onrender.com

## Features

| Feature              | Description                                                  |
|----------------------|--------------------------------------------------------------|
| User Authentication  | Secure registration and login system with password hashing   |
| Report Lost Items    | Submit detailed reports for lost belongings with images      |
| Report Found Items   | Log found items to help others locate their property         |
| Image Upload         | Upload and manage item images securely                       |
| Search & Filter      | Find items by category, date, location, and status           |
| Claim Requests       | Submit claims with proof descriptions for found items        |
| Admin Dashboard      | Comprehensive statistics and management interface            |
| Approval Workflow    | Admin review system for claim requests                       |
| Role-Based Access    | Different permissions for students and administrators        |

## Security Implementations

- Password hashing using Werkzeug security
- CSRF protection with Flask-WTF
- Session-based authentication with Flask-Login
- Secure file upload validation (allowed extensions, size limit)
- Input sanitization and validation
- Role-based access control middleware

## Technology Stack

### Backend Framework
- Flask (Python web framework)
- Flask-SQLAlchemy (ORM)
- Flask-Login (Authentication)
- Flask-WTF (Form handling & CSRF)
- Werkzeug (Security utilities)

### Database
- SQLite (for development)
- SQLAlchemy (database abstraction)

### Frontend
- HTML5
- Bootstrap 5
- Jinja2 Templating
- CSS3

### Deployment
- Gunicorn (WSGI server)
- Render (cloud platform)

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
│   │   ├── auth.py
│   │   ├── main.py
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
├── run.py
└── README.md
```

## Installation

Follow these steps to set up the project locally:

1. **Clone the repository**

```bash
git clone https://github.com/greattitandev/astu_lost_found.git
cd astu_lost_found
```

2. **Create virtual environment**

```bash
python -m venv venv
```

3. **Activate virtual environment**

**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

4. **Install dependencies**

```bash
pip install -r requirements.txt
```

5. **Run the application**

```bash
python run.py
```

6. **Access the application**  
Open your browser and navigate to:  
http://localhost:5000

## Deployment (Render)

The application is deployed on Render using Gunicorn as the WSGI server.

**Render Configuration**
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn run:app`
- **Python Version**: 3.9+

**Environment Variables**
- `FLASK_ENV`: production
- `SECRET_KEY`: [Your secure secret key]
- `DATABASE_URL`: SQLite database path (or upgrade to PostgreSQL later)

## Demo Credentials

| Role    | Email              | Password    |
|---------|--------------------|-------------|
| Admin   | admin@astu.edu     | admin123    |
| Student | Register new account | User-defined |

> **Note**: Change the default admin password in production!

## License

This project is developed for educational purposes at Adama Science and Technology University.  
It is licensed under the **MIT License**.

See the [LICENSE](LICENSE) file for details.

---

**Developed by ASTU Student • 2026**
