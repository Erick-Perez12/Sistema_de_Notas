from flask import Blueprint, jsonify
from app.utils.role_required import role_required

student_bp = Blueprint('student', __name__)

@student_bp.route('/dashboard', methods=['GET'])
@role_required('estudiante')
def student_dashboard():
    return jsonify({"message": "Welcome, student!"})
