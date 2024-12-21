from flask import Blueprint, jsonify
from app.utils.role_required import role_required
from app.utils.role_required import permission_required

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard', methods=['GET'])
@role_required('administrador')
def admin_dashboard():
    return jsonify({"message": "Welcome, administrator!"})

@admin_bp.route('/manage-users', methods=['POST'])
@permission_required(3)  # Solo administradores pueden gestionar usuarios

def manage_users():
    
    # Lógica de gestión de usuarios
    return jsonify({"message": "Users managed successfully"}), 200
