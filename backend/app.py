from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db 

app = Flask(__name__)
CORS(app)
app.config.from_object('config')

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Usando SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Desactivar modificaciones de seguimiento



db.init_app(app)
from models import db, User, Product, Order

# Crear la base de datos y las tablas
with app.app_context():
    db.create_all()


from routes import routes_bp
app.register_blueprint(routes_bp)
@app.route('/')
def hello():
    return "¡Hola, mundo!"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3001)
