import unittest
from tests.base_test_case import ApiTestCase
from app.models import User


class TestMealsApiTestCase(ApiTestCase):
    """
     Tests for the admin meals api
    """

    def test_unauthenticated_admin_cannot_access_meals(self):
        res = self.client().get(self.meals_endpoint)
        self.assertEqual(res.status_code, 401)
        data = self.get_response_data(res)
        self.assertEqual(
            'No Bearer token in Authorisation header', data['error'])

    def test_only_admin_can_access_meals(self):
        # use test user
        token = self.login_test_user()
        res = self.client().get(self.meals_endpoint, headers={
            'Authorization': token})
        self.assertEqual(res.status_code, 403)
        data = self.get_response_data(res)
        self.assertEqual('403 forbidden access is denied', data['error'])

    def test_admin_can_access_meals(self):
        token = self.login_admin()

        res = self.client().get(self.meals_endpoint, headers={
            'Authorization': token})
        self.assertEqual(res.status_code, 200)
        data = self.get_response_data(res)
        self.assertIn('meals', data)

    def test_customer_cannot_post_meals(self):
        token = self.login_test_user()
        res = self.client().post(
            self.meals_endpoint,
            headers={
                'Authorization': token
            },
            data={
                'title': 'Beef with posho',
                'price': 1000,
                'description': 'lorem ispunm'
            }
        )
        self.assertEqual(res.status_code, 403)
        data = self.get_response_data(res)
        self.assertEqual('403 forbidden access is denied', data['error'])

    def test_admin_can_post_meal(self):
        token = self.login_admin()
        res = self.client().post(
            self.meals_endpoint,
            headers={
                'Authorization': token
            },
            data={
                'title': 'Beef with matooke',
                'price': 10000,
                'description': 'lorem ispunm'
            }
        )

        self.assertEqual(res.status_code, 201)
        data = self.get_response_data(res)
        self.assertIn('id', data)

    def test_admin_can_edit_meal(self):
        token = self.login_admin()
        self.add_mock_meals()
        res = self.client().put(
            self.meals_endpoint + '/1',
            headers={
                'Authorization': token
            },
            data={
                'title': 'meal option121',
                'price': 10000,
                'description': 'lorem ispum'
            }
        )
        self.assertEqual(res.status_code, 200)
        data = self.get_response_data(res)
        self.assertEqual(1, data['id'])

    def test_admin_can_delete_meal(self):
        token = self.login_admin()
        self.add_mock_meals()
        res = self.client().delete(
            self.meals_endpoint + '/2',
            headers={
                'Authorization': token
            }
        )
        self.assertEqual(res.status_code, 200)
        data = self.get_response_data(res)
        self.assertIn('message', data)

    def test_customer_cannot_delete_meal(self):
        token = self.login_test_user()
        res = self.client().delete(
            self.meals_endpoint + '/2',
            headers={
                'Authorization': token
            }
        )
        self.assertEqual(res.status_code, 403)
        data = self.get_response_data(res)
        self.assertEqual('403 forbidden access is denied', data['error'])

    def test_admin_cannot_delete_that_doesnot_exist(self):
        token = self.login_admin()
        res = self.client().delete(
            self.meals_endpoint + '/200',
            headers={
                'Authorization': token
            }
        )
        self.assertEqual(res.status_code, 400)
        data = self.get_response_data(res)
        self.assertIn('error', data)

    def test_admin_cannot_edit_meal_that_doesnot_exist(self):
        token = self.login_admin()
        res = self.client().put(
            self.meals_endpoint + '/200',
            headers={
                'Authorization': token
            },
            data={
                'title': 'meal option121',
                'price': 10000,
                'description': 'lorem ispum'
            }
        )

        self.assertEqual(res.status_code, 400)
        data = self.get_response_data(res)
        self.assertIn('error', data)
