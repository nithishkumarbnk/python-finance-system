from ..models.transaction import Transaction
from .. import db
from datetime import datetime


def get_transactions(user_id, filters=None, page=1, per_page=20):
    query = Transaction.query.filter_by(user_id=user_id)

    if filters:
        if filters.get('type'):
            query = query.filter_by(type=filters['type'])
        if filters.get('category'):
            query = query.filter_by(category=filters['category'])
        if filters.get('date_from'):
            query = query.filter(Transaction.date >= filters['date_from'])
        if filters.get('date_to'):
            query = query.filter(Transaction.date <= filters['date_to'])
        if filters.get('min_amount'):
            query = query.filter(Transaction.amount >= float(filters['min_amount']))
        if filters.get('max_amount'):
            query = query.filter(Transaction.amount <= float(filters['max_amount']))

    query = query.order_by(Transaction.date.desc())
    paginated = query.paginate(page=page, per_page=per_page, error_out=False)

    return {
        'transactions': [t.to_dict() for t in paginated.items],
        'pagination': {
            'page':     paginated.page,
            'per_page': paginated.per_page,
            'total':    paginated.total,
            'pages':    paginated.pages,
            'has_next': paginated.has_next,
            'has_prev': paginated.has_prev
        }
    }


def create_transaction(user_id, data):
    txn = Transaction(
        amount   = float(data['amount']),
        type     = data['type'],
        category = data['category'].strip(),
        date     = datetime.strptime(data['date'], '%Y-%m-%d').date(),
        notes    = data.get('notes', '').strip() or None,
        user_id  = user_id
    )
    db.session.add(txn)
    db.session.commit()
    return txn


def update_transaction(txn, data):
    if 'amount'   in data: txn.amount   = float(data['amount'])
    if 'type'     in data: txn.type     = data['type']
    if 'category' in data: txn.category = data['category'].strip()
    if 'date'     in data: txn.date     = datetime.strptime(data['date'], '%Y-%m-%d').date()
    if 'notes'    in data: txn.notes    = data.get('notes', '').strip() or None
    db.session.commit()
    return txn


def delete_transaction(txn):
    db.session.delete(txn)
    db.session.commit()
