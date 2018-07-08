"""
Module contains the base model
"""
from .. import db


class BaseModel(db.Model):
    """
    Base model for all db models.
    """
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(), default=db.func.current_timestamp())

    def save(self):
        """
        save. saves model to the database
        """
        db.session.add(self)
        db.session.commit()

    def set_attr(self, key, value):
        """
        sets attribute on a model
        """
        if hasattr(self, key) and value is not None:
            setattr(self, key, value)
            return True
        return False

    def delete(self):
        """
        delete. removes a model from database
        """
        db.session.delete(self)
        db.session.commit()
