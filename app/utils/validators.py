from datetime import datetime

def validate_transaction_data(data, partial=False):
    errors = {}

    if not partial or 'amount' in data:
        try:
            val = float(data.get('amount'))
            if val <= 0:
                errors['amount'] = 'Amount must be a positive number.'
        except (TypeError, ValueError):
            errors['amount'] = 'Amount must be a valid positive number.'

    if not partial or 'type' in data:
        if data.get('type') not in ['income', 'expense']:
            errors['type'] = "Type must be 'income' or 'expense'."

    if not partial or 'category' in data:
        cat = str(data.get('category', '')).strip()
        if not cat:
            errors['category'] = 'Category is required.'
        elif len(cat) > 80:
            errors['category'] = 'Category must be at most 80 characters.'

    if not partial or 'date' in data:
        try:
            datetime.strptime(str(data.get('date', '')), '%Y-%m-%d')
        except ValueError:
            errors['date'] = 'Date must be in YYYY-MM-DD format.'

    if data.get('notes') and len(str(data['notes'])) > 500:
        errors['notes'] = 'Notes must be at most 500 characters.'

    return len(errors) == 0, errors


def validate_user_data(data, partial=False):
    errors = {}

    if not partial or 'username' in data:
        u = str(data.get('username', '')).strip()
        if not (3 <= len(u) <= 80):
            errors['username'] = 'Username must be between 3 and 80 characters.'

    if not partial or 'email' in data:
        e = str(data.get('email', '')).strip()
        if '@' not in e or '.' not in e.split('@')[-1]:
            errors['email'] = 'A valid email address is required.'

    if not partial or 'password' in data:
        p = data.get('password', '')
        if len(p) < 6:
            errors['password'] = 'Password must be at least 6 characters.'

    if data.get('role') and data['role'] not in ['viewer', 'analyst', 'admin']:
        errors['role'] = "Role must be 'viewer', 'analyst', or 'admin'."

    return len(errors) == 0, errors
