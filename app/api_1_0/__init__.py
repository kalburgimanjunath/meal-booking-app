from flask import Blueprint
from flask_restplus import Api, Resource


api_bp = Blueprint('api', __name__)
api = Api(api_bp)

from .auth import Login, Register, RegisterBusiness  # noqa
from .meals import MealResource, MealsResource  # noqa

api.add_resource(Register, '/auth/signup')
api.add_resource(RegisterBusiness, '/auth/business/signup')
api.add_resource(Login, '/auth/login')


api.add_resource(MealsResource, '/meals')
api.add_resource(MealResource, '/meals/<int:mealId>')
