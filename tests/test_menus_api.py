import unittest
from tests.base_test_case import ApiTestCase
from app.models import User, data


class TestMenusApiTestCase(ApiTestCase):
    """
    Tests for menus api endpoints
    """

    def test_unauthenticated_user_cannot_access_menu(self):
        res = self.client().get(self.menu_endpoint)
        self.assertEqual(res.status_code, 401)

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
        menu = {
            "menuDate": "2018-04-26",
            "title": "Buffet ipsum",
            "description": "menu lorem ispum",
            "meals": [meal.id for meal in data.meals]
        }
        res = self.client().post(
            self.menu_endpoint,
            headers={
                'Authorization': token
            },
            data=menu
        )
        self.assertEqual(res.status_code, 403)

    def test_unauthenticated_admin_cannot_set_menu(self):
        menu = {
            "menuDate": "2018-04-26",
            "title": "Buffet ipsum",
            "description": "menu lorem ispum",
            "meals": [meal.id for meal in data.meals]
        }
        res = self.client().post(self.menu_endpoint, data=menu)
        self.assertEqual(res.status_code, 401)

    def test_admin_can_set_menu(self):
        token = self.login_admin()
        menu = {
            "date": "2018-04-26",
            "title": "Buffet ipsum",
            "description": "menu lorem ispum",
            "meals": [meal.id for meal in data.meals]
        }
        res = self.client().post(
            self.menu_endpoint,
            headers={
                'Authorization': token
            },
            data=menu
        )
        self.assertEqual(res.status_code, 201)
