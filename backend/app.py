import os

from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db
# from app import db
from flask import Flask, jsonify, request
# from models import db, User, Product, Order 
# from routes import routes_bp
import importlib.metadata  # Importar el módulo para obtener la versión



app = Flask(__name__)
CORS(app)


# Configurar la URI de la base de datos
app.config.from_object('config')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/site.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Evitar advertencias
db = SQLAlchemy(app)
# db.init_app(app)


print(importlib.metadata.version("flask"))  


 # Crea la carpeta 'instance' si no existe
if not os.path.exists(app.instance_path):
        os.makedirs(app.instance_path)


@app.before_first_request
def create_tables(): 
    # Obtiene la ruta absoluta de la base de datos
    db_file = os.path.join(app.instance_path, 'site.db')
    print("Ruta de la base de datos:", db_file)  # Imprimir la ruta de la base de datos


# Crear la base de datos y las tablas
# with app.app_context():
    # Crea las tablas si no existen
    db.create_all()



# Obtener la ruta base del directorio donde se encuentra este archivo
basedir = os.path.abspath(os.path.dirname(__file__))

# Construir la ruta completa hacia el archivo site.db dentro de la carpeta instance
DATABASE_PATH = os.path.join(basedir, 'instance', 'site.db')


app.register_blueprint(routes_bp)

# Ruta para la página de inicio mis endpoints
@app.route('/')
def home():
    return "¡Bienvenido a la tienda en línea!"

# Ruta para obtener todos los productos
@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()  # Obtener todos los productos
    return jsonify([{
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': product.price,
        'image_url': product.image_url,
    } for product in products])

# Ruta para obtener un producto específico por ID
@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)  # Obtener producto o 404 si no existe
    return jsonify({
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': product.price,
        'image_url': product.image_url,
    })

# Ruta para crear un nuevo usuario
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()  # Obtener datos del cuerpo de la solicitud
    new_user = User(
        username=data['username'],
        email=data['email'],
        password=data['password']  # Asegúrate de manejar la contraseña adecuadamente
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Usuario creado exitosamente!'}), 201

# Ruta para crear un nuevo pedido
@app.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    new_order = Order(
        user_id=data['user_id'],
        product_id=data['product_id'],
        quantity=data['quantity']
    )
    db.session.add(new_order)
    db.session.commit()
    return jsonify({'message': 'Pedido creado exitosamente!'}), 201


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
