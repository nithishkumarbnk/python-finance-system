from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from ..models.user import User
from ..utils.validators import validate_user_data
from .. import db

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Request body must be JSON.'}), 400

    is_valid, errors = validate_user_data(data)
    if not is_valid:
        return jsonify({'error': 'Validation failed.', 'details': errors}), 422

    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already taken.'}), 409
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered.'}), 409

    user = User(username=data['username'].strip(), email=data['email'].strip(), role='viewer')
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()

    # Store identity as string — flask-jwt-extended 4.x requires string subject
    token = create_access_token(identity=str(user.id))
    return jsonify({'message': 'Registration successful.', 'user': user.to_dict(), 'access_token': token}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Request body must be JSON.'}), 400

    identifier = data.get('username') or data.get('email')
    password   = data.get('password')

    if not identifier or not password:
        return jsonify({'error': 'Username/email and password are required.'}), 400

    user = (User.query.filter_by(username=identifier).first() or
            User.query.filter_by(email=identifier).first())

    if not user or not user.check_password(password):
        return jsonify({'error': 'Invalid credentials.'}), 401
    if not user.is_active:
        return jsonify({'error': 'Account is deactivated. Contact an administrator.'}), 403

    # Store identity as string — flask-jwt-extended 4.x requires string subject
    token = create_access_token(identity=str(user.id))
    return jsonify({'message': 'Login successful.', 'user': user.to_dict(), 'access_token': token}), 200


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def me():
    user = User.query.get(int(get_jwt_identity()))
    if not user:
        return jsonify({'error': 'User not found.'}), 404
    return jsonify({'user': user.to_dict()}), 200
