"""
Module contains API resource parsers
"""
from flask_restplus import reqparse
from .common import str_type, edit_menu_date_type, menu_date_type

menu_modal = reqparse.RequestParser()
menu_modal.add_argument('title', type=str_type, required=True)
menu_modal.add_argument('description', type=str_type)
menu_modal.add_argument('meals', required=True, action='append')
menu_modal.add_argument('date', type=menu_date_type, required=True)


edit_menu_modal = reqparse.RequestParser()
edit_menu_modal.add_argument('title', type=str_type)
edit_menu_modal.add_argument('description', type=str_type)
edit_menu_modal.add_argument('meals', action='append')
edit_menu_modal.add_argument('date', type=edit_menu_date_type)
