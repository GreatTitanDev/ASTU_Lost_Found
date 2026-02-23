import os
from datetime import timedelta


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'demo-secret-key')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///astu_lost_found.db'

SQLALCHEMY_TRACK_MODIFICATIONS = False
UPLOAD_FOLDER = 'static/uploads'
MAX_CONTENT_LENGTH = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
PERMANENT_SESSION_LIFETIME = timedelta(days=7)
