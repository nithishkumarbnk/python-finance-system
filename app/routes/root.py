from flask import Blueprint, jsonify

root_bp = Blueprint('root', __name__)

@root_bp.route('/', methods=['GET'])
def index():
    return jsonify({
        'name': 'Python Finance System API',
        'version': '1.0.0',
        'status': 'running',
        'author': 'Bhuvaneswaram Nithish Kumar',
        'endpoints': {
            'auth': {
                'POST /api/auth/register': 'Register a new user',
                'POST /api/auth/login':    'Login and get JWT token',
                'GET  /api/auth/me':       'Get current user profile'
            },
            'transactions': {
                'GET    /api/transactions':      'List transactions (filters + pagination)',
                'POST   /api/transactions':      'Create a transaction [analyst, admin]',
                'GET    /api/transactions/<id>': 'Get single transaction',
                'PUT    /api/transactions/<id>': 'Update transaction [analyst, admin]',
                'DELETE /api/transactions/<id>': 'Delete transaction [admin]'
            },
            'analytics': {
                'GET /api/analytics/summary':    'Income, expenses, balance [all]',
                'GET /api/analytics/categories': 'Category breakdown [analyst, admin]',
                'GET /api/analytics/monthly':    'Monthly totals [analyst, admin]',
                'GET /api/analytics/recent':     'Recent transactions [all]'
            },
            'users': {
                'GET   /api/users':              'List all users [admin]',
                'GET   /api/users/<id>':         'Get user [admin]',
                'PATCH /api/users/<id>/role':    'Update user role [admin]',
                'DELETE /api/users/<id>':        'Deactivate user [admin]'
            }
        },
        'seed_credentials': {
            'admin':   {'username': 'admin',   'password': 'admin123'},
            'analyst': {'username': 'analyst', 'password': 'analyst123'},
            'viewer':  {'username': 'viewer',  'password': 'viewer123'}
        },
        'docs': 'Send Authorization: Bearer <token> header for protected routes.'
    }), 200
