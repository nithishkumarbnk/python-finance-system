from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models.user import User
from .. import db

from ..services.analytics_service import (
    get_summary,
    get_category_breakdown,
    get_monthly_totals,
    get_recent_activity,
)
from ..utils.decorators import role_required

analytics_bp = Blueprint("analytics", __name__)


def _get_current_user():
    return db.session.get(User, int(get_jwt_identity()))


@analytics_bp.route("/summary", methods=["GET"])
@jwt_required()
def summary():
    return jsonify(get_summary(_get_current_user().id)), 200


@analytics_bp.route("/categories", methods=["GET"])
@jwt_required()
@role_required("admin", "analyst")
def categories():
    txn_type = request.args.get("type")
    if txn_type and txn_type not in ["income", "expense"]:
        return jsonify({"error": "Type must be 'income' or 'expense'."}), 400
    return (
        jsonify(
            {"breakdown": get_category_breakdown(_get_current_user().id, txn_type)}
        ),
        200,
    )


@analytics_bp.route("/monthly", methods=["GET"])
@jwt_required()
@role_required("admin", "analyst")
def monthly():
    year_str = request.args.get("year")
    year = None
    if year_str:
        try:
            year = int(year_str)
        except ValueError:
            return jsonify({"error": "year must be an integer."}), 400
    return (
        jsonify({"monthly_totals": get_monthly_totals(_get_current_user().id, year)}),
        200,
    )


@analytics_bp.route("/recent", methods=["GET"])
@jwt_required()
def recent():
    try:
        limit = min(50, max(1, int(request.args.get("limit", 10))))
    except ValueError:
        return jsonify({"error": "limit must be an integer."}), 400
    return (
        jsonify(
            {"recent_activity": get_recent_activity(_get_current_user().id, limit)}
        ),
        200,
    )
