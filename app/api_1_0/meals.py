from flask_restplus import Resource, reqparse, fields
from ..models import Catering, Meal
from .decorators import authenticate, admin_required
from .common import str_type, price_type
from . import api
from flask import g
from .. import db

meal_modal = api.model('Meal', {
    'title': fields.String('Meal title'),
    'price': fields.String('Meal price'),
    'description': fields.String('Meal Description')
})


class MealsResource(Resource):

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
    @api.expect(meal_modal)
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
        title = args['title']
        price = args['price']
        description = args['description']
        user = g.current_user
        meal = Meal(title=title, price=price,
                    description=description, catering=user.catering)
        db.session.add(meal)
        db.session.commit()

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
    @api.expect(meal_modal)
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
        parser.add_argument('title', type=str_type,
                            required=True, help='Title field is required')
        parser.add_argument('price', type=price_type, required=True)
        parser.add_argument('description', type=str)
        args = parser.parse_args()

        meal.title = args['title']
        meal.price = args['price']
        meal.description = args['description']
        db.session.add(meal)
        db.session.commit()

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
            db.session.delete(meal)
            db.session.commit()
            return {
                'message': 'successfully deleted'
            }, 200
        return {
            'error': 'no meal with such id exists'
        }, 400
