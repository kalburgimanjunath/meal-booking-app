from flask_restful import Resource, reqparse, fields
from ..models import User, Catering
from .decorators import authenticate


user_fields = {
    'id': fields.Integer,
    'email': fields.String,
    'name': fields.String
}

auth_fields = {
    'token': fields.String,
    'user': user_fields
}


def email_type(value):
    if not value:
        raise ValueError("Email field is required")
    if not isinstance(value, str):
        raise ValueError("Email must be a string")
    user = User.get_by_email(value)
    if user is not None:
        raise ValueError("Email already in use")
    return value


class Register(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True,
                            help='Name field is required')
        parser.add_argument('email', type=email_type, required=True)
        parser.add_argument('password', type=str, required=True,
                            help='Password field is required')
        args = parser.parse_args()

        name = args['name']
        email = args['email']
        password = args['password']

        # create user and return the created user
        user = User(name=name, email=email)
        user.password = password
        user.save()
        return {
            'user': user.to_dict()
        }, 201


class RegisterBusiness(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('businessAddress', type=str,
                            help='Business Address field is required')
        parser.add_argument('businessName', type=str,
                            help='Business Name field is required')
        parser.add_argument('name', type=str, required=True,
                            help='Name field is required')
        parser.add_argument('email', type=email_type, required=True)
        parser.add_argument('password', type=str, required=True,
                            help='Password field is required')
        args = parser.parse_args()

        name = args['name']
        email = args['email']
        password = args['password']
        address = args['businessAddress']
        business_name = args['businessName']
        # create user and return the created user

        user = User(name=name, email=email)
        user.password = password
        user.is_admin = True
        user.save()

        catering = Catering(name=business_name, address=address)
        catering.admin = user
        catering.save()
        return {
            'user': user.to_dict(),
            'business': catering.to_dict()
        }, 201


class Login(Resource):
    method_decorators = [authenticate]

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True,
                            help='Username field is required')
        parser.add_argument('password', type=str, required=True,
                            help='Password field is required')
        args = parser.parse_args()

        username = args['username']
        password = args['password']

        user = User.get_by_email(username)
        if user is not None and user.verify_password(password):
            # login in user
            token = user.generate_jwt_token()
            return {
                'token': token,
                'user': user.to_dict()
            }, 200
        return {
            'message': {
                'form': 'Wrong username or password'
            }
        }, 401
