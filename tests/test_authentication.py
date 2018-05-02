from tests import ApiTestCase
from app.models import User


class AuthenticationTestCase(ApiTestCase):
    """
    Test for authentication endpoints
    """

    def test_api_cannot_register_user_with_empty_email(self):
        self.test_user['email'] = ''
        res = self.make_post_request(
            self.user_register_endpoint, self.test_user)
        self.assertEqual(res.status_code, 400)

    def test_api_cannot_register_user_with_empty_password(self):
        self.test_user['password'] = ''
        res = self.make_post_request(
            self.user_register_endpoint, self.test_user)
        self.assertEqual(res.status_code, 400)

    def test_api_can_register_user(self):
        res = self.make_post_request(
            self.user_register_endpoint, self.test_user)
        self.assertEqual(res.status_code, 201)

    def test_api_can_login_registered_user(self):
        # register user first
        user = User(name='solo', email='solo@yahoo.com')
        user.password = 'test'
        user.save()
        res = self.make_post_request(
            self.user_login_endpoint, {'email': 'solo@yahoo.com',
                                       'password': 'test'})
        self.assertEqual(res.status_code, 200)

    def test_api_cannot_login_unregistered_user(self):
        res = self.make_post_request(
            self.user_login_endpoint, self.test_login_user)
        self.assertEqual(res.status_code, 401)

    def test_token_returned_on_authenticating(self):
        user = User(name='solo', email='solo@yahoo.com')
        user.password = 'test'
        user.save()
        res = self.make_post_request(
            self.user_login_endpoint, {'email': 'solo@yahoo.com',
                                       'password': 'test'})
        self.assertEqual(res.status_code, 200)
        self.assertIn('token', str(res.data))

    def test_can_register_business(self):
        res = self.make_post_request(
            self.business_register_endpoint, self.test_business_user)
        self.assertEqual(res.status_code, 201)
