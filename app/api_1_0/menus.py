from flask_restplus import Resource, reqparse, fields
from ..models import Menu, data, MealOption
from .decorators import authenticate, admin_required
from datetime import datetime
from .common import str_type, validate_date, validate_meals_list
from . import api
from dateutil import parser as date_parser
from flask import request

menu_model = api.model('Menu', {
    'date': fields.String('yyyy-mm-dd'),
    'title': fields.String('Title'),
    'description': fields.String('Optional)'),
    'meals': fields.String('[]')
})


class MenusResource(Resource):
    @authenticate
    @admin_required
    @api.header('Authorization', type=str, description='Authentication token')
    def get(self):
        return {
            'menus': [menu.to_dict() for menu in data.menus],
            'status': 'success'
        }, 200


class MenuResource(Resource):
    @authenticate
    @api.header('Authorization', type=str, description='Authentication token')
    def get(self):
        current_date = datetime.now().date()
        for menu in data.menus:
            if menu.menu_date == current_date:
                return menu.to_dict(), 200
        return {
            'message': 'menu not yet set.'
        }, 200

    @authenticate
    @admin_required
    @api.expect(menu_model)
    @api.header('Authorization', type=str, description='Authentication token')
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('date', type=str_type,
                            required=True, help='Date field is required')
        parser.add_argument('title', type=str_type, required=True,
                            help='Title field is required')
        parser.add_argument('description', type=str)
        args = parser.parse_args()
        meals = request.json.get('meals', '')
        val = validate_meals_list(meals)
        if val:
            return val, 400

        # validate date
        if not validate_date(args['date']):
            return {
                'errors': {
                    'date': 'Incorrect date format, should be YYYY-MM-DD'
                }
            }, 400
        menu = Menu(title=args['title'], description=args['description'],)
        m_date = date_parser.parse(args['date'])
        menu.menu_date = m_date.date()
        menu.add_meals(meals)
        menu.save()
        return menu.to_dict(), 201
