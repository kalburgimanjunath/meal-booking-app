from flask import Blueprint
from flask_restplus import Api
from ..models import User, MealOption

# Add some mock data for api testing
# create a test user
test_user = User(name='test', email='test@test.com')
test_user.password = 'test'
test_user.save()

# create a test admin user
admin_user = User('admin', email='admin@admin.com')
admin_user.password = 'admin'
admin_user.is_admin = True
admin_user.save()

# # create a test meal
# meal = MealOption('lorem meal', 10000, description='lorem ipsum desc')
# meal.save()

# meal = MealOption('Beef with rice', 1500, description='lorem desc ipsum')
# meal.save()

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
api.add_resource(MealResource, '/meals/<int:mealId>')

api.add_resource(MenuResource, '/menu')
api.add_resource(MenusResource, '/menus')

api.add_resource(OrderResource, '/orders/<int:orderId>')
api.add_resource(OrdersResource, '/orders')
