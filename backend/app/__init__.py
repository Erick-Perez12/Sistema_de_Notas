from flask import Flask
from app.services.database import MySQLPool

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    
    # Inicialización de base de datos
    mysql_pool = MySQLPool()
    
    # Registrar Blueprints
    from app.routes.auth import auth_bp
    from app.routes.users import users_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(users_bp, url_prefix='/users')
    
    return app

