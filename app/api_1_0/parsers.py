"""
Module contains API resource parsers
"""
import werkzeug
from flask_restplus import reqparse
from .common import str_type

menu_modal = reqparse.RequestParser()
menu_modal.add_argument('title', type=str_type,
                        required=True, help='Title field is required')
menu_modal.add_argument('description', type=str)
menu_modal.add_argument('image_file', type=werkzeug.datastructures.FileStorage,
                        location='files', help='Menu image file')
menu_modal.add_argument('meals', required=True,
                        action='append')
