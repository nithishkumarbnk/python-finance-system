from ..models.user import User
from ..models.transaction import Transaction
from .. import db
from datetime import date

def seed_data():
    if User.query.count() > 0:
        return

    users_data = [
        {'username': 'admin',   'email': 'admin@finance.dev',   'password': 'admin123',   'role': 'admin'},
        {'username': 'analyst', 'email': 'analyst@finance.dev', 'password': 'analyst123', 'role': 'analyst'},
        {'username': 'viewer',  'email': 'viewer@finance.dev',  'password': 'viewer123',  'role': 'viewer'},
    ]
    created = []
    for u in users_data:
        user = User(username=u['username'], email=u['email'], role=u['role'])
        user.set_password(u['password'])
        db.session.add(user)
        created.append(user)
    db.session.flush()

    admin = created[0]
    txns = [
        {'amount': 85000.00, 'type': 'income',  'category': 'salary',        'date': date(2026,1,1),  'notes': 'January salary'},
        {'amount': 85000.00, 'type': 'income',  'category': 'salary',        'date': date(2026,2,1),  'notes': 'February salary'},
        {'amount': 85000.00, 'type': 'income',  'category': 'salary',        'date': date(2026,3,1),  'notes': 'March salary'},
        {'amount': 12000.00, 'type': 'income',  'category': 'freelance',     'date': date(2026,1,15), 'notes': 'Web dev project'},
        {'amount': 5500.00,  'type': 'income',  'category': 'investment',    'date': date(2026,2,20), 'notes': 'Stock dividends'},
        {'amount': 18000.00, 'type': 'expense', 'category': 'rent',          'date': date(2026,1,5),  'notes': 'Monthly rent'},
        {'amount': 18000.00, 'type': 'expense', 'category': 'rent',          'date': date(2026,2,5),  'notes': 'Monthly rent'},
        {'amount': 18000.00, 'type': 'expense', 'category': 'rent',          'date': date(2026,3,5),  'notes': 'Monthly rent'},
        {'amount': 4200.00,  'type': 'expense', 'category': 'groceries',     'date': date(2026,1,10), 'notes': 'Monthly groceries'},
        {'amount': 3800.00,  'type': 'expense', 'category': 'groceries',     'date': date(2026,2,12), 'notes': 'Monthly groceries'},
        {'amount': 1500.00,  'type': 'expense', 'category': 'transport',     'date': date(2026,1,20), 'notes': 'Petrol & auto'},
        {'amount': 2200.00,  'type': 'expense', 'category': 'utilities',     'date': date(2026,2,8),  'notes': 'Electricity & internet'},
        {'amount': 3500.00,  'type': 'expense', 'category': 'entertainment', 'date': date(2026,1,25), 'notes': 'Movies & dining'},
        {'amount': 8000.00,  'type': 'expense', 'category': 'education',     'date': date(2026,3,10), 'notes': 'Online courses'},
        {'amount': 6000.00,  'type': 'expense', 'category': 'shopping',      'date': date(2026,2,28), 'notes': 'Clothes & gadgets'},
    ]
    for t in txns:
        db.session.add(Transaction(**t, user_id=admin.id))
    db.session.commit()
    print('[Seed] Database seeded successfully.')
