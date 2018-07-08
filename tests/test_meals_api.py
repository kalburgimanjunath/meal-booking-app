import json
from tests.base_test_case import ApiTestCase
from app.models import Meal


class TestMealsApiTestCase(ApiTestCase):
    """
     Tests for the admin meals api
    """

    def setUp(self):
        super().setUp()
        self.admin_token, self.admin = self.login_admin('s@admin.com')
        self.user_token, self.customer_user = self.login_test_user(
            'self@tesst.com')
        self.meal = Meal(title='lorem ipsum', price=2000,
                         description='lorem ipsum', catering=self.admin.catering)
        self.meal.save()

    def post_meal(self, token):
        res = self.client().post(
            self.meals_endpoint,
            headers={
                'Authorization': token,
                'Content-Type': 'application/json'
            },
            data=json.dumps({
                'title': 'Beef with matooke',
                'price': 10000,
                'description': 'lorem ispunm'
            })
        )
        return res

    def test_unauthenticated_admin_cannot_access_meals(self):
        res = self.client().get(self.meals_endpoint)
        self.assertEqual(res.status_code, 401)
        data = self.get_response_data(res)
        self.assertEqual(
            'No Bearer token in Authorisation header', data['message'])

    def test_only_admin_can_access_meals(self):
        res = self.client().get(self.meals_endpoint, headers={
            'Authorization': self.user_token})
        self.assertEqual(res.status_code, 403)
        data = self.get_response_data(res)
        self.assertEqual('403 forbidden access is denied', data['message'])

    def test_admin_can_access_meals(self):
        res = self.client().get(self.meals_endpoint, headers={
            'Authorization': self.admin_token})
        self.assertEqual(res.status_code, 200)
        data = self.get_response_data(res)
        self.assertIn('meals', data)

    def test_customer_cannot_post_meals(self):
        res = self.post_meal(self.user_token)
        self.assertEqual(res.status_code, 403)
        data = self.get_response_data(res)
        self.assertEqual('403 forbidden access is denied', data['message'])

    def test_admin_can_post_meal(self):
        res = self.post_meal(self.admin_token)
        data = self.get_response_data(res)

        self.assertEqual(res.status_code, 201)
        self.assertIn('id', data)

    def test_admin_can_edit_meal(self):
        res = self.modify_resource(
            self.meals_endpoint + '/{}'.format(self.meal.id),
            self.admin_token,
            {
                'title': 'meal option121',
                'price': 10000,
                'description': 'lorem ispum'
            })

        data = self.get_response_data(res)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(1, data['id'])

    def test_admin_can_delete_meal(self):
        res = self.client().delete(
            self.meals_endpoint + '/{}'.format(self.meal.id),
            headers={
                'Authorization': self.admin_token
            }
        )
        self.assertEqual(res.status_code, 200)
        data = self.get_response_data(res)
        self.assertIn('message', data)

    def test_admin_cannot_delete_meal_that_doesnot_exist(self):
        res = self.client().delete(
            self.meals_endpoint + '/200',
            headers={
                'Authorization': self.admin_token
            }
        )
        self.assertEqual(res.status_code, 400)
        data = self.get_response_data(res)
        self.assertEqual('No meal with such id 200 exists', data['message'])

    def test_admin_cannot_edit_meal_that_doesnot_exist(self):
        res = self.modify_resource(self.meals_endpoint + '/{}'.format(10000), self.admin_token, {
            'title': 'meal detail',
            'price': 10000,
            'description': 'desc'
        })
        self.assertEqual(res.status_code, 400)
        data = self.get_response_data(res)
        self.assertEqual('No meal with such id 10000 exists', data['message'])

    def test_admin_can_get_meal(self):
        """
        tests an admin can get a meal
        """
        meal = self.add_test_meal(self.admin)
        endpoint = self.meals_endpoint + '/{0}'.format(meal.id)
        res = self.client().get(endpoint, headers={
            'Authorization': self.admin_token
        })
        res_data = self.get_response_data(res)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_data['id'], meal.id)

    def test_admin_cannot_get_nonexistent_meal(self):
        """
        tests an admin cannot get non-existent meal
        """
        endpoint = self.meals_endpoint + '/1000'
        res = self.client().get(endpoint, headers={
            'Authorization': self.admin_token
        })
        res_data = self.get_response_data(res)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(
            res_data['message'], 'No meal with such id 1000 exists')
