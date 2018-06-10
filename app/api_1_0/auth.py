"""
Module contains API resources for authentication
"""
from flask_restplus import Resource, reqparse, fields
from ..models import User, Catering, Role
from .import api
from .common import str_type, email_type


LOGIN_MODAL = api.model('login', {
    'email': fields.String('Email.'),
    'password': fields.String('Password')
})

REGISTER_MODAL = api.model('register', {
    'name': fields.String('Your Name'),
    'email': fields.String('Your Email'),
    'password': fields.String('Your Password')
})


class Register(Resource):
    """
    Register. resource for registering a user
    """
    @api.expect(REGISTER_MODAL)
    def post(self):
        """
        Signs up a new customer
        """
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str_type, required=True,
                            help='Name field is required')
        parser.add_argument('email', type=email_type, required=True)
        parser.add_argument('password', type=str_type, required=True,
                            help='Password field is required')
        args = parser.parse_args()

        user = User(name=args['name'], email=args['email'],
                    password=args['password'])
        user.save()
        return user.to_dict(), 201


SIGNUP_BUSINESS = api.model('business_signup', {
    'businessAddress': fields.String('Your business Address'),
    'businessName': fields.String('Your business name'),
    'email': fields.String('Your email'),
    'name': fields.String('Your Name'),
    'password': fields.String('Your password')
})


class RegisterBusiness(Resource):
    """
    RegisterBusiness. resource for registering a business
    """
    @api.expect(SIGNUP_BUSINESS)
    def post(self):
        """
        Signs up a new business
        """
        parser = reqparse.RequestParser()
        parser.add_argument('businessAddress', type=str_type,
                            help='Business Address field is required')
        parser.add_argument('businessName', type=str_type,
                            help='Business Name field is required')
        parser.add_argument('name', type=str_type, required=True,
                            help='Name field is required')
        parser.add_argument('email', type=email_type, required=True)
        parser.add_argument('password', type=str_type, required=True,
                            help='Password field is required')
        args = parser.parse_args()
        role = Role.query.filter_by(name='Admin').first()
        user = User(name=args['name'], email=args['email'],
                    password=args['password'], role=role)
        user.save()
        catering = Catering(name=args['businessName'],
                            address=args['businessAddress'], admin=user)
        catering.save()
        return {
            'user': user.to_dict(),
            'business': catering.to_dict()
        }, 201


class Login(Resource):
    """
    Class Login exposes login functionality in form of a resource
    """
    @api.expect(LOGIN_MODAL)
    def post(self):
        """
         Handles post requests for logging in a user
        """
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str_type, required=True,
                            help='Email field is required')
        parser.add_argument('password', type=str_type, required=True,
                            help='Password field is required')
        args = parser.parse_args()
        user = User.query.filter_by(email=args['email']).first()
        if user is not None and user.verify_password(args['password']):
            token = user.generate_jwt_token()
            return {
                'token': token
            }, 200
        return {
            'errors': {
                'form': 'Wrong username or password'
            }
        }, 401
