"""
Module contains the catering model.
"""
from .. import db
from . base_model import BaseModel


class Catering(BaseModel):
    """
    Catering class represents caterings table
    """
    __tablename__ = 'caterings'
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(100))
    menus = db.relationship('Menu', backref='catering', lazy='dynamic')
    meals = db.relationship('Meal', backref='catering', lazy='dynamic')
    orders = db.relationship('Order', backref='catering', lazy='dynamic')
    admin_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    admin = db.relationship(
        "User", backref=db.backref('catering', uselist=False))

    def to_dict(self):
        """
        to_dict. turns object to dict
        """
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address
        }
