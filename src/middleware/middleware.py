from functools import wraps
from flask import session, jsonify


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(session)
        if 'username' in session:
            return func(*args, **kwargs)
        else:
            return jsonify({'message': 'Unauthorized'}), 401

    return wrapper
