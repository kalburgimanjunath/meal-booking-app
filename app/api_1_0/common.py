"""
Module to store helper functions for validation
"""
import datetime
import validators
from ..models import Meal, User


def str_type(value):
    """
    str_type. validates a type is a string and not empty
    """
    if not isinstance(value, str):
        raise ValueError("Field value must be a string")
    if not value.strip(' '):
        raise ValueError("This field cannot be empty")
    return value


def price_type(value):
    """
    price_type. validates price is an integer and not empty
    """
    if not isinstance(value, int):
        raise ValueError("Price value must be a integer")
    if not value:
        raise ValueError("Price cannot be empty")
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

    if not value.strip(' '):
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
