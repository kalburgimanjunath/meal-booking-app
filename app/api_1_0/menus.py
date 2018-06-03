from flask_restplus import Resource, reqparse, fields
from .decorators import authenticate, admin_required
from datetime import datetime
from .common import str_type, validate_date, validate_meals_list
from . import api
from dateutil import parser as date_parser
from flask import request, g
from ..models import Menu, Meal
from .. import db

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
        """
        Allows a business to retrieve all menus
        """
        user = g.current_user
        menus = Menu.query.filter_by(catering=user.catering).order_by(
            Menu.created_at.desc()).all()
        return {
            'menus': [menu.to_dict() for menu in menus],
            'status': 'success'
        }, 200


class MenuResource(Resource):
    """
     Exposes a menu as a resource
    """
    # @authenticate
    @api.header('Authorization', type=str, description='Authentication token')
    def get(self):
        """
        Allows a customer to get a specific day menu
        """
        current_date = datetime.now().date()
        # return all current day menus
        menus = Menu.query.filter_by(date=current_date).all()
        return {
            'menus': [menu.to_dict() for menu in menus]
        }, 200

    @authenticate
    @admin_required
    @api.expect(menu_model)
    @api.header('Authorization', type=str, description='Authentication token')
    def post(self):
        """
        Allows a business create a specific day menu
        """
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
        user = g.current_user
        menu_date = date_parser.parse(args['date'])
        menu = Menu.query.filter_by(
            catering=user.catering).filter_by(date=menu_date).first()
        if menu:
            return {
                'errors': {
                    'date': 'Menu for the specific date {} already set'.format(
                        args['date'])
                }
            }, 400

        menu = Menu(title=args['title'], description=args['description'],
                    date=menu_date, catering=user.catering)
        for meal_id in meals:
            meal = Meal.query.get(meal_id)
            menu.meals.append(meal)
        db.session.add(menu)
        db.session.commit()
        return menu.to_dict(), 201


class SpecificMenuResource(Resource):
    """
     Returns a menu of a given id
    """

    def get(self, id):
        """
        Returns a menu with a specific id.
        """
        menu = Menu.query.get(id)
        if menu:
            return {
                'menu': menu.to_dict()
            }
