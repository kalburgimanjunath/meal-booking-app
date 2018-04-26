import unittest
import json
from tests import ApiTestCase
from app.models import User
import json


class TestMealsApiTestCase(ApiTestCase):
    """
     Tests for the admin meals api
    """

    def test_unauthenticated_admin_cannot_access_meals(self):
        res = self.client().get(self.meals_endpoint)
        self.assertEqual(res.status_code, 401)

    def test_only_admin_can_access_meals(self):
        # use test user
        token = self.login_test_user()
        res = self.client().get(self.meals_endpoint, headers={
            'Authorization': token})
        self.assertEqual(res.status_code, 403)

    def test_admin_can_access_meals(self):
        token = self.login_admin()

        res = self.client().get(self.meals_endpoint, headers={
            'Authorization': token})
        self.assertEqual(res.status_code, 200)

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

    def test_admin_can_edit_meal(self):
        token = self.login_admin()
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

    def test_admin_can_delete_meal(self):
        token = self.login_admin()
        res = self.client().delete(
            self.meals_endpoint + '/2',
            headers={
                'Authorization': token
            }
        )
        self.assertEqual(res.status_code, 200)

    def test_admin_cannot_delete_that_doesnot_exist(self):
        token = self.login_admin()
        res = self.client().delete(
            self.meals_endpoint + '/4',
            headers={
                'Authorization': token
            }
        )
        self.assertEqual(res.status_code, 400)

    def test_admin_cannot_edit_meal_that_doesnot_exist(self):
        token = self.login_admin()
        res = self.client().put(
            self.meals_endpoint + '/4',
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
