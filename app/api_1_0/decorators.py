from functools import wraps
from flask import g, request
from ..models import User


def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'Authorization' in request.headers:
            access_token = request.headers.get('Authorization')
            if access_token and len(access_token) != 0:
                token = access_token.split(' ')[1]
                user = User.verify_jwt_token(token)
                if user:
                    g.current_user = user
                    return func(*args,**kwargs)
                else:
                    return {
                        'error': 'Authorization failed try again'
                    }, 401
        return {
                'error': 'No Bearer token in Authorisation header'
            }, 401
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
