"""
Module contains API resource for exposing catering menus
"""
from datetime import datetime
from flask_restplus import Resource, fields
from dateutil import parser as date_parser
from flask import g
from .decorators import authenticate, admin_required
from .common import save_image, validate_meals
from . import api
from . import parsers
from ..models import Menu, Meal


class MenusResource(Resource):
    """
    MenusResource. for exposing menus as API endpoints
    """
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
        menus = Menu.query.filter_by(date=current_date).all()
        return {
            'menus': [menu.to_dict() for menu in menus]
        }, 200

    @authenticate
    @admin_required
    @api.expect(parsers.menu_modal)
    @api.header('Authorization', type=str, description='Authentication token')
    def post(self):
        """
        Allows a business create a specific day menu
        """
        args = parsers.menu_modal.parse_args()
        user = g.current_user
        menu_date = date_parser.parse(args['date'])

        image_path = save_image(args)
        menu = Menu(title=args['title'], description=args['description'],
                    date=menu_date, catering=user.catering, image_url=image_path)
        meals = args['meals']
        for meal_id in meals:
            meal = Meal.query.get(meal_id)
            if meal:
                menu.meals.append(meal)
        menu.save()
        return menu.to_dict(), 201


class SpecificMenuResource(Resource):
    """
     Returns a menu of a given id
    """

    def get(self, menu_id):
        """
        Returns a menu with a specific id.
        """
        menu = Menu.query.get(menu_id)
        if menu:
            return {
                'menu': menu.to_dict()
            }
        return {}
