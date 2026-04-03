from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from ..models.user import User
from ..utils.decorators import role_required
from .. import db

users_bp = Blueprint('users', __name__)


@users_bp.route('', methods=['GET'])
@jwt_required()
@role_required('admin')
def list_users():
    return jsonify({'users': [u.to_dict() for u in User.query.all()]}), 200


@users_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
@role_required('admin')
def get_user(user_id):
    user = User.query.get_or_404(user_id, description='User not found.')
    return jsonify({'user': user.to_dict()}), 200


@users_bp.route('/<int:user_id>/role', methods=['PATCH'])
@jwt_required()
@role_required('admin')
def update_role(user_id):
    data = request.get_json()
    role = data.get('role') if data else None
    if role not in ['viewer', 'analyst', 'admin']:
        return jsonify({'error': "Role must be 'viewer', 'analyst', or 'admin'."}), 422
    user = User.query.get_or_404(user_id, description='User not found.')
    user.role = role
    db.session.commit()
    return jsonify({'message': f'Role updated to {role}.', 'user': user.to_dict()}), 200


@users_bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
@role_required('admin')
def delete_user(user_id):
    user = User.query.get_or_404(user_id, description='User not found.')
    user.is_active = False
    db.session.commit()
    return jsonify({'message': f'User {user.username} deactivated.'}), 200
