from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from ..models.user import User
from .. import db


def role_required(*allowed_roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            # Identity is stored as string, cast to int for DB lookup
            user = db.session.get(User, int(get_jwt_identity()))

            if not user or not user.is_active:
                return jsonify({"error": "User not found or inactive."}), 403
            if user.role not in allowed_roles:
                return (
                    jsonify(
                        {
                            "error": f'Access denied. Required role(s): {", ".join(allowed_roles)}.'
                        }
                    ),
                    403,
                )
            return fn(*args, **kwargs)

        return wrapper

    return decorator
