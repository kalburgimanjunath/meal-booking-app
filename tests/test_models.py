import flask
from app.models import User, Menu, MealOption, Catering, Order
import unittest
from tests import ApiTestCase


class UserModelTestCase(ApiTestCase):
    """
    Tests for the user model object
    """

    def test_password_setter(self):
        self.user.password = 'test'
        self.assertTrue(self.user.password_hash is not None)

    def test_password_getter(self):
        with self.assertRaises(AttributeError):
            self.user.password

    def test_password_verification(self):
        self.user.password = 'test'
        self.assertFalse(self.user.verify_password('cat'))

    def test_generate_token(self):
        token = self.user.generate_jwt_token()
        self.assertIsInstance(token, str)

    def test_save_user(self):
        self.user.save()
        self.assertIsNotNone(self.user.id)

    def test_verify_token(self):
        self.user.save()
        token = self.user.generate_jwt_token()
        self.assertIsNotNone(User.verify_jwt_token(token))

    def test_save_menu(self):
        menu = Menu(title='menu 1', description='lorem ipsum')
        menu.save()
        self.assertIsInstance(menu.id, int)

    def test_save_meal_option(self):
        opt = MealOption('beef with rice', 1000, 'lorem ipsum')
        opt.save()
        self.assertIsNotNone(opt.id)

    def test_save_order(self):
        order = Order()
        order.total_cost = 1000
        order.user = self.user
        order.save()
        self.assertIsInstance(order.id, int)
