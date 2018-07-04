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

    def delete(self):
        """
        delete. removes a model from database
        """
        db.session.delete(self)
        db.session.commit()


def make_pivot_table(name, fk_1, tb_1, fk_2, tb_2):
    """
    generates a pivot table.
    """
    table = db.Table(name,
                     db.Column(fk_1, db.Integer, db.ForeignKey(
                         tb_1), primary_key=True),
                     db.Column(fk_2, db.Integer, db.ForeignKey(
                         tb_2), primary_key=True))

    return table
