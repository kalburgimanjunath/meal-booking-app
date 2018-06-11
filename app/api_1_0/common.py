"""
Module to store helper functions for validation
"""
import os
import errno
import datetime
import uuid
import validators
from dateutil import parser as date_parser
from flask import current_app, g
from ..models import Meal, User, Menu


def silentremove(path):
    """
    silently removes a file
    """
    try:
        os.remove(path)
    except OSError as e:
        if e.errno != errno.ENOENT:
            raise


def validate_meals(value):
    """
    validates a list of meals
    """
    if not is_list(value):
        raise ValueError("Field meals is required and should be a JSON array")
    for meal_id in value:
        meal = Meal.query.get(meal_id)
        if not meal:
            raise ValueError("Meal ids donot correspond to any meal")
    return value


def menu_date_type(value):
    """
    validates menu date and ensures only one menu is created for a date
    """
    value = edit_menu_date_type(value)
    user = g.current_user
    menu_date = date_parser.parse(value)
    menu = Menu.query.filter_by(
        catering=user.catering).filter_by(date=menu_date).first()
    if menu:
        raise ValueError(
            'Menu for the specific date {} is already set'.format(value))
    return value


def edit_menu_date_type(value):
    """
    validates menu date
    """
    value = str_type(value)
    if not validate_date(value):
        raise ValueError('Incorrect date format, should be YYYY-MM-DD')
    return value


def save_image(args):
    """
    save_image. saves image uploads
    """
    if args['image_file']:
        mime_type = args['image_file'].mimetype
        if mime_type == 'image/png' or mime_type == 'image/jpeg':
            if 'png' in mime_type:
                file_type = 'png'
            elif 'jpeg' in mime_type:
                file_type = 'jpeg'
            destination = os.path.join(
                current_app.config.get('DATA_FOLDER'), 'medias/')
            if not os.path.exists(destination):
                os.makedirs(destination)

            image_file = '%s%s' % (
                destination, '{0}.{1}'.format(uuid.uuid4(), file_type))
            args['image_file'].save(image_file)
            return image_file.replace('app', '')
    return None


def type_menu_id(value):
    """
    type_menu_id defines a type for validating menu id
    """
    if not isinstance(value, int):
        raise ValueError("Field value must be an integer")
    menu = Menu.query.get(value)
    if not menu:
        raise ValueError("Menu with id {} does not exist".format(value))
    return value


def str_type(value):
    """
    str_type. validates a type is a string and not empty
    """
    if not isinstance(value, str):
        raise ValueError("Field value must be a string")
    elif not value.strip(' '):
        raise ValueError("This field cannot be empty")
    return value


def price_type(value):
    """
    price_type. validates price is an integer and not empty
    """
    if not isinstance(value, int):
        raise ValueError("Price value must be a integer")
    elif not value or value <= 0:
        raise ValueError("Price cannot be less or equal to zero / empty")
    return value


def validate_email_type(value):
    """
    validate_email_type. validates a string is an email
    """
    result = validators.email(value)
    if result:
        return True
    return False


def validate_date(date_text):
    """
    validate_date. validates that a string is a date and of format YYYY-MM-DD
    """
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def email_type(value):
    """
    email_type. validates an email and ensures no user exists with same email
    """
    if not isinstance(value, str):
        raise ValueError("Email must be a string")
    elif not value.strip(' '):
        raise ValueError("Email field is required")
    is_valid = validate_email_type(value)
    if not is_valid:
        raise ValueError('Email is not valid')
    user = User.query.filter_by(email=value).first()
    if user is not None:
        raise ValueError("Email already in use")
    return value


def is_list(value):
    """
    is_list. determines a value is of type list
    """
    if not isinstance(value, list):
        return False
    return True


def validate_meals_list(meals):
    if not is_list(meals):
        return {
            'errors': {
                'meals': 'Field meals is required and should be a JSON array'
            }
        }
    elif not meals:
        return {
            'errors': {'meals': 'List of meals cannot be empty'}
        }

    for meal_id in meals:
        try:
            meal = Meal.query.filter_by(id=int(meal_id)).first()
            if not meal:
                return {
                    'errors': {
                        'meals': 'No meal exists with id: {}'.format(meal_id)
                    }
                }
        except ValueError:
            return {
                'error': {
                    'meals': 'Values in meals field must  be integer ids of meals'  # noqa
                }
            }
    return None
