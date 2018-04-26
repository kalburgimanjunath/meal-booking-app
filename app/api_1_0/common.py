"""
Module to store common functions
"""


def str_type(value):
    if not isinstance(value, str):
        raise ValueError("Field value must be a string")
    if not value or len(value.strip(' ')) == 0:
        raise ValueError("This field cannot be empty")
    return value
