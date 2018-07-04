import json
from tests.base_test_case import ApiTestCase


class TestMenusApiTestCase(ApiTestCase):
    """
    Tests for menus api endpoints
    """

    def setUp(self):
        super(TestMenusApiTestCase, self).setUp()
        self.admin_token, self.admin = self.login_admin('admin_m1@test.com')
        self.customer_token, self.customer = self.login_test_user(
            'testm1@test.com')
        self.meal = self.add_test_meal(self.admin)
        self.menu = {
            "menu_date": "2018-04-26",
            "title": "Buffet ipsum",
            "description": "menu lorem ispum",
            "meals": [self.meal.id]
        }

    def post_menu(self, token):
        res = self.client().post(
            self.menu_endpoint,
            headers={
                'Authorization': token,
                'Content-Type': 'application/json'
            },
            data=json.dumps(self.menu)
        )
        return res

    def test_authenticated_user_can_access_menu(self):
        """
        tests unauthenticated user can access menus
        """
        res = self.client().get(
            self.menu_endpoint,
            headers={
                'Authorization': self.customer_token
            }
        )
        self.assertEqual(res.status_code, 200)

    def test_authenticated_user_cannot_set_menu(self):
        res = self.post_menu(self.customer_token)
        self.assertEqual(res.status_code, 403)
        res_data = self.get_response_data(res)
        self.assertEqual('403 forbidden access is denied', res_data['message'])

    def test_admin_can_set_menu(self):
        res = self.post_menu(self.admin_token)
        self.assertEqual(res.status_code, 201)
        res_data = self.get_response_data(res)
        self.assertIn('id', res_data)

    def test_admin_cannot_set_menu_withoutmeals(self):
        self.menu['meals'] = []
        res = self.post_menu(self.admin_token)
        self.assertEqual(res.status_code, 400)
        res_data = self.get_response_data(res)
        self.assertIn('errors', res_data)

    def test_admin_cannot_set_menu_with_wrong_date_format(self):
        # give menu wrong date
        self.menu['menu_date'] = "06-05-2018"
        res = self.post_menu(self.admin_token)
        self.assertEqual(res.status_code, 400)
        res_data = self.get_response_data(res)
        self.assertIn('errors', res_data)

    def test_admin_cannot_set_menu_with_empty_fields(self):
        self.menu = {}
        res = self.post_menu(self.admin_token)
        self.assertEqual(res.status_code, 400)
        res_data = self.get_response_data(res)
        self.assertIn('errors', res_data)

    def test_admin_can_delete_menu(self):
        """
        test menu deletion
        """
        token = self.login_admin('admin_m1@test.com')[0]
        menu_id = self.add_test_menu()
        endpoint = '/api/v1/menu/{0}'.format(menu_id)
        res = self.client().delete(endpoint, headers={
            'Authorization': token
        })
        self.assertEqual(res.status_code, 200)
        res_data = self.get_response_data(res)
        self.assertIn('status', res_data)

    def test_admin_can_edit_menu(self):
        """
        tests an admin can edit their menu
        """
        menu_id = self.add_test_menu()
        endpoint = '/api/v1/menu/{0}'.format(menu_id)
        res = self.modify_resource(endpoint, self.admin_token, self.menu)
        res_data = self.get_response_data(res)
        self.assertEqual(res.status_code, 200)
        self.assertIn('id', res_data)

    def test_can_edit_menu_meals_only(self):
        """
        tests modification of meals only on a menu
        """
        menu_id = self.add_test_menu()
        endpoint = '/api/v1/menu/{0}'.format(menu_id)
        meal = self.add_test_meal(self.admin)
        self.menu['meals'] = [meal.id]
        res = self.modify_resource(endpoint, self.admin_token, self.menu)
        res_data = self.get_response_data(res)
        self.assertEqual(res.status_code, 200)
        self.assertIn('id', res_data)

    def test_can_get_menus(self):
        """
        tests. admin can get menus
        """
        token = self.login_admin('admin_m1@test.com')[0]
        res = self.client().get(self.get_menus_endpoint, headers={
            'Authorization': token
        })
        res_data = self.get_response_data(res)
        self.assertEqual(res.status_code, 200)
        self.assertIsInstance(res_data['menus'], list)

    def test_cannot_delete_nonexistent_menu(self):
        """
        tests cannot delete menu that doesnot exists
        """
        token = self.login_admin('admin_m1@test.com')[0]
        endpoint = '/api/v1/menu/10000'  # create endpoint with non-existent menu id
        res = self.client().delete(endpoint, headers={
            'Authorization': token
        })
        res_data = self.get_response_data(res)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res_data['message'],
                         'Menu with id 10000 doesnot exist')

    def test_can_get_a_menu(self):
        menu_id = self.add_test_menu()
        endpoint = '/api/v1/menu/{0}'.format(menu_id)
        token = self.login_admin('admin_m1@test.com')[0]
        res = self.client().get(endpoint, headers={
            'Authorization': token
        })
        res_data = self.get_response_data(res)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_data['menu']['id'], menu_id)

    def test_cannot_get_nonexistent_menu(self):
        menu_id = 1000
        endpoint = '/api/v1/menu/{0}'.format(menu_id)
        token = self.login_admin('admin_m1@test.com')[0]
        res = self.client().get(endpoint, headers={
            'Authorization': token
        })
        res_data = self.get_response_data(res)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res_data['message'],
                         'Requested menu with id 1000 does not exist')

    def test_admin_cannot_modify_menu_without_fields(self):
        """
        tests an admin can edit their menu
        """
        menu_id = self.add_test_menu()
        endpoint = '/api/v1/menu/{0}'.format(menu_id)
        res = self.modify_resource(endpoint, self.admin_token, {})
        res_data = self.get_response_data(res)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res_data['message'],
                         'No field(s) specified to be modified')
