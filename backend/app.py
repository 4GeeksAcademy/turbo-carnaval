import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db
from app import db
from flask import Flask, jsonify, request
from config import Config
from models import db, bcrypt, jwt
# from routes import routes_bp
from routes import routes
import importlib.metadata  # Importar el módulo para obtener la versión
from flask_jwt_extended import JWTManager


app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
bcrypt.init_app(app)
jwt.init_app(app)


# Configuración de JWT
app.config['JWT_SECRET_KEY'] = 'Paletti'  # Cambia esto por una clave segura y única
jwt = JWTManager(app)



# Configurar la URI de la base de datos
app.config.from_object('config')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/site.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Evitar advertencias
# db = SQLAlchemy(app)
db.init_app(app)


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


# Registra el blueprint de rutas
app.register_blueprint(routes, url_prefix='/api')  # Prefijo opcional para las rutas




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
