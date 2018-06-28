"""
Module to store helper functions for validation
"""

import datetime
import validators
from dateutil import parser as date_parser
from flask import g
from flask_restplus import abort
from ..models import Meal, User, Menu


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


def validate_meals_list(meals):
    """
    validates a list of meals
    """
    for meal_id in meals:
        meal = Meal.query.filter_by(id=meal_id).first()
        if not meal:
            abort(code=400, message='No meal exists with id: {}'.format(meal_id))
