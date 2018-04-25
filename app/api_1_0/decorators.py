from functools import wraps
from flask import g, request
from ..models import User


def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not getattr(func, 'authenticated', True):
            return func(*args, **kwargs)

        access_token = request.headers.get('Authorization')
        if not access_token or len(access_token) == 0:
            return {
                'message': 'No Bearer token in Authorisation header'
            }, 401

        token = access_token.split('Bearer ')[1]
        user = User.verify_jwt_token(token)
        if not user:
            return {
                'message': 'Authorisation failed'
            }, 401
        g.current_user = user
        g.token_used = True
        return func(*args, **kwargs)
        # restful.abort(401)
    return wrapper
