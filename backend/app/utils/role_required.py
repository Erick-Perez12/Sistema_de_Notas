from flask import request, jsonify
from functools import wraps
from app.services.auth_service import authenticate_token
from app.models.user import UserModel
from app.connectionPool.pool import MySQLPool

mysql_pool = MySQLPool()
user_model = UserModel()

def role_required(*roles):
    """
    Decorador para verificar si el usuario autenticado tiene uno de los roles permitidos.
    """
    def wrapper(fn):
        @wraps(fn)
        def decorated(*args, **kwargs):
            # Obtener el token de los headers
            token = request.headers.get('Authorization')
            if not token:
                return jsonify({"message": "Missing token"}), 401

            # Decodificar el token y obtener el ID del usuario
            user_id = authenticate_token(token)
            if not user_id:
                return jsonify({"message": "Invalid or expired token"}), 401

            # Obtener el rol del usuario desde la base de datos
            user = user_model.get_user_by_id(user_id)
            if not user or user["rol"] not in roles:
                return jsonify({"message": "Access denied"}), 403

            # Pasar la validación, ejecutar la función
            return fn(*args, **kwargs)
        return decorated
    return wrapper

def check_permission(user_id, permiso_id):
    """
    Verifica si un usuario tiene un permiso específico basado en su rol.
    """
    sql = """
    SELECT COUNT(*) FROM RolesPermisos rp
    INNER JOIN Usuarios u ON u.rol = rp.rol_id
    WHERE u.id = %s AND rp.permiso_id = %s
    """
    result = mysql_pool.execute(sql, (user_id, permiso_id))
    return result[0][0] > 0  # Retorna True si el usuario tiene el permiso

def permission_required(permiso_id):
    """
    Decorador para proteger rutas según los permisos.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Obtener el token del encabezado de la solicitud
            token = request.headers.get('Authorization')
            if not token:
                return jsonify({'message': 'Token is missing'}), 403

            # Autenticar el token y obtener el ID del usuario
            from app.services.auth_service import authenticate_token
            user_id = authenticate_token(token)
            if not user_id:
                return jsonify({'message': 'Invalid or expired token'}), 403

            # Verificar el permiso
            if not check_permission(user_id, permiso_id):
                return jsonify({'message': 'Access denied'}), 403

            return func(*args, **kwargs)
        return wrapper
    return decorator
