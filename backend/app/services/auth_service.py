from app.models.user import UserModel
from flask import jsonify, current_app
from werkzeug.security import check_password_hash
import jwt
import datetime

# Crear una instancia de UserModel para interactuar con la base de datos
user_model = UserModel()

def register_user(data: dict):
    """
    Registra un nuevo usuario en el sistema.
    Verifica si el usuario ya existe por email.
    """
    # Verificar si el usuario ya existe
    existing_user = user_model.get_by_email(data["email"])
    if existing_user:
        return jsonify({"message": "User already exists"}), 400

    # Agregar el nuevo usuario a la base de datos
    user_model.add_user(data)
    return jsonify({"message": "User registered successfully"}), 201

def login_user(data: dict):
    """
    Inicia sesión de un usuario verificando las credenciales.
    """
    # Recuperar al usuario por email
    user = user_model.get_by_email(data["email"])
    if not user:
        return jsonify({"message": "Invalid credentials"}), 401

    # Verificar si la contraseña es correcta usando la función de hash
    encrypted_password = user["contrasena"]
    if not check_password_hash(encrypted_password, data["password"]):
        return jsonify({"message": "Invalid credentials"}), 401

    # Generar un token JWT si las credenciales son válidas
    token = generate_jwt_token(user["id"])

    return jsonify({
        "message": "Login successful",
        "token": token
    }), 200

def generate_jwt_token(user_id):
    """
    Genera un token JWT para la autenticación de usuario.
    El token incluirá el ID del usuario y el tiempo de expiración.
    """
    SECRET_KEY = current_app.config['SECRET_KEY']  # Definir aquí SECRET_KEY
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    token = jwt.encode({
        "user_id": user_id,
        "exp": expiration_time
    }, SECRET_KEY, algorithm="HS256")

    return token

def authenticate_token(token):
    """
    Decodifica y verifica el token JWT.
    :param token: token JWT
    :return: ID de usuario si el token es válido, de lo contrario None
    """
    SECRET_KEY = current_app.config['SECRET_KEY']  # Definir aquí SECRET_KEY
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded_token["user_id"]
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
