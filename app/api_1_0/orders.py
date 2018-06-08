import datetime
from flask import g, current_app, request
from flask_restplus import Resource, reqparse, fields
from ..models import Order, Meal, Menu
from .decorators import authenticate, admin_required
from . import api
from .common import validate_meals_list
from .. import db

ORDER_MODEL = api.model('order', {
    'meals': fields.String('[]'),
    'cateringId': fields.Integer('cateringId'),
    'menuId': fields.Integer('menuId')
})


class OrderResource(Resource):
    """
     Exposes order resource
    """
    @authenticate
    @api.header('Authorization', type=str, description='Authentication token')
    def get(self, order_id):
        """
        Allows a customer to get his order details
        """
        user = g.current_user
        order = Order.query.filter_by(
            customer=user).filter_by(id=order_id).first()
        if not order:
            return {
                'error': 'Order with such id {} doesnot exist'.format(order_id)
            }, 400

        return {
            'order': order.to_dict()
        }, 200

    @authenticate
    @api.expect(ORDER_MODEL)
    @api.header('Authorization', type=str, description='Authentication token')
    def put(self, order_id):
        """
        Allows a customer to modify an order
        """
        user = g.current_user
        order = Order.query.filter_by(
            customer=user).filter_by(id=order_id).first()
        if not order:
            return {
                'error': 'Order with such id {} doesnot exist'.format(order_id)
            }, 400
        # check if the order has not yet expired
        time_diff = datetime.timedelta(
            minutes=current_app.config['ORDER_EXPIRES_IN'])
        if order.expires_at and datetime.datetime.now() - order.expires_at > time_diff:  # noqa
            return {
                'error': 'Order expired and cannot be modify it'
            }, 400

        meals = request.json.get('meals', '')
        order_count = request.json.get('orderCount', 1)
        val = validate_meals_list(meals)
        if val:
            return val, 400

        expires_at = datetime.datetime.now(
        ) + datetime.timedelta(minutes=current_app.config['ORDER_EXPIRES_IN'])
        order.expires_at = expires_at
        total_cost = 0
        order.meals.clear()  # remove all items from the array
        for meal_id in meals:
            meal = Meal.query.get(int(meal_id))
            if meal:
                total_cost += meal.price
                order.meals.append(meal)

        order.total_cost = total_cost * int(order_count)
        order.order_count = int(order_count)
        db.session.add(order)
        db.session.commit()
        return {
            'order': order.to_dict()
        }, 200


def type_menu_id(value):
    """
    type_menu_id defines a type for validating memu id
    """
    if not isinstance(value, int):
        raise ValueError("Field value must be an integer")
    menu = Menu.query.get(value)
    if not menu:
        raise ValueError("Menu with id {} does not exist".format(value))
    return value


class OrdersResource(Resource):
    """
    Exposes an orders as resources
    """
    @authenticate
    @admin_required
    @api.header('Authorization', type=str, description='Authentication token')
    def get(self):
        """
        Allows a business get orders placed to their catering
        """
        user = g.current_user
        return {
            'orders': [order.to_dict() for order in user.catering.orders]
        }

    @authenticate
    @api.expect(ORDER_MODEL)
    @api.header('Authorization', type=str, description='Authentication token')
    def post(self):
        """
        Allows a user to place an order to catering for food.
        """
        customer = g.current_user
        meals = request.json.get('meals', '')
        order_count = request.json.get('orderCount', 1)
        parser = reqparse.RequestParser()
        parser.add_argument('menuId', type=type_menu_id,
                            help='menu id is required', required=True)
        args = parser.parse_args()
        menu = Menu.query.filter_by(id=args['menuId']).first()
        print(menu.id)

        val = validate_meals_list(meals)
        if val:
            return val, 400

        order_meals = []
        total_cost = 0

        for meal_id in meals:
            meal = Meal.query.get(meal_id)
            if meal:
                total_cost += meal.price
                order_meals.append(meal)
        total_cost = total_cost * int(order_count)
        order = Order(total_cost=total_cost, meals=order_meals,
                      customer=customer, catering=menu.catering, menu=menu,
                      order_count=int(order_count))
        db.session.add(order)
        db.session.commit()
        return {
            'order': order.to_dict()
        }, 201


class MyOrderResource(Resource):
    """
    Resource exposes a customer's orders
    """
    @authenticate
    def get(self):
        """
        Allows a customer to get thier previous orders
        """
        customer = g.current_user
        orders = Order.query.filter_by(customer=customer).order_by(
            Order.created_at.desc()).all()
        return {
            'orders': [order.to_dict() for order in orders]
        }
