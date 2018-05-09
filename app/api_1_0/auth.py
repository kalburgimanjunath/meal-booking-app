from flask_restplus import Resource, reqparse, fields
from ..models import User, Catering, Role
from .import api
from .common import str_type, validate_email_type
from .. import db
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
    is_valid = validate_email_type(value)
    if not is_valid:
        raise ValueError('Email is not valid')
    user = User.query.filter_by(email=value).first()
    if user is not None:
        raise ValueError("Email already in use")
    return value


class Register(Resource):
    @api.expect(register_modal)
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

        name = args['name']
        email = args['email']
        password = args['password']

        # create user and return the created user
        user = User(name=name, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return user.to_dict(), 201


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
        password = args['password']
        role = Role.query.filter_by(name='Admin').first()
        # create user and return the created user
        user = User(name=args['name'], email=args['email'],
                    password=password, role=role)
        db.session.add(user)
        db.session.commit()

        catering = Catering(name=args['businessName'],
                            address=args['businessAddress'])
        catering.admin = user
        db.session.add(catering)
        db.session.commit()

        return {
            'user': user.to_dict(),
            'business': catering.to_dict()
        }, 201


class Login(Resource):
    """
    Class Login exposes login functionality in form of a resource
    """
    @api.expect(login_modal)
    def post(self):
        """
         Post handles post requests for logging in a user
        """
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str_type, required=True,
                            help='Email field is required')
        parser.add_argument('password', type=str_type, required=True,
                            help='Password field is required')
        args = parser.parse_args()

        email = args['email']
        password = args['password']

        user = User.query.filter_by(email=email).first()
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
