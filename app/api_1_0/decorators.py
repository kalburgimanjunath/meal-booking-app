from functools import wraps
from flask import g, request
from ..models import User


def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not getattr(func, 'authenticated', True):
            return func(*args, **kwargs)
        if 'Authorization' not in request.headers:
            return {
                'error': 'No Bearer token in Authorisation header'
            }, 401

        access_token = request.headers.get('Authorization')
        if not access_token or len(access_token) == 0:
            return {
                'error': 'No Bearer token in Authorisation header'
            }, 401

        token = access_token.split('Bearer ')[1]
        user = User.verify_jwt_token(token)
        if not user:
            return {
                'error': 'Authorisation failed'
            }, 401
        g.current_user = user
        g.token_used = True
        return func(*args, **kwargs)
        # restful.abort(401)
    return wrapper


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # TODO: change this in upcoming challenges
        if not g.current_user.is_admin:
            return {
                'error': '403 forbidden access is denied'
            }, 403
        return f(*args, **kwargs)
    return decorated_function
