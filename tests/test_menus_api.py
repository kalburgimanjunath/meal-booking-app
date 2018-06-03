import json
from tests.base_test_case import ApiTestCase
from app.models import User, Meal


class TestMenusApiTestCase(ApiTestCase):
    """
    Tests for menus api endpoints
    """

    # def test_unauthenticated_user_cannot_access_menu(self):
    #     res = self.client().get(self.menu_endpoint)
    #     self.assertEqual(res.status_code, 401)
    #     res_data = self.get_response_data(res)
    #     self.assertIn('error', res_data)

    def test_authenticated_user_can_access_menu(self):
        token = self.login_test_user('test_menu@test.com')[0]
        res = self.client().get(
            self.menu_endpoint,
            headers={
                'Authorization': token
            }
        )
        self.assertEqual(res.status_code, 200)

    def test_authenticated_user_cannot_set_menu(self):
        token = self.login_test_user('testm1@test.com')[0]
        meal = self.add_test_meal()
        menu = {
            "date": "2018-04-26",
            "title": "Buffet ipsum",
            "description": "menu lorem ispum",
            "meals": [meal.id]
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
        meal = self.add_test_meal()
        menu = {
            "date": "2018-04-26",
            "title": "Buffet ipsum",
            "description": "menu lorem ispum",
            "meals": [meal.id]
        }
        res = self.client().post(self.menu_endpoint, data=json.dumps(menu))
        self.assertEqual(res.status_code, 401)
        res_data = self.get_response_data(res)
        self.assertEqual(
            'No Bearer token in Authorisation header', res_data['error'])

    def test_admin_can_set_menu(self):
        token, user = self.login_admin('admin_m1@test.com')
        meal = self.add_test_meal(user)
        menu = {
            "date": "2018-04-26",
            "title": "Buffet ipsum",
            "description": "menu lorem ispum",
            "meals": [meal.id]
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
        token = self.login_admin('adminm2@admin.com')[0]
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
        token, user = self.login_admin('test_ad3@admin.com')
        meal = self.add_test_meal(user)
        menu = {
            "date": "06-05-2018",
            "title": "Buffet ipsum",
            "description": "menu lorem ispum",
            "meals": [meal.id]
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
        token = self.login_admin('admin_test2@admin.com')[0]
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
