"""
This module contains models of entities showing how they relate to each other
"""
import datetime
from flask import current_app
from dateutil import parser
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash
from . import db


class BaseModel(db.Model):
    """
    Base model for all db models.
    """
    __abstract__ = True
    created_at = db.Column(db.DateTime(), default=db.func.current_timestamp())

    def save(self):
        """
        save. saves model to the database
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """
        delete. removes a model from database
        """
        db.session.delete(self)
        db.session.commit()


class Permission:
    """
     Permission represents persmissions held by a role
    """
    CUSTOMER = 2
    CATERER = 4


class Role(BaseModel):
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


class User(BaseModel):
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

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            self.role = Role.query.filter_by(default=True).first()

    @property
    def password(self):
        """
        makes password a write only attribute
        """
        raise AttributeError('password is not readable')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        verify_password. verifies a user's password
        """
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
        """
        generate_jwt_token. generates a jwt token after user authentication
        """
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


class Catering(BaseModel):
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


menu_meals = db.Table('menu_meals',
                      db.Column('menu_id', db.Integer, db.ForeignKey(
                          'menus.id'), primary_key=True),
                      db.Column('meal_id', db.Integer, db.ForeignKey(
                          'meals.id'), primary_key=True))


class Menu(BaseModel):
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

    @property
    def menu_date(self):
        """
        define property menu date for setting or getting date
        """
        return str(self.date)

    @menu_date.setter
    def menu_date(self, menu_date):
        self.date = parser.parse(menu_date)

    def modify(self, args):
        """
        modifies self, setting attributes
        """
        modified = False
        for key in args:
            if args[key] is not None:
                if key == 'meals' and args['meals']:
                    modified = True
                    self.meals.clear()
                    for meal_id in args['meals']:
                        meal = Meal.query.get(meal_id)
                        if meal:
                            self.meals.append(meal)
                elif hasattr(self, key):
                    modified = True
                    setattr(self, key, args[key])

        return modified

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


class Meal(BaseModel):
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

    def modify(self, args):
        """
        modifies self, setting attributes
        """
        modified = False
        for key in args:
            if args[key] is not None:
                if hasattr(self, key):
                    modified = True
                    setattr(self, key, args[key])
        return modified


order_meals = db.Table('order_meals',
                       db.Column('order_id', db.Integer, db.ForeignKey(
                           'orders.id'), primary_key=True),
                       db.Column('meal_id', db.Integer, db.ForeignKey(
                           'meals.id'), primary_key=True))


class Order(BaseModel):
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

    def is_expired(self):
        """
        is_expired. determines if an order is expired
        """
        time_diff = datetime.timedelta(
            minutes=current_app.config['ORDER_EXPIRES_IN'])
        if self.expires_at and datetime.datetime.now() - self.expires_at > time_diff:
            return True
        return False

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
