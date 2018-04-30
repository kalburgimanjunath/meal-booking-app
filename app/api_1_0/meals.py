from flask_restplus import Resource, reqparse, fields
from ..models import Catering, MealOption, data
from .decorators import authenticate, admin_required
from .common import str_type
from . import api

meal_modal = api.model('Meal', {
    'title': fields.String('Meal title'),
    'price': fields.String('Meal price'),
    'description': fields.String('Meal Description')
})


class MealsResource(Resource):

    @authenticate
    @admin_required
    def get(self):
        return {
            'meals': [meal.to_dict() for meal in data.meals]
        }, 200

    @authenticate
    @admin_required
    @api.expect(meal_modal)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str_type,
                            required=True, help='Title field is required')
        parser.add_argument('price', type=float, required=True,
                            help='Price field is required')
        parser.add_argument('description', type=str)

        args = parser.parse_args()
        title = args['title']
        price = args['price']
        description = args['description']
        meal = MealOption(title=title, price=price, description=description)
        meal.save()

        return {
            'meal': meal.to_dict()
        }, 201


class MealResource(Resource):

    @authenticate
    @admin_required
    def get(self, mealId):
        meal = MealOption.get_by_id(mealId)
        if not meal:
            return {
                'error': 'Bad request, no meal with such id exists'
            }, 400
        return {
            'meal': meal.to_dict()
        }, 200

    @authenticate
    @admin_required
    @api.expect(meal_modal)
    def put(self, mealId):
        meal = MealOption.get_by_id(mealId)
        if not meal:
            return {
                'error': 'Bad request, no meal with such id exists'
            }, 400
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str_type,
                            required=True, help='Title field is required')
        parser.add_argument('price', type=float, required=True,
                            help='Price field is required')
        parser.add_argument('description', type=str)
        args = parser.parse_args()

        meal.title = args['title']
        meal.price = args['price']
        meal.description = args['description']

        return {
            'meal': meal.to_dict()
        }, 200

    @authenticate
    @admin_required
    def delete(self, mealId):
        for meal in data.meals:
            if meal.id == mealId:
                data.meals.remove(meal)
                return {
                    'message': 'successfully deleted'
                }, 200
        return {
            'error': 'no such meal with the id exists'
        }, 400
