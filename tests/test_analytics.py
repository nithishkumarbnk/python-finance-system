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
                'username': 'analyst2', 'email': 'b@b.com', 'password': 'pass123'
            })
            from app.models.user import User
            u = User.query.filter_by(username='analyst2').first()
            u.role = 'analyst'
            db.session.commit()
            res = client.post('/api/auth/login', json={
                'username': 'analyst2', 'password': 'pass123'
            })
            token = res.get_json()['access_token']
            client.environ_base['HTTP_AUTHORIZATION'] = f'Bearer {token}'
            yield client
            db.drop_all()


@pytest.fixture
def viewer_client():
    app = create_app(TestConfig)
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            client.post('/api/auth/register', json={
                'username': 'viewer1', 'email': 'v@v.com', 'password': 'pass123'
            })
            res = client.post('/api/auth/login', json={
                'username': 'viewer1', 'password': 'pass123'
            })
            token = res.get_json()['access_token']
            client.environ_base['HTTP_AUTHORIZATION'] = f'Bearer {token}'
            yield client
            db.drop_all()


def test_summary_empty(auth_client):
    res = auth_client.get('/api/analytics/summary')
    assert res.status_code == 200
    data = res.get_json()
    assert data['total_income'] == 0.0
    assert data['total_expenses'] == 0.0
    assert data['balance'] == 0.0


def test_summary_with_data(auth_client):
    auth_client.post('/api/transactions', json={
        'amount': 10000, 'type': 'income', 'category': 'salary', 'date': '2026-04-01'
    })
    auth_client.post('/api/transactions', json={
        'amount': 3000, 'type': 'expense', 'category': 'rent', 'date': '2026-04-02'
    })
    res = auth_client.get('/api/analytics/summary')
    data = res.get_json()
    assert data['total_income']   == 10000.0
    assert data['total_expenses'] == 3000.0
    assert data['balance']        == 7000.0


def test_monthly_totals(auth_client):
    auth_client.post('/api/transactions', json={
        'amount': 5000, 'type': 'income', 'category': 'salary', 'date': '2026-04-01'
    })
    res = auth_client.get('/api/analytics/monthly?year=2026')
    assert res.status_code == 200
    assert 'monthly_totals' in res.get_json()


def test_category_breakdown(auth_client):
    auth_client.post('/api/transactions', json={
        'amount': 2000, 'type': 'expense', 'category': 'groceries', 'date': '2026-04-01'
    })
    res = auth_client.get('/api/analytics/categories')
    assert res.status_code == 200
    assert 'breakdown' in res.get_json()


def test_viewer_cannot_access_categories(viewer_client):
    res = viewer_client.get('/api/analytics/categories')
    assert res.status_code == 403
