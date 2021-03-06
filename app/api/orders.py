"""
Module contains Api resources for exposing orders
"""
import datetime
from flask import g, current_app
from flask_restplus import Resource, fields, abort
from ..models import Order, Meal, Menu
from .decorators import authenticate, admin_required
from . import api
from .common import validate_meals_list
from .parsers import orders_parser, edit_orders_parser

ORDER_MODEL = api.model('order', {
    'meals': fields.List(fields.Integer),
    'orderCount': fields.Integer(min=1),
    'menuId': fields.Integer()
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
            abort(
                code=400, message='Order with such id {} doesnot exist'.format(order_id)
            )

        return {
            'order': order.to_dict()
        }, 200

    @authenticate
    @api.expect(ORDER_MODEL, validate=True)
    @api.header('Authorization', type=str, description='Authentication token')
    def put(self, order_id):
        """
        Allows a customer to modify an order
        """
        user = g.current_user
        order = Order.query.filter_by(
            customer=user).filter_by(id=order_id).first()
        if not order:
            abort(
                code=400, message='Order with such id {} doesnot exist'.format(order_id))
        if order.is_expired():
            abort(code=400, message='Order expired and cannot be modify it')
        args = edit_orders_parser.parse_args()
        meals = args['meals']
        order_count = args['orderCount']
        validate_meals_list(meals)
        expires_at = datetime.datetime.now(
        ) + datetime.timedelta(minutes=current_app.config['ORDER_EXPIRES_IN'])
        order.expires_at = expires_at
        order.meals.clear()  # remove all meal items from the array
        total_cost = order.add_meals(meals)
        order.total_cost = total_cost * order_count
        order.order_count = order_count
        order.save()
        return {
            'order': order.to_dict()
        }, 200


class CustomerOrderResource(Resource):
    """
    Exposes orders as resources
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
    @api.expect(ORDER_MODEL, validate=True)
    @api.header('Authorization', type=str, description='Authentication token')
    def post(self):
        """
        Allows a user to place an order to catering for food.
        """
        customer = g.current_user

        args = orders_parser.parse_args()
        menu = Menu.query.filter_by(id=args['menuId']).first()
        meals = args['meals']
        order_count = args.get('orderCount', 1)
        validate_meals_list(meals)
        order_meals = []
        total_cost = 0
        for meal_id in meals:
            meal = Meal.query.get(meal_id)
            if meal:
                total_cost += meal.price
                order_meals.append(meal)
        total_cost = total_cost * order_count
        order = Order(total_cost=total_cost, meals=order_meals,
                      customer=customer, catering=menu.catering, menu=menu,
                      order_count=order_count)
        order.save()
        return {
            'order': order.to_dict()
        }, 201


class MyOrderResource(Resource):
    """
    Resource exposes a customer's orders as an endpoint.
    """
    @authenticate
    @api.header('Authorization', type=str, description='Authentication token')
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
