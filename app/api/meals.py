"""
Module contain API resources for exposing meals
"""
from flask_restplus import Resource, reqparse, fields, abort
from flask import g
from ..models import Meal
from .decorators import authenticate, admin_required
from .common import str_type
from . import api

MEAL_MODAL = api.model('Meal', {
    'title': fields.String(max_length=64),
    'price': fields.Integer(min=100),
    'description': fields.String(max_length=64)
})


class MealsResource(Resource):
    """
    MealsResource exposes meals as an endpoint
    """
    @authenticate
    @admin_required
    @api.header('Authorization', type=str, description='Authentication token')
    def get(self):
        """
        Allows a business to retrieve all meals
        """
        user = g.current_user
        return {
            'meals': [meal.to_dict() for meal in user.catering.meals],
            'status': 'success'
        }, 200

    @authenticate
    @admin_required
    @api.expect(MEAL_MODAL, validate=True)
    @api.header('Authorization', type=str, description='Authentication token')
    def post(self):
        """
        Allows a business to add new meals
        """
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str_type, required=True)
        parser.add_argument('price', type=int, required=True)
        parser.add_argument('description', type=str_type)

        args = parser.parse_args()
        user = g.current_user
        meal = Meal(title=args['title'], price=args['price'],
                    description=args['description'], catering=user.catering)
        meal.save()
        return meal.to_dict(), 201


class MealResource(Resource):
    """
     MealResource exposes a meal as an API resource
    """
    @authenticate
    @admin_required
    @api.header('Authorization', type=str, description='Authentication token')
    def get(self, meal_id):
        """
         Handles a get request for a meal by id
        """
        user = g.current_user
        meal = Meal.query.filter_by(
            catering=user.catering).filter_by(id=meal_id).first()
        if not meal:
            abort(code=400, message='No meal with such id {} exists'.format(meal_id))
        return meal.to_dict(), 200

    @authenticate
    @admin_required
    @api.expect(MEAL_MODAL, validate=True)
    @api.doc(responses={200: 'Success', 400: 'Bad request',
                        401: 'Authorization failed'})
    @api.header('Authorization', type=str, description='Authentication token')
    def put(self, meal_id):
        """
        Put handles put request for modifying a meal
        """
        user = g.current_user
        meal = Meal.query.filter_by(
            catering=user.catering).filter_by(id=meal_id).first()
        if not meal:
            abort(code=400, message='No meal with such id {} exists'.format(meal_id))

        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str)
        parser.add_argument('price', type=int)
        parser.add_argument('description', type=str)
        args = parser.parse_args()

        modified = meal.modify(args)
        if modified:
            meal.save()
            return meal.to_dict(), 200
        abort(code=400, message='Specify a field or fields to be edited')

    @authenticate
    @admin_required
    @api.header('Authorization', type=str, description='Authentication token')
    def delete(self, meal_id):
        """
        delete removes a meal
        """
        user = g.current_user
        meal = Meal.query.filter_by(
            catering=user.catering).filter_by(id=meal_id).first()
        if meal:
            meal.delete()
            return {
                'status': 'ok',
                'message': 'meal successfully deleted'
            }, 200
        abort(code=400, message='No meal with such id {} exists'.format(meal_id))
