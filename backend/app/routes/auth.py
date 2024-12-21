from flask import Blueprint, request, jsonify
from app.models.user import UserModel
from app import bcrypt, db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = UserModel.add_user(nombre=data['nombre'], email=data['email'], contrasena=hashed_password, rol=data['rol'])
    if new_user:
    #db.session.add(new_user)
    #db.session.commit()
        return jsonify({'message': 'User registered successfully'}), 201
    else:
        return jsonify({'message': 'No successfully'}), 404

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user_data = UserModel.get_by_email(email=data['email'])

    if not user_data:
        return jsonify({'message': 'Invalid credentials'}), 401

    user = user_data  # user_data es una lista
    stored_password = user[3]

    # Verificar si el hash está en el formato esperado
    if isinstance(stored_password, str) and bcrypt.check_password_hash(stored_password, data['password']):
        return jsonify({'message': 'Login successful', 'rol': user[4]}), 200

    return jsonify({'message': 'Invalid credentials'}), 401

