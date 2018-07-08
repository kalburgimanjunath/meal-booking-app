"""
Module contains API resource parsers
"""
from flask_restplus import reqparse
from .common import str_type, edit_menu_date_type, menu_date_type, type_menu_id

menu_modal = reqparse.RequestParser()
menu_modal.add_argument('title', type=str_type, required=True)
menu_modal.add_argument('description', type=str_type)
menu_modal.add_argument('meals', required=True, action='append')
menu_modal.add_argument('menu_date', type=menu_date_type, required=True)


edit_menu_modal = reqparse.RequestParser()
edit_menu_modal.add_argument('title', type=str_type)
edit_menu_modal.add_argument('description', type=str_type)
edit_menu_modal.add_argument('meals', action='append')
edit_menu_modal.add_argument('menu_date', type=edit_menu_date_type)


orders_parser = reqparse.RequestParser()
orders_parser.add_argument('menuId', type=type_menu_id, required=True)
orders_parser.add_argument('meals', required=True, action='append')
orders_parser.add_argument('orderCount', required=True, type=int)


edit_orders_parser = reqparse.RequestParser()
edit_orders_parser.add_argument('meals', required=True, action='append')
edit_orders_parser.add_argument('orderCount', required=True, type=int)
