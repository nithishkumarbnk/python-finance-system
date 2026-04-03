import pytest
from app import create_app, db
from app.config import TestConfig

@pytest.fixture
def client():
    app = create_app(TestConfig)
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

def test_register(client):
    res = client.post('/api/auth/register', json={
        'username': 'testuser', 'email': 'test@example.com', 'password': 'pass123'
    })
    assert res.status_code == 201
    assert 'access_token' in res.get_json()

def test_login(client):
    client.post('/api/auth/register', json={
        'username': 'testuser', 'email': 'test@example.com', 'password': 'pass123'
    })
    res = client.post('/api/auth/login', json={'username': 'testuser', 'password': 'pass123'})
    assert res.status_code == 200
    assert 'access_token' in res.get_json()

def test_login_invalid_credentials(client):
    res = client.post('/api/auth/login', json={'username': 'nobody', 'password': 'wrong'})
    assert res.status_code == 401

def test_register_duplicate_username(client):
    client.post('/api/auth/register', json={'username': 'dup', 'email': 'a@a.com', 'password': 'pass123'})
    res = client.post('/api/auth/register', json={'username': 'dup', 'email': 'b@b.com', 'password': 'pass123'})
    assert res.status_code == 409

def test_register_invalid_email(client):
    res = client.post('/api/auth/register', json={'username': 'newuser', 'email': 'notanemail', 'password': 'pass123'})
    assert res.status_code == 422
