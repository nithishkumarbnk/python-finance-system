from .. import db
from datetime import datetime, timezone

class Transaction(db.Model):
    __tablename__ = 'transactions'

    id         = db.Column(db.Integer, primary_key=True)
    amount     = db.Column(db.Float,      nullable=False)
    type       = db.Column(db.String(10), nullable=False)
    category   = db.Column(db.String(80), nullable=False)
    date       = db.Column(db.Date,       nullable=False)
    notes      = db.Column(db.String(500))
    user_id    = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc),
                           onupdate=lambda: datetime.now(timezone.utc))

    TYPES = ['income', 'expense']
    CATEGORIES = [
        'salary', 'freelance', 'investment', 'gift', 'other_income',
        'rent', 'groceries', 'transport', 'utilities', 'healthcare',
        'entertainment', 'education', 'shopping', 'food', 'other_expense'
    ]

    def to_dict(self):
        return {
            'id':         self.id,
            'amount':     self.amount,
            'type':       self.type,
            'category':   self.category,
            'date':       self.date.isoformat(),
            'notes':      self.notes,
            'user_id':    self.user_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    def __repr__(self):
        return f'<Transaction {self.type} {self.amount} ({self.category})>'
