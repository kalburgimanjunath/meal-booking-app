"""
Module contains API resource for exposing catering menus
"""
from datetime import datetime
from flask_restplus import Resource
from dateutil import parser as date_parser
from flask import g
from .decorators import authenticate, admin_required
from .common import save_image, menu_date_type, edit_menu_date_type, silentremove
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
        parsers.menu_modal.add_argument(
            'date', type=menu_date_type, required=True)
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
    @authenticate
    @api.header('Authorization', type=str, description='Authentication token')
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

    @authenticate
    @admin_required
    @api.expect(parsers.menu_modal)
    @api.header('Authorization', type=str, description='Authentication token')
    def put(self, menu_id):
        """
        modifies a menu
        """
        menu = Menu.query.filter_by(id=menu_id).filter_by(
            catering=g.current_user.catering).first()
        if not menu:
            return {
                'error': 'menu with id {} does not exist'.format(menu_id)
            }, 400
        parsers.menu_modal.add_argument(
            'date', type=edit_menu_date_type, required=True)
        args = parsers.menu_modal.parse_args()
        image_path = save_image(args)
        if image_path is not None:
            silentremove('app{0}'.format(menu.image_url))
            menu.image_url = image_path
        menu.title = args['title']
        menu.description = args['description']
        menu.date = date_parser.parse(args['date'])

        menu.meals.clear()
        meals = args['meals']
        for meal_id in meals:
            meal = Meal.query.get(meal_id)
            if meal:
                menu.meals.append(meal)
        menu.save()
        return menu.to_dict(), 200

    @authenticate
    @admin_required
    @api.header('Authorization', type=str, description='Authentication token')
    def delete(self, menu_id):
        """
        deletes a caterer's menu
        """
        menu = Menu.query.filter_by(id=menu_id).filter_by(
            catering=g.current_user.catering).first()
        if menu:
            menu.delete()
            return {
                'status': 'Menu deleted successfully'
            }
        return {
            'error': 'Menu with id {0} doesnot exist'.format(menu_id)
        }
