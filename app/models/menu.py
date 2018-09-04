
from dateutil import parser
from flask import current_app
from .. import db
from . base_model import BaseModel
from . meal import Meal


menu_meals = db.Table('menu_meals',
                      db.Column('menu_id', db.Integer, db.ForeignKey(
                          'menus.id'), primary_key=True),
                      db.Column('meal_id', db.Integer, db.ForeignKey(
                          'meals.id'), primary_key=True)
                      )


class Menu(BaseModel):
    """
    Menu class represents the menus table
    """

    __tablename__ = 'menus'
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text)
    date = db.Column(db.String(20))
    meals = db.relationship('Meal', secondary=menu_meals, lazy='subquery',
                            backref=db.backref('menu', lazy=True))
    catering_id = db.Column(db.Integer, db.ForeignKey('caterings.id'))
    image_url = db.Column(db.String(256))
    orders = db.relationship('Order', backref='menu', lazy='dynamic')

    @property
    def menu_date(self):
        """
        define property menu date for setting or getting date
        """
        return str(self.date)

    @menu_date.setter
    def menu_date(self, menu_date):
        self.date = menu_date

    def append_meals(self, meals):
        """
        appends meals to menu
        """
        self.meals.clear()
        for meal_id in meals:
            meal = Meal.query.get(meal_id)
            self.meals.append(meal)
        return True

    def modify(self, args):
        """
        modifies self, setting attributes
        """
        modified = False
        for key in args:
            if key == 'meals' and args[key] is not None:
                modified = self.append_meals(args["meals"])
            elif args[key] is not None:
                modified = self.set_attr(key, args[key])
        return modified

    def to_dict(self):
        """
          Turns Menu into a dict for easy serialization
        """
        image_url = ""
        if self.image_url:
            image_url = current_app.config['BASE_URL'] + self.image_url
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'meals': [meal.to_dict() for meal in self.meals],
            'menuDate': self.date,
            'catering': {
                'id': self.id,
                'name': self.catering.name,
                'address': self.catering.address
            },
            'imageURL': image_url
        }
