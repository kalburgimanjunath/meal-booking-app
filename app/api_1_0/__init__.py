from flask import Blueprint
from flask_restplus import Api


api_bp = Blueprint('api', __name__)
api = Api(api_bp)

from .auth import Login, Register, RegisterBusiness  # noqa
from .meals import MealResource, MealsResource  # noqa
from .menus import MenuResource, MenusResource  # noqa
from .orders import OrderResource, OrdersResource  # noqa

api.add_resource(Register, '/auth/signup')
api.add_resource(RegisterBusiness, '/auth/business/signup')
api.add_resource(Login, '/auth/login')


api.add_resource(MealsResource, '/meals')
api.add_resource(MealResource, '/meals/<int:meal_id>')

api.add_resource(MenuResource, '/menu')
api.add_resource(MenusResource, '/menus')

api.add_resource(OrderResource, '/orders/<int:order_id>')
api.add_resource(OrdersResource, '/orders')
