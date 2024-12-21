from flask import Blueprint, jsonify, request
from app.services.user_service import get_all_users, create_user

users_bp = Blueprint('users', __name__)

@users_bp.route('/', methods=['GET'])
def list_users():
    users = get_all_users()
    return jsonify(users)

@users_bp.route('/', methods=['POST'])
def add_user():
    data = request.get_json()
    create_user(data['nombre'], data['email'], data['contrasena'], data['rol'])
    return jsonify({"message": "User created successfully"}), 201
