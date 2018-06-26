"""
Module contains the role model.
"""
from .. import db
from . base_model import BaseModel


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
