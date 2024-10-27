from flask import Blueprint, jsonify, request
from models import db, User, Product, Order
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

routes = Blueprint('routes', __name__)


# Ruta para la página de inicio 
@routes.route('/')
def home():
    return "¡Bienvenido a la tienda en línea!"

# Ruta para crear un nuevo producto (requiere autenticación)
@routes.route('/products', methods=['POST'])
@jwt_required()  # Esta ruta requiere un token JWT válido
def create_product():
    data = request.get_json()
    product = Product(
        name=data['name'],
        description=data['description'],
        price=data['price'],
        image_url=data.get('image_url', '')  # Optional field
    )
    db.session.add(product)
    db.session.commit()
    return jsonify({'message': 'Producto creado exitosamente!'}), 201

# Ruta para obtener todos los productos
@routes.route('/products', methods=['GET'])
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
@routes.route('/products/<int:product_id>', methods=['GET'])
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
@routes.route('/users', methods=['POST'])
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
@routes.route('/orders', methods=['POST'])
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

# Rutas para el registro y login de usuarios
# Ruta para registrar un nuevo usuario
@routes.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'El usuario ya existe'}), 400

    user = User(
        username=data['username'],
        email=data['email']
    )
    user.set_password(data['password'])  # Hashea y guarda la contraseña
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'Usuario registrado exitosamente!'}), 201


# Ruta para iniciar sesión y obtener un token de acceso
@routes.route('/login', methods=['POST'])
def login():
    data = request.get_json() # Obtiene los datos enviados en el cuerpo de la solicitud
    user = User.query.filter_by(email=data['email']).first() # Busca al usuario por email

    if user and user.check_password(data['password']): # Si el usuario existe y la contraseña es correcta
         # Genera el token JWT con los datos del usuario
        access_token = create_access_token(identity={'id': user.id, 'username': user.username}) 
        return jsonify(access_token=access_token), 200  # Devuelve el token si la autenticación es correcta
    return jsonify({'message': 'Credenciales inválidas'}), 401 # Si falla, devuelve un mensaje de error


# Ejemplo de ruta protegida que requiere autenticación
@routes.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    return jsonify({'message': 'Tienes acceso a esta ruta porque estás autenticado!'})

# CRUD operations for Product
@routes.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([{'id': p.id, 'name': p.name, 'price': p.price} for p in products])

@routes.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get_or_404(id)
    return jsonify({'id': product.id, 'name': product.name, 'price': product.price})

@routes.route('/products', methods=['POST'])
@jwt_required() 
def create_product():
     data = request.get_json()
     product = Product(name=data['name'], description=data['description'], price=data['price'])
     db.session.add(product)
     db.session.commit()
     return jsonify({'message': 'Product created successfully'}), 201
