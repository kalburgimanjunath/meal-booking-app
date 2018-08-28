"""
Module contains the order model
"""
import datetime
from flask import current_app
from .. import db
from . base_model import BaseModel
from .meal import Meal


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
    total_cost = db.Column(db.Float, nullable=False)
    order_count = db.Column(db.Integer, default=1)
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    catering_id = db.Column(db.Integer, db.ForeignKey('caterings.id'))
    menu_id = db.Column(db.Integer, db.ForeignKey('menus.id'))
    meals = db.relationship('Meal', secondary=order_meals, lazy='subquery',
                            backref=db.backref('order', lazy=True))
    expires_at = db.Column(db.DateTime, nullable=False)

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

    def add_meals(self, meals):
        total_cost = 0
        for meal_id in meals:
            meal = Meal.query.get(int(meal_id))
            if meal:
                total_cost += meal.price
                self.meals.append(meal)
        return total_cost

    def to_dict(self):
        """
         Turns order into dict for easy serialization
        """
        menu_id = 0
        if self.menu:
            menu_id = self.menu.id
        return {
            'id': self.id,
            'cost': self.total_cost,
            'totalCost': self.total_cost / self.order_count,
            'expiresAt': str(self.expires_at),
            'meals': [meal.to_dict() for meal in self.meals],
            'customer': self.customer.to_dict(),
            'createdAt': str(self.created_at),
            'orderCount': self.order_count,
            'menuId': menu_id
        }
