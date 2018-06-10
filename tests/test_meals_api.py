from tests.base_test_case import ApiTestCase
from app.models import Meal, User


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
        token = self.login_test_user('test@testapi.com')[0]
        res = self.client().get(self.meals_endpoint, headers={
            'Authorization': token})
        self.assertEqual(res.status_code, 403)
        data = self.get_response_data(res)
        self.assertEqual('403 forbidden access is denied', data['error'])

    def test_admin_can_access_meals(self):
        token = self.login_admin('s@admin.com')[0]

        res = self.client().get(self.meals_endpoint, headers={
            'Authorization': token})
        self.assertEqual(res.status_code, 200)
        data = self.get_response_data(res)
        self.assertIn('meals', data)

    def test_customer_cannot_post_meals(self):
        token = self.login_test_user('self@tesst.com')[0]
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
        token = self.login_admin('self@admin.com')[0]
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
        data = self.get_response_data(res)
        self.assertEqual(res.status_code, 201)
        self.assertIn('id', data)

    def test_admin_can_edit_meal(self):
        token, user = self.login_admin('adm@adm.com')

        meal = Meal(title='lorem ipsum', price=2000,
                    description='lorem ipsum', catering=user.catering)
        meal.save()
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
        token, user = self.login_admin('self@ad.com')

        meal = Meal(title='lorem ipsum', price=2000,
                    description='lorem ipsum', catering=user.catering)
        meal.save()

        res = self.client().delete(
            self.meals_endpoint + '/{}'.format(meal.id),
            headers={
                'Authorization': token
            }
        )
        self.assertEqual(res.status_code, 200)
        data = self.get_response_data(res)
        self.assertIn('message', data)

    def test_customer_cannot_delete_meal(self):
        token = self.login_test_user('test@self.com')[0]
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
        token = self.login_admin('admin@a.com')[0]
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
        token = self.login_admin('admin@catering.com')[0]
        res = self.client().put(
            self.meals_endpoint + '/10000',
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
