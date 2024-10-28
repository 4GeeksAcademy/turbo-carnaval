from flask_sqlalchemy import SQLAlchemy
from app import db  # Importa la instancia de db desde app.py
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token
from datetime import datetime


bcrypt = Bcrypt()
jwt = JWTManager()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    orders = db.relationship('Order', backref='user', lazy=True)

def set_password(self, password):
        #  Hashea la contraseña y la guarda en `password_hash`
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

def check_password(self, password):
        #  Verifica si la contraseña proporcionada coincide con el hash almacenado.
        return bcrypt.check_password_hash(self.password, password)

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(500), nullable=True)  # URL de la imagen

    def __repr__(self):
        return f'<Product {self.name}>'  # Representación del objeto Product


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f'<Order {self.id} by User {self.user_id}>'  # Representación del objeto Order
