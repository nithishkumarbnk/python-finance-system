import os
from datetime import timedelta

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'finance-system-secret-key-2026-xK9mP2nQ')
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        f'sqlite:///{os.path.join(BASE_DIR, "..", "finance.db")}'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'jwt-finance-system-secret-2026-xK9mP2nQ')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    # Suppress the HMAC key length warning entirely
    JWT_ALGORITHM = 'HS256'


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SECRET_KEY = 'test-secret-key-for-finance-system-2026'
    JWT_SECRET_KEY = 'test-jwt-secret-key-for-finance-system-2026'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=5)
