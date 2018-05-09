import json
import unittest
from app import create_application, db
from app.models import User, Meal, Role, Catering


class ApiTestCase(unittest.TestCase):
    """
    Base class for creating unit tests
    """

    def setUp(self):
        self.app = create_application('testing')
        self.app_context = self.app.app_context()
        self.client = self.app.test_client
        self.app_context.push()
        db.create_all()
        Role.insert_roles()

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
            'email': 'solo.nsubuga@andela.com',
            'password': 'AwesomeAndela'
        }

        self.user = User(name='solo', email='solo@gmail.com',
                         password='test')

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
        """
        makes a post request
        """
        res = self.client().post(
            endpoint, data=json.dumps(data),
            content_type='application/json')
        return res

    def login_admin(self, email):
        """
        logins an admin test user
        """
        # use test admin_user
        role = Role.query.filter_by(name='Admin').first()
        u = User(name='admin', email=email,
                 password='admin', role=role)
        db.session.add(u)
        db.session.commit()
        business = Catering(name='biz', address='kla', admin=u)
        db.session.add(business)
        db.session.commit()
        response = self.make_post_request(
            self.user_login_endpoint, {'email': email,
                                       'password': 'admin'})
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)  # user successfully logins
        token = json_response.get('token')
        # token = 'Bearer ' + token

        self.assertIsNotNone(token)  # verify that we have the token
        return token, u

    def login_test_user(self, email):
        """
        logins a test user
        """
        user = User(name='test', email=email, password='test')
        db.session.add(user)
        db.session.commit()
        response = self.make_post_request(
            self.user_login_endpoint, {'email': email,
                                       'password': 'test'})
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)  # user successfully logins
        token = json_response.get('token')

        self.assertIsNotNone(token)  # verify that we have the token
        return token, user

    def add_mock_meals(self):
        """
        adds mock meals
        """
        meal = Meal(title='lorem meal', price=10000,
                    description='lorem ipsum desc')
        db.session.add(meal)
        meal2 = Meal(title='Beef with rice', price=1500,
                     description='lorem desc ipsum')
        db.session.add(meal2)
        db.session.commit()

    def add_test_meal(self, user=None):
        """
        adds a test meal and returns id
        """
        meal = Meal(title='Beef with rice', price=1500,
                    description='lorem desc ipsum')
        if user:
            meal.catering = user.catering
        db.session.add(meal)
        db.session.commit()
        return meal

    def get_response_data(self, response):
        """
        gets request response json data
        """
        json_response = json.loads(response.get_data(as_text=True))
        return json_response

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
