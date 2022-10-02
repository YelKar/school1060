import os


class Config(object):
    """Configuration object for app"""

    SECRET_KEY = os.environ.get('SECRET_KEY') or "qwertyuiop"  # Creating secret key for forms
    DEBUG = True  # Activating debug mode
    SQLALCHEMY_DATABASE_URI = "sqlite:///db.db"  # route to database

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    FLASK_ADMIN_SWATCH = "solar"
