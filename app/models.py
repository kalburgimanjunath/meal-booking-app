"""
This module contains models of entities showing how they relate to each other
"""

from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash


class data:
    """
     This class holds the mock data objects used to store application data
    """
    users = []
    menus = []
    meals = []
    caterings = []
    orders = []


class User:
    """
    User class for storing data about a user of the application
    """

    def __init__(self, name, email):
        self.id = None
        self.name = name
        self.email = email
        self.password_hash = None
        self.is_admin = False

    @property
    def password(self):
        raise AttributeError('password is not readable')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def save(self):
        if not data.users:
            self.id = 1
        else:
            u = data.users[-1]
            self.id = u.id + 1
        data.users.append(self)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'is_admin': self.is_admin
        }

    @staticmethod
    def get_by_email(val):
        for u in data.users:
            if u.email == val:
                return u
        return None

    @staticmethod
    def get_by_id(val):
        for u in data.users:
            if u.id == val:
                return u
        return None

    def generate_jwt_token(self):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=36000)
        return s.dumps({
            'id': self.id,
            'name': self.name,
            'email': self.email
        }).decode('ascii')

    @staticmethod
    def verify_jwt_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])

        try:
            user = s.loads(token)
        except:
            return None
        return User.get_by_id(user['id'])


class Catering:
    """
    Catering class for storing data about catering business managed by admin
    """

    def __init__(self, name, address):
        self.id = None
        self.name = name
        self.address = address
        self.admin = None
        self.meal_options = []
        self.menus = []

    def save(self):
        if not data.caterings:
            self.id = 1
        else:
            self.id = data.caterings[-1] + 1
        data.caterings.append(self)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address
        }


class Menu:
    """
    Menu class fot storing data about a menu
    """

    def __init__(self, title, description):
        self.id = None
        self.title = title
        self.description = description
        self.meals = []
        self.menu_date = None
        self.catering = None

    def save(self):
        if not data.menus:
            self.id = 1
        else:
            self.id = data.menus[-1].id + 1
        data.menus.append(self)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'meals': [meal.to_dict() for meal in self.meals],
            'menuDate': self.menu_date
        }


class MealOption:
    """
    MealOption for storing data about a meal
    """

    def __init__(self, title, price, description=None):
        self.id = None
        self.title = title
        self.price = price
        self.description = description
        self.catering = None

    def save(self):
        if not data.meals:
            self.id = 1
        else:
            self.id = data.meals[-1].id + 1
        data.meals.append(self)

    @staticmethod
    def get_by_id(id):
        for meal in data.meals:
            if meal.id == id:
                return meal
        return None

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price
        }


class Order:
    """
    Order class for storing data about customer order
    """

    def __init__(self):
        self.id = None
        self.meals = []
        self.total_cost = 0
        self.user = User(None, None)
        self.catering = None
        self.expires_at = None

    def save(self):
        if not data.orders:
            self.id = 1
        else:
            self.id = data.orders[-1].id + 1
        data.orders.append(self)

    @staticmethod
    def get_by_id(id):
        for order in data.orders:
            if order.id == id:
                return order
        return None

    def to_dict(self):
        return {
            'id': self.id,
            'cost': self.total_cost,
            'expiresAt': str(self.expires_at),
            'meals': [meal.to_dict() for meal in self.meals],
            'customer': self.user.to_dict()
        }
