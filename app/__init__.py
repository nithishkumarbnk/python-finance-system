from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from .config import Config

db = SQLAlchemy()
jwt = JWTManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    jwt.init_app(app)

    from .routes.root import root_bp
    from .routes.auth import auth_bp
    from .routes.transactions import transactions_bp
    from .routes.analytics import analytics_bp
    from .routes.users import users_bp

    app.register_blueprint(root_bp)
    app.register_blueprint(auth_bp,         url_prefix='/api/auth')
    app.register_blueprint(transactions_bp, url_prefix='/api/transactions')
    app.register_blueprint(analytics_bp,    url_prefix='/api/analytics')
    app.register_blueprint(users_bp,        url_prefix='/api/users')

    with app.app_context():
        db.create_all()
        from .utils.seed import seed_data
        seed_data()

    return app
