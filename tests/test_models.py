from app.models import User, Menu, Order, Meal
from tests.base_test_case import ApiTestCase


class ModelsTestCase(ApiTestCase):
    """
    Tests models
    """

    def test_password_setter(self):
        self.user.password = 'test'
        self.assertTrue(self.user.password_hash is not None)

    def test_password_getter(self):
        with self.assertRaises(AttributeError):
            self.user.password

    def test_password_verification(self):
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
        opt = Meal(title='beef with rice', price=1000,
                   description='lorem ipsum')
        opt.save()
        self.assertIsNotNone(opt.id)

    def test_save_order(self):
        order = Order(total_cost=1000)
        order.save()
        self.assertIsInstance(order.id, int)
