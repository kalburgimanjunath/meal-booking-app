import unittest
from tests.base_test_case import ApiTestCase
from app.models import User, data
import json


class TestMenusApiTestCase(ApiTestCase):
    """
    Tests for menus api endpoints
    """

    def test_unauthenticated_user_cannot_access_menu(self):
        res = self.client().get(self.menu_endpoint)
        self.assertEqual(res.status_code, 401)
        res_data = self.get_response_data(res)
        self.assertIn('error', res_data)

    def test_authenticated_user_can_access_menu(self):
        token = self.login_test_user()
        res = self.client().get(
            self.menu_endpoint,
            headers={
                'Authorization': token
            }
        )
        self.assertEqual(res.status_code, 200)

    def test_authenticated_user_cannot_set_menu(self):
        token = self.login_test_user()
        self.add_mock_meals()
        menu = {
            "date": "2018-04-26",
            "title": "Buffet ipsum",
            "description": "menu lorem ispum",
            "meals": [meal.id for meal in data.meals]
        }
        res = self.client().post(
            self.menu_endpoint,
            headers={
                'Authorization': token,
                'Content-Type': 'application/json'
            },
            data=json.dumps(menu)
        )
        self.assertEqual(res.status_code, 403)
        res_data = self.get_response_data(res)
        self.assertEqual('403 forbidden access is denied', res_data['error'])

    def test_unauthenticated_admin_cannot_set_menu(self):
        self.add_mock_meals()
        menu = {
            "date": "2018-04-26",
            "title": "Buffet ipsum",
            "description": "menu lorem ispum",
            "meals": [meal.id for meal in data.meals]
        }
        res = self.client().post(self.menu_endpoint, data=json.dumps(menu))
        self.assertEqual(res.status_code, 401)
        res_data = self.get_response_data(res)
        self.assertEqual(
            'No Bearer token in Authorisation header', res_data['error'])

    def test_admin_can_set_menu(self):
        token = self.login_admin()
        self.add_mock_meals()
        menu = {
            "date": "2018-04-26",
            "title": "Buffet ipsum",
            "description": "menu lorem ispum",
            "meals": [meal.id for meal in data.meals]
        }
        res = self.client().post(
            self.menu_endpoint,
            headers={
                'Authorization': token,
                'Content-Type': 'application/json'
            },
            data=json.dumps(menu)
        )

        self.assertEqual(res.status_code, 201)
        res_data = self.get_response_data(res)
        self.assertIn('id', res_data)

    def test_admin_cannot_set_menu_withoutmeals(self):
        token = self.login_admin()
        menu = {
            "date": "2018-04-26",
            "title": "Buffet ipsum",
            "description": "menu lorem ispum",
            "meals": []
        }
        res = self.client().post(
            self.menu_endpoint,
            headers={
                'Authorization': token,
                'Content-Type': 'application/json'
            },
            data=json.dumps(menu)
        )

        self.assertEqual(res.status_code, 400)
        res_data = self.get_response_data(res)
        self.assertIn('errors', res_data)

    def test_admin_cannot_set_menu_with_wrong_date_format(self):
        token = self.login_admin()
        menu = {
            "date": "06-05-2018",
            "title": "Buffet ipsum",
            "description": "menu lorem ispum",
            "meals": [1, 2]
        }
        res = self.client().post(
            self.menu_endpoint,
            headers={
                'Authorization': token,
                'Content-Type': 'application/json'
            },
            data=json.dumps(menu)
        )

        self.assertEqual(res.status_code, 400)
        res_data = self.get_response_data(res)
        self.assertIn('errors', res_data)

    def test_admin_cannot_set_menu_with_empty_fields(self):
        token = self.login_admin()
        menu = {}
        res = self.client().post(
            self.menu_endpoint,
            headers={
                'Authorization': token,
                'Content-Type': 'application/json'
            },
            data=json.dumps(menu)
        )

        self.assertEqual(res.status_code, 400)
        res_data = self.get_response_data(res)
        self.assertIn('errors', res_data)
