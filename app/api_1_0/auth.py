from flask_restplus import Resource, reqparse, fields
from ..models import User, Catering
from .decorators import authenticate
from .import api
from .common import str_type

login_modal = api.model('login', {'email': fields.String('Email.'),
                                  'password': fields.String('Password')})

register_modal = api.model('register',
                           {'name': fields.String('Your Name'),
                            'email': fields.String('Your Email'),
                               'password': fields.String('Your Password')
                            })


def email_type(value):
    if not isinstance(value, str):
        raise ValueError("Email must be a string")
    if not value or len(value.strip(' ')) == 0:
        raise ValueError("Email field is required")
    user = User.get_by_email(value)
    if user is not None:
        raise ValueError("Email already in use")
    return value


class Register(Resource):
    @api.expect(register_modal)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str_type, required=True,
                            help='Name field is required')
        parser.add_argument('email', type=email_type, required=True)
        parser.add_argument('password', type=str_type, required=True,
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
            'user': user.to_dict(),
            'token': user.generate_jwt_token()
        }, 201


signup_business = api.model('business_signup', {
    'businessAddress': fields.String('Your business Address'),
    'businessName': fields.String('Your business name'),
    'email': fields.String('Your email'),
    'name': fields.String('Your Name'),
    'password': fields.String('Your password')
})


class RegisterBusiness(Resource):
    @api.expect(signup_business)
    def post(self):
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
        password = args['password']

        # create user and return the created user
        user = User(name=args['name'], email=args['email'])
        user.password = password
        user.is_admin = True
        user.save()

        catering = Catering(name=args['businessName'],
                            address=args['businessAddress'])
        catering.admin = user
        catering.save()

        return {
            'user': user.to_dict(),
            'token': user.generate_jwt_token(),
            'business': catering.to_dict()
        }, 201


class Login(Resource):
    @api.expect(login_modal)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str_type, required=True,
                            help='Email field is required')
        parser.add_argument('password', type=str_type, required=True,
                            help='Password field is required')
        args = parser.parse_args()

        email = args['email']
        password = args['password']

        user = User.get_by_email(email)
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
