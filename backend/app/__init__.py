from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    
    db.init_app(app)
    bcrypt.init_app(app)
    
    # Registrar Blueprints
    from app.routes.auth import auth_bp
    from app.routes.users import users_bp
    from app.routes.notes import notes_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(notes_bp, url_prefix='/notes')
    
    return app
