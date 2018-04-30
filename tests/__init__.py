import unittest
from app import create_application
from app.models import User
import json


class ApiTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_application('testing')
        self.app_context = self.app.app_context()
        self.client = self.app.test_client
        self.app_context.push()

        self.user_register_endpoint = '/api/v1/auth/signup'
        self.user_login_endpoint = '/api/v1/auth/login'
        self.business_register_endpoint = '/api/v1/auth/business/signup'
        self.meals_endpoint = '/api/v1/meals'
        self.menu_endpoint = '/api/v1/menu'
        self.orders_endpoint = '/api/v1/orders'

        self.test_user = {
            'email': 'solo@andela.com',
            'name': 'Solomon Nsubuga',
            'password': 'AwesomeAndela'
        }

        self.test_login_user = {
            'username': 'solo.nsubuga@andela.com',
            'password': 'AwesomeAndela'
        }

        self.user = User('solo', 'solo@gmail.com')

        self.test_business_user = {
            'email': 'solo@gmail.com',
            'name': 'Solo Dev',
            'password': 'AwesomeAndela',
            'businessAddress': 'Kampala',
            'businessName': 'Cater1'
        }

        self.test_admin_user = {
            'email': 'solo@gmail.com',
            'password': 'AwesomeAndela',
        }

    def make_post_request(self, endpoint, data):
        res = self.client().post(
            endpoint, data=json.dumps(data),
            content_type='application/json')
        return res

    def login_admin(self):
        # use test admin_user
        response = self.make_post_request(
            self.user_login_endpoint, {'username': 'admin@admin.com',
                                       'password': 'admin'})
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)  # user successfully logins
        token = json_response.get('token')
        # token = 'Bearer ' + token

        self.assertIsNotNone(token)  # verify that we have the token
        return token

    def login_test_user(self):
        response = self.make_post_request(
            self.user_login_endpoint, {'username': 'test@test.com',
                                       'password': 'test'})
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)  # user successfully logins
        token = json_response.get('token')
        # token = 'Bearer ' + token

        self.assertIsNotNone(token)  # verify that we have the token
        return token

    def tearDown(self):
        self.app_context.pop()
