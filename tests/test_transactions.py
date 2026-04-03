import pytest
from app import create_app, db
from app.config import TestConfig


@pytest.fixture
def auth_client():
    app = create_app(TestConfig)
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            client.post('/api/auth/register', json={
                'username': 'analyst1', 'email': 'a@a.com', 'password': 'pass123'
            })
            from app.models.user import User
            u = User.query.filter_by(username='analyst1').first()
            u.role = 'analyst'
            db.session.commit()
            res = client.post('/api/auth/login', json={
                'username': 'analyst1', 'password': 'pass123'
            })
            token = res.get_json()['access_token']
            client.environ_base['HTTP_AUTHORIZATION'] = f'Bearer {token}'
            yield client
            db.drop_all()


def test_create_transaction(auth_client):
    res = auth_client.post('/api/transactions', json={
        'amount': 5000, 'type': 'income', 'category': 'salary', 'date': '2026-04-01'
    })
    assert res.status_code == 201
    assert res.get_json()['transaction']['amount'] == 5000.0


def test_invalid_transaction_type(auth_client):
    res = auth_client.post('/api/transactions', json={
        'amount': 100, 'type': 'gift', 'category': 'misc', 'date': '2026-04-01'
    })
    assert res.status_code == 422


def test_invalid_negative_amount(auth_client):
    res = auth_client.post('/api/transactions', json={
        'amount': -500, 'type': 'income', 'category': 'salary', 'date': '2026-04-01'
    })
    assert res.status_code == 422


def test_list_transactions(auth_client):
    auth_client.post('/api/transactions', json={
        'amount': 1000, 'type': 'expense', 'category': 'food', 'date': '2026-04-02'
    })
    res = auth_client.get('/api/transactions')
    assert res.status_code == 200
    assert 'pagination' in res.get_json()


def test_filter_by_type(auth_client):
    auth_client.post('/api/transactions', json={
        'amount': 2000, 'type': 'income', 'category': 'freelance', 'date': '2026-04-03'
    })
    res = auth_client.get('/api/transactions?type=income')
    assert res.status_code == 200
    txns = res.get_json()['transactions']
    assert all(t['type'] == 'income' for t in txns)


def test_update_transaction(auth_client):
    create_res = auth_client.post('/api/transactions', json={
        'amount': 500, 'type': 'expense', 'category': 'food', 'date': '2026-04-01'
    })
    txn_id = create_res.get_json()['transaction']['id']
    res = auth_client.put(f'/api/transactions/{txn_id}', json={'amount': 750})
    assert res.status_code == 200
    assert res.get_json()['transaction']['amount'] == 750.0


def test_delete_requires_admin(auth_client):
    create_res = auth_client.post('/api/transactions', json={
        'amount': 100, 'type': 'expense', 'category': 'food', 'date': '2026-04-01'
    })
    txn_id = create_res.get_json()['transaction']['id']
    res = auth_client.delete(f'/api/transactions/{txn_id}')
    assert res.status_code == 403
