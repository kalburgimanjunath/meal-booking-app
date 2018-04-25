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

    def tearDown(self):
        self.app_context.pop()
