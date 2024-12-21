from flask import Flask
from app.connectionPool.pool import MySQLPool
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    #app.config.from_object('app.config.Config')
    app.config['SECRET_KEY'] = 'your_secret_key'
    
    # Inicialización de base de datos
    mysql_pool = MySQLPool()
    # Registrar Blueprints
    from app.routes.auth import auth_bp
    from app.routes.users import users_bp
    from app.routes.admin import admin_bp
    from app.routes.professor import professor_bp
    from app.routes.student import student_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(professor_bp, url_prefix='/professor')
    app.register_blueprint(student_bp, url_prefix='/student')
    return app

