import unittest
import flask
from app import create_application


class ApiTestCase(unittest.TestCase):

    def Setup(self):
        self.app = create_application('testing')
        self.app_context = self.app.app_context()
        self.client = self.app.test_client
        self.app_context.push()

        self.base_url = '/api/v1'
        self.user_register_endpoint = '/auth/signup'
        self.user_login_endpoint = '/auth/signup'
        self.business_register_endpoint = '/auth/business/signup'

        self.test_user = {
            'email': 'solo.nsubuga@andela.com',
            'name': 'Solomon Nsubuga',
            'password': 'AwesomeAndela'
        }

        self.test_user_login = {
            'email': 'solo.nsubuga@andela.com',
            'password': 'AwesomeAndela'
        }

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

    def tearDown(self):
        self.app_context.pop()
