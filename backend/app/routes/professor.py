from flask import Blueprint, jsonify, request
from app.utils.role_required import role_required
from app.utils.role_required import permission_required

professor_bp = Blueprint('professor', __name__)
notes_bp = Blueprint('notes', __name__)

@professor_bp.route('/dashboard', methods=['GET'])
@role_required('profesor')
def professor_dashboard():
    return jsonify({"message": "Welcome, professor!"})


@notes_bp.route('/edit', methods=['PUT'])
@permission_required(2)  # Permiso para editar notas
def edit_notes():
    data = request.get_json()
    # Lógica para editar notas
    return jsonify({"message": "Note edited successfully"}), 200
