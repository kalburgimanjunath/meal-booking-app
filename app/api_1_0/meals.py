"""
Module contain API resources for exposing meals
"""
from flask_restplus import Resource, reqparse, fields
from flask import g
from ..models import Meal
from .decorators import authenticate, admin_required
from .common import str_type, price_type
from . import api

MEAL_MODAL = api.model('Meal', {
    'title': fields.String('Meal title'),
    'price': fields.String('Meal price'),
    'description': fields.String('Meal Description')
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
    @api.expect(MEAL_MODAL)
    @api.header('Authorization', type=str, description='Authentication token')
    def post(self):
        """
        Allows a business to add new meals
        """
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str_type,
                            required=True, help='Title field is required')
        parser.add_argument('price', type=price_type, required=True)
        parser.add_argument('description', type=str)

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
            return {
                'error': 'Bad request, no meal with such id exists'
            }, 400
        return meal.to_dict(), 200

    @authenticate
    @admin_required
    @api.expect(MEAL_MODAL)
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
            return {
                'error': 'Bad request, no meal with such id exists'
            }, 400
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str)
        parser.add_argument('price', type=price_type)
        parser.add_argument('description', type=str)
        args = parser.parse_args()

        modified = meal.modify(args)
        if modified:
            meal.save()
        else:
            return {
                'error': 'No fields specified to be modified'
            }, 400
        return meal.to_dict(), 200

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
                'message': 'successfully deleted'
            }, 200
        return {
            'error': 'no meal with such id exists'
        }, 400
