import datetime
from flask import current_app
from dateutil import parser
from .. import db
from . base_model import BaseModel


class Meal(BaseModel):
    """
    Meal class represents the meals table
    """
    __tablename__ = 'meals'
    title = db.Column(db.String(128), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    catering_id = db.Column(db.Integer, db.ForeignKey('caterings.id'))

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
