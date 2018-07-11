"""
Module contains API resource for exposing catering menus
"""

from datetime import datetime
from flask_restplus import Resource, fields, abort
from flask import g
from .decorators import authenticate, admin_required
from . import api
from . import parsers
from .common import validate_meals_list
from ..models import Menu, Meal

MENU_MODAL = api.model('Menu', {
    'title': fields.String(max_length=64),
    'menu_date': fields.Date(),
    'description': fields.String(max_length=200),
    'meals': fields.List(fields.Integer)
})


class GetMenuResource(Resource):
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
    @api.expect(MENU_MODAL, validate=True)
    @api.header('Authorization', type=str, description='Authentication token')
    def post(self):
        """
        Allows a business create a specific day menu
        """

        args = parsers.menu_modal.parse_args()
        user = g.current_user

        menu = Menu(title=args['title'], description=args['description'],
                    menu_date=args['menu_date'], catering=user.catering)
        meals = args['meals']
        validate_meals_list(meals)
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
        abort(code=400, message='Requested menu with id {} does not exist'.format(menu_id))

    @authenticate
    @admin_required
    @api.expect(MENU_MODAL, validate=True)
    @api.header('Authorization', type=str, description='Authentication token')
    def put(self, menu_id):
        """
        modifies a menu
        """
        menu = Menu.query.filter_by(id=menu_id).filter_by(
            catering=g.current_user.catering).first()
        if not menu:
            abort(code=400, message='menu with id {} does not exist'.format(menu_id))
        args = parsers.edit_menu_modal.parse_args()
        if args.get('meals', None):
            validate_meals_list(args["meals"])
        modified = menu.modify(args)
        if modified:
            menu.save()
            return menu.to_dict(), 200
        abort(code=400, message='No field(s) specified to be modified')

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
                'status': 'ok',
                'message': 'Menu deleted successfully'
            }, 200
        abort(
            code=400, message='Menu with id {0} doesnot exist'.format(menu_id)
        )
