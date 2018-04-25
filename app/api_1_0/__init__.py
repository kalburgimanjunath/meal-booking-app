from flask import Blueprint
from flask_restplus import Api, Resource

from .auth import Login, Register, RegisterBusiness

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

api.add_resource(Register, '/auth/signup')
api.add_resource(RegisterBusiness, '/auth/business/signup')
api.add_resource(Login, '/auth/login')
