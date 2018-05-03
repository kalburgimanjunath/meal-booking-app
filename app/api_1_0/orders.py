from flask import g, current_app
from flask_restplus import Resource, reqparse, fields
from ..models import Order, data, MealOption
from .decorators import authenticate, admin_required
import datetime
from . import api

order_model = api.model('order', {
    'meals': fields.String('A list of meal options to order')
})


class OrderResource(Resource):
    @authenticate
    @api.header('Authorization', type=str, description='Authentication token')
    def get(self, orderId):
        order = Order.get_by_id(orderId)
        if not order:
            return {
                'error': 'Order with such id {} doesnot exist'.format(orderId)
            }, 400

        return {
            'order': order.to_dict()
        }, 200

    @authenticate
    @api.expect(order_model)
    @api.header('Authorization', type=str, description='Authentication token')
    def put(self, orderId):
        order = Order.get_by_id(orderId)
        if not order:
            return {
                'error': 'Order with such id {} doesnot exist'.format(orderId)
            }, 400
        time_diff = datetime.timedelta(current_app.config['ORDER_EXPIRES_IN'])
        if order.expires_at and datetime.datetime.now() - order.expires_at > time_diff:  # noqa
            return {
                'error': 'Order expired and cannot be modify it'
            }, 400

        parser = reqparse.RequestParser()
        parser.add_argument(
            'meals', help='Meals id list is required', action='append')
        args = parser.parse_args()
        expires_at = datetime.datetime.now(
        ) + datetime.timedelta(minutes=current_app.config['ORDER_EXPIRES_IN'])
        order.expires_at = expires_at
        total_cost = 0
        order.meals.clear()  # remove all items from the array
        for meal_id in args['meals']:
            meal = MealOption.get_by_id(int(meal_id))
            if meal:
                total_cost += meal.price
                order.meals.append(meal)

        order.total_cost = total_cost
        return {
            'order': order.to_dict()
        }, 200


class OrdersResource(Resource):
    @authenticate
    @admin_required
    @api.header('Authorization', type=str, description='Authentication token')
    def get(self):
        return {
            'orders': [order.to_dict() for order in data.orders]
        }

    @authenticate
    @api.expect(order_model)
    @api.header('Authorization', type=str, description='Authentication token')
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'meals', help='Meals list is required', action='append')
        args = parser.parse_args()

        total_cost = 0
        order = Order()
        order.user = g.current_user

        for meal_id in args['meals']:
            meal = MealOption.get_by_id(int(meal_id))
            if meal:
                total_cost += meal.price
                order.meals.append(meal)

        expires_at = datetime.datetime.now(
        ) + datetime.timedelta(minutes=current_app.config['ORDER_EXPIRES_IN'])
        order.expires_at = expires_at
        order.total_cost = total_cost
        order.save()
        return {
            'order': order.to_dict()
        }, 201
