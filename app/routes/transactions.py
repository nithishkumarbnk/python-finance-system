from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models.transaction import Transaction
from ..models.user import User
from ..services.transaction_service import (
    get_transactions, create_transaction, update_transaction, delete_transaction
)
from ..utils.validators import validate_transaction_data
from ..utils.decorators import role_required

transactions_bp = Blueprint('transactions', __name__)


def _get_current_user():
    return User.query.get(int(get_jwt_identity()))


@transactions_bp.route('', methods=['GET'])
@jwt_required()
def list_transactions():
    user = _get_current_user()
    filters = {
        'type':       request.args.get('type'),
        'category':   request.args.get('category'),
        'date_from':  request.args.get('date_from'),
        'date_to':    request.args.get('date_to'),
        'min_amount': request.args.get('min_amount'),
        'max_amount': request.args.get('max_amount'),
    }
    target_user_id = user.id
    if user.role == 'admin' and request.args.get('user_id'):
        target_user_id = int(request.args.get('user_id'))

    try:
        page     = max(1, int(request.args.get('page', 1)))
        per_page = min(100, max(1, int(request.args.get('per_page', 20))))
    except ValueError:
        return jsonify({'error': 'page and per_page must be integers.'}), 400

    result = get_transactions(target_user_id, filters, page, per_page)
    return jsonify(result), 200


@transactions_bp.route('', methods=['POST'])
@jwt_required()
@role_required('admin', 'analyst')
def create():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Request body must be JSON.'}), 400

    is_valid, errors = validate_transaction_data(data)
    if not is_valid:
        return jsonify({'error': 'Validation failed.', 'details': errors}), 422

    txn = create_transaction(_get_current_user().id, data)
    return jsonify({'message': 'Transaction created.', 'transaction': txn.to_dict()}), 201


@transactions_bp.route('/<int:txn_id>', methods=['GET'])
@jwt_required()
def get_one(txn_id):
    user = _get_current_user()
    txn = Transaction.query.get_or_404(txn_id, description='Transaction not found.')
    if user.role != 'admin' and txn.user_id != user.id:
        return jsonify({'error': 'Access denied.'}), 403
    return jsonify({'transaction': txn.to_dict()}), 200


@transactions_bp.route('/<int:txn_id>', methods=['PUT'])
@jwt_required()
@role_required('admin', 'analyst')
def update(txn_id):
    user = _get_current_user()
    txn = Transaction.query.get_or_404(txn_id, description='Transaction not found.')
    if user.role != 'admin' and txn.user_id != user.id:
        return jsonify({'error': 'Access denied.'}), 403

    data = request.get_json()
    if not data:
        return jsonify({'error': 'Request body must be JSON.'}), 400

    is_valid, errors = validate_transaction_data(data, partial=True)
    if not is_valid:
        return jsonify({'error': 'Validation failed.', 'details': errors}), 422

    txn = update_transaction(txn, data)
    return jsonify({'message': 'Transaction updated.', 'transaction': txn.to_dict()}), 200


@transactions_bp.route('/<int:txn_id>', methods=['DELETE'])
@jwt_required()
@role_required('admin')
def delete(txn_id):
    txn = Transaction.query.get_or_404(txn_id, description='Transaction not found.')
    delete_transaction(txn)
    return jsonify({'message': f'Transaction {txn_id} deleted.'}), 200
