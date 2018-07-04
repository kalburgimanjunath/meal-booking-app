"""
This module is the base test case for allm test cases.
"""
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
        self.meals_endpoint = '/api/v1/meals'
        self.menu_endpoint = '/api/v1/menu'
        self.orders_endpoint = '/api/v1/orders'
        self.myorders_endpoint = 'api/v1/myorders'
        self.get_menus_endpoint = 'api/v1/menus'
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
        self.test_admin_user = {
            'email': 'solo@gmail.com',
            'password': 'AwesomeAndela',
        }

    def make_post_request(self, endpoint, data, headers=None):
        """
        makes a post request
        """
        if headers is None:
            headers = {}
        res = self.client().post(
            endpoint, headers=headers, data=json.dumps(data),
            content_type='application/json')
        return res

    def modify_resource(self, endpoint, token, data):
        res = self.client().put(
            endpoint,
            headers={
                'Authorization': token,
                'Content-Type': 'application/json'
            },
            data=json.dumps(data)
        )
        return res

    def login_admin(self, email):
        """
        logins an admin test user
        """
        # use test admin_user
        role = Role.query.filter_by(name='Admin').first()
        u = User(name='admin', email=email,
                 password='admin', role=role)
        u.save()
        business = Catering(name='biz', address='kla', admin=u)
        business.save()
        response = self.make_post_request(
            '/api/v1/auth/login', {'email': email,
                                   'password': 'admin'})
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200)  # user successfully logins
        token = json_response.get('token')

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
            '/api/v1/auth/login', {'email': email,
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
        meal.save()
        meal2 = Meal(title='Beef with rice', price=1500,
                     description='lorem desc ipsum')
        meal2.save()

    def add_test_meal(self, user=None):
        """
        adds a test meal and returns id
        """
        meal = Meal(title='Beef with rice', price=1500,
                    description='lorem desc ipsum')
        if user:
            meal.catering = user.catering
        meal.save()
        return meal

    def add_test_menu(self):
        """
        add_test_menu. adds mock test menu
        """
        token, user = self.login_admin('admin_m1@test.com')
        meal = self.add_test_meal(user)
        menu = {
            "menu_date": "2018-04-26",
            "title": "Buffet ipsum",
            "description": "menu lorem ispum",
            "meals": [meal.id]
        }
        res = self.make_post_request(self.menu_endpoint, menu, headers={
            'Authorization': token,
            'Content-Type': 'application/json'
        })
        res_data = self.get_response_data(res)
        return res_data['id']

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
