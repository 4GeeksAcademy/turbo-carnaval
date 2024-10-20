import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    STRIPE_API_KEY = os.getenv('STRIPE_API_KEY')
    CLOUDINARY_URL = os.getenv('CLOUDINARY_URL')
