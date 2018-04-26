from flask_restplus import Resource, reqparse
from ..models import Menu, data, MealOption
from .decorators import authenticate, admin_required
from datetime import datetime


def str_type(value):
    if not isinstance(value, str):
        raise ValueError("Field value must be a string")
    if not value or len(value.strip(' ')) == 0:
        raise ValueError("This field cannot be empty")
    return value


class MenusResource(Resource):
    @authenticate
    @admin_required
    def get(self):
        return {
            'menus': [menu.to_dict() for menu in data.menus]
        }, 200


class MenuResource(Resource):
    @authenticate
    def get(self):
        current_date = datetime.now().date()
        for menu in data.menus:
            if menu.menu_date == str(current_date):
                return {
                    'menu': menu.to_dict()
                }, 200
        return {
            'message': 'menu not yet set.'
        }, 200

    @authenticate
    @admin_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('menuDate', type=str_type,
                            required=True, help='Date field is required')
        parser.add_argument('title', type=str_type, required=True,
                            help='Title field is required')
        parser.add_argument('description', type=str)
        parser.add_argument(
            'meals', help='Meals list is required', action='append')
        args = parser.parse_args()

        menu = Menu(title=args['title'], description=args['description'])
        menu.menu_date = args['menuDate']
        for meal_id in args['meals']:
            meal = MealOption.get_by_id(int(meal_id))
            if meal:
                menu.meals.append(meal)
        menu.save()
        return {
            'menu': menu.to_dict()
        }, 201
