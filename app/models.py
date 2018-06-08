"""
This module contains models of entities showing how they relate to each other
"""
import datetime
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash
from . import db


class Permission:
    """
     Permission represents persmissions held by a role
    """
    CUSTOMER = 2
    CATERER = 4


class Role(db.Model):
    """
     Role represents the roles table
    """

    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        """
        insert_roles. adds required user roles to the database
        """
        roles = {
            'Customer': (Permission.CUSTOMER, True),
            'Admin': (Permission.CATERER, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()


class User(db.Model):
    """
    User class represents the users table
    """

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    orders = db.relationship('Order', backref='customer', lazy='dynamic')
    created_at = db.Column(db.DateTime(), default=db.func.current_timestamp())

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            self.role = Role.query.filter_by(default=True).first()

    def save(self):
        """
        save. saves model to the db
        """
        db.session.add(self)
        db.session.commit()

    @property
    def password(self):
        raise AttributeError('password is not readable')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        """
        to_dict. returns object as serializable dict.
        """
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }

    def can(self, permissions):
        """
        can. determines if a user does have a given permissions.
        """
        return self.role is not None and \
            (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        """
        is_administrator. determines if a user is an administrator
        """
        return self.can(Permission.CATERER)

    def generate_jwt_token(self):
        s = Serializer(current_app.config['SECRET_KEY'],
                       expires_in=360000)
        return s.dumps({
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'isAdmin': self.is_administrator()
        }).decode('ascii')

    @staticmethod
    def verify_jwt_token(token):
        """
         Verifies a JWT token
        """
        serializer = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = serializer.loads(token)
        except:
            return None
        return User.query.get(data['id'])


class Catering(db.Model):
    """
    Catering class represents caterings table
    """
    __tablename__ = 'caterings'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100))
    menus = db.relationship('Menu', backref='catering', lazy='dynamic')
    meals = db.relationship('Meal', backref='catering', lazy='dynamic')
    orders = db.relationship('Order', backref='catering', lazy='dynamic')
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    admin = db.relationship(
        "User", backref=db.backref('catering', uselist=False))
    created_at = db.Column(db.DateTime(), default=db.func.current_timestamp())

    def to_dict(self):
        """
        to_dict. turns object to dict
        """
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address
        }

    def save(self):
        """
        save. saves model to the database
        """
        db.session.add(self)
        db.session.commit()


menu_meals = db.Table('menu_meals',
                      db.Column('menu_id', db.Integer, db.ForeignKey(
                          'menus.id'), primary_key=True),
                      db.Column('meal_id', db.Integer, db.ForeignKey(
                          'meals.id'), primary_key=True)
                      )


class Menu(db.Model):
    """
    Menu class represents the menus table
    """

    __tablename__ = 'menus'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text)
    date = db.Column(db.Date)
    meals = db.relationship('Meal', secondary=menu_meals, lazy='subquery',
                            backref=db.backref('menu', lazy=True))
    catering_id = db.Column(db.Integer, db.ForeignKey('caterings.id'))
    orders = db.relationship('Order', backref='menu', lazy='dynamic')
    created_at = db.Column(db.DateTime(), default=db.func.current_timestamp())

    def to_dict(self):
        """
          Turns Menu into a dict for easy serialization
        """
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'meals': [meal.to_dict() for meal in self.meals],
            'menuDate': str(self.date),
            'catering': {
                'id': self.id,
                'name': self.catering.name,
                'address': self.catering.address
            }
        }

    def save(self):
        db.session.add(self)
        db.session.commit()


class Meal(db.Model):
    """
    Meal class represents the meals table
    """
    __tablename__ = 'meals'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    catering_id = db.Column(db.Integer, db.ForeignKey('caterings.id'))
    created_at = db.Column(db.DateTime(), default=db.func.current_timestamp())

    def to_dict(self):
        """
          Turns Meal into a dict for easy serialization
        """
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price
        }


order_meals = db.Table('order_meals',
                       db.Column('order_id', db.Integer, db.ForeignKey(
                           'orders.id'), primary_key=True),
                       db.Column('meal_id', db.Integer, db.ForeignKey(
                           'meals.id'), primary_key=True)
                       )


class Order(db.Model):
    """
    Order class represents the orders table
    """
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    total_cost = db.Column(db.Float, nullable=False)
    order_count = db.Column(db.Integer, default=1)
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    catering_id = db.Column(db.Integer, db.ForeignKey('caterings.id'))
    menu_id = db.Column(db.Integer, db.ForeignKey('menus.id'))
    meals = db.relationship('Meal', secondary=order_meals, lazy='subquery',
                            backref=db.backref('order', lazy=True))
    expires_at = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, **kwargs):
        super(Order, self).__init__(**kwargs)
        self.expires_at = datetime.datetime.now(
        ) + datetime.timedelta(minutes=current_app.config['ORDER_EXPIRES_IN'])

    def to_dict(self):
        """
         Turns order into dict for easy serialization
        """
        return {
            'id': self.id,
            'cost': self.total_cost,
            'totalCost': self.total_cost / self.order_count,
            'expiresAt': str(self.expires_at),
            'meals': [meal.to_dict() for meal in self.meals],
            'customer': self.customer.to_dict(),
            'createdAt': str(self.created_at),
            'orderCount': self.order_count,
            'menuId': self.menu.id
        }
