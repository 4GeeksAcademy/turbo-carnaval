import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'mysecret')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'your_jwt_secret_key_here'
    STRIPE_API_KEY = os.getenv('STRIPE_API_KEY')
    CLOUDINARY_URL = os.getenv('CLOUDINARY_URL')
