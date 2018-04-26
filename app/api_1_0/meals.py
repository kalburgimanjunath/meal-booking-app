from flask_restplus import Resource, reqparse
from ..models import Catering, MealOption, data
from .decorators import authenticate, admin_required


def str_type(value):
    if not isinstance(value, str):
        raise ValueError("Field value must be a string")
    if not value or len(value.strip(' ')) == 0:
        raise ValueError("This field cannot be empty")
    return value


class MealsResource(Resource):
    Resource.method_decorators.append(admin_required)
    Resource.method_decorators.append(authenticate)

    def get(self):
        return {
            'meals': [meal.to_dict() for meal in data.meals]
        }, 200

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
    Resource.method_decorators.append(admin_required)
    Resource.method_decorators.append(authenticate)

    def get(self, mealId):
        meal = MealOption.get_by_id(mealId)
        if not meal:
            return {
                'error': 'Bad request, no meal with such id exists'
            }, 400
        return {
            'meal': meal.to_dict()
        }, 200

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
