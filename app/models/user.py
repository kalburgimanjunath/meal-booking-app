"""
Module contains the User model.
"""
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash
from .. import db
from . base_model import BaseModel
from . role import Role, Permission


class User(BaseModel):
    """
    User class represents the users table
    """

    __tablename__ = 'users'
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
    def get_by_email(email):
        return User.query.filter_by(email=email).first()

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
