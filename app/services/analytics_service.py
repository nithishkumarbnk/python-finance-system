from ..models.transaction import Transaction
from sqlalchemy import func
from .. import db
from datetime import date


def get_summary(user_id):
    rows = db.session.query(
        Transaction.type,
        func.sum(Transaction.amount).label('total')
    ).filter_by(user_id=user_id).group_by(Transaction.type).all()

    totals   = {r.type: float(r.total) for r in rows}
    income   = totals.get('income',  0.0)
    expenses = totals.get('expense', 0.0)

    return {
        'total_income':   round(income,           2),
        'total_expenses': round(expenses,          2),
        'balance':        round(income - expenses, 2)
    }


def get_category_breakdown(user_id, txn_type=None):
    query = db.session.query(
        Transaction.category,
        Transaction.type,
        func.sum(Transaction.amount).label('total'),
        func.count(Transaction.id).label('count')
    ).filter_by(user_id=user_id)

    if txn_type:
        query = query.filter_by(type=txn_type)

    rows = query.group_by(Transaction.category, Transaction.type).all()
    return [
        {'category': r.category, 'type': r.type,
         'total': round(float(r.total), 2), 'count': r.count}
        for r in rows
    ]


def get_monthly_totals(user_id, year=None):
    query = Transaction.query.filter_by(user_id=user_id)
    if year:
        query = query.filter(
            Transaction.date >= date(year, 1, 1),
            Transaction.date <= date(year, 12, 31)
        )

    monthly = {}
    for t in query.all():
        key = f"{t.date.year}-{t.date.month:02d}"
        if key not in monthly:
            monthly[key] = {'month': key, 'income': 0.0, 'expense': 0.0}
        monthly[key][t.type] = round(monthly[key][t.type] + t.amount, 2)

    result = sorted(monthly.values(), key=lambda x: x['month'])
    for row in result:
        row['balance'] = round(row['income'] - row['expense'], 2)
    return result


def get_recent_activity(user_id, limit=10):
    txns = (Transaction.query
            .filter_by(user_id=user_id)
            .order_by(Transaction.date.desc(), Transaction.created_at.desc())
            .limit(limit).all())
    return [t.to_dict() for t in txns]
