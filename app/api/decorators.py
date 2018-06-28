"""
Module contains decorators for protecting routes
"""
from functools import wraps
from flask_restplus import abort
from flask import g, request
from ..models import User


def authenticate(func):
    """
    authenticate. protects a route to only authenticated users
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'Authorization' in request.headers:
            access_token = request.headers.get('Authorization')
            if access_token.strip(' '):
                user = User.verify_jwt_token(access_token)
                if user:
                    g.current_user = user
                    return func(*args, **kwargs)
                abort(code=401, message='Authorization failed try again')
        abort(code=401, message='No Bearer token in Authorisation header')
    return wrapper


def admin_required(func):
    """
    admin_required. protects a route to only adminstrators or caterers
    """
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not g.current_user.is_administrator():
            abort(code=403, message='403 forbidden access is denied')
        return func(*args, **kwargs)
    return decorated_function
