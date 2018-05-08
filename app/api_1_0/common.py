"""
Module to store common functions
"""
import datetime
import validators
from ..models import Meal


def str_type(value):
    if not isinstance(value, str):
        raise ValueError("Field value must be a string")
    if not value or len(value.strip(' ')) == 0:
        raise ValueError("This field cannot be empty")
    return value


def price_type(value):
    if not isinstance(value, int):
        raise ValueError("Price value must be a integer")
    if not value:
        raise ValueError("Price cannot be empty")
    return value


def validate_email_type(value):
    result = validators.email(value)
    if result:
        return True
    return False


def validate_date(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def is_list(value):
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
