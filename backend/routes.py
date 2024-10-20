from flask import Blueprint

routes_bp = Blueprint('routes', __name__)

# Define tus rutas aquí
@routes_bp.route('/')
def home():
    return "Hello from routes!"
