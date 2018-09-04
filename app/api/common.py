"""
Module to store helper functions for validation
"""

import datetime
import os
from flask import (current_app, g)
import uuid
import validators
import boto3
import botocore

from dateutil import parser as date_parser
from flask_restplus import abort
from ..models import Meal, User, Menu


def menu_date_type(value):
    """
    validates menu date and ensures only one menu is created for a date
    """
    value = edit_menu_date_type(value)
    user = g.current_user
    # menu_date = date_parser.parse(value)
    menu = Menu.query.filter_by(
        catering=user.catering).filter_by(date=value).first()
    if menu:
        raise ValueError(
            'Menu for the specific day {} is already set'.format(value))
    return value.lower()


def edit_menu_date_type(value):
    """
    validates menu date
    """
    value = str_type(value)
    days = ['monday', 'tuesday', 'wednesday',
            'thursday', 'friday', 'saturday', 'sunday']
    if not value.lower() in days:
        raise ValueError('Incorrect day')
    return value.lower()


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
        raise ValueError("This field is required")
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
    value = str_type(value)
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
    if isinstance(meals, str):
        meals = meals.split(',')
    for meal_id in meals:
        meal = Meal.query.filter_by(id=meal_id).first()
        if not meal:
            abort(code=400, message='No meal exists with id: {}'.format(meal_id))


def save_image(args):
    """
    save_image. saves image uploads
    """
    if args['imageFile']:
        mime_type = args['imageFile'].mimetype
        if mime_type == 'image/png' or mime_type == 'image/jpeg':
            if 'png' in mime_type:
                file_type = 'png'
            elif 'jpeg' in mime_type:
                file_type = 'jpeg'
            destination = os.path.join(
                current_app.config.get('DATA_FOLDER'), 'medias/')
            if not os.path.exists(destination):
                os.makedirs(destination)
            file_name = '{0}.{1}'.format(uuid.uuid4(), file_type)
            s3_file = args['imageFile'].stream
            s3_file_name = save_file_to_s3_storage(s3_file, file_name)
            return s3_file_name
    return None


def make_integer(number):
    return int(number)


def save_file_to_s3_storage(file, file_name):
    s3 = boto3.client(
        "s3",
        aws_access_key_id=current_app.config['S3_KEY'],
        aws_secret_access_key=current_app.config['S3_SECRET']
    )
    try:
        s3.upload_fileobj(file,
                          current_app.config['S3_BUCKET'],
                          file_name)
        return '{}{}'.format(current_app.config['S3_LOCATION'], file_name)
    except Exception as e:
        print(e)
        return None
