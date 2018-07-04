"""
This module contains tests for testing orders.
"""
import datetime
import json
from flask import current_app
from tests.base_test_case import ApiTestCase
from app.models import Order, Menu


class TestOrdersApiTestCase(ApiTestCase):
    """
     TestOrdersApiTestCase tests the orders api
    """

    def setUp(self):
        super(TestOrdersApiTestCase, self).setUp()
        self.customer_token, self.customer = self.login_test_user(
            'testorders@test.com')
        self.admin_token, self.admin = self.login_admin(
            'ordersadmin@test.com')

    def post_order(self, data):
        res = self.client().post(
            self.orders_endpoint,
            headers={
                'Authorization': self.customer_token,
                'Content-Type': 'application/json'
            },
            data=json.dumps(data)
        )
        return res

    def modify_order(self, id, data):
        res = self.modify_resource(
            self.orders_endpoint + '/{}'.format(id), self.customer_token, data)
        return res

    def test_only_admin_can_get_orders(self):
        """
        Test only an admin can order a meal
        """
        res = self.client().get(self.orders_endpoint, headers={
            'Authorization': self.customer_token
        })
        self.assertEqual(res.status_code, 403)

    def test_admin_can_get_orders(self):
        """
        Test an admin can get orders from their customers to their catering
        """
        res = self.client().get(self.orders_endpoint, headers={
            'Authorization': self.admin_token
        })
        self.assertEqual(res.status_code, 200)

    def test_authenticated_user_can_order_meal(self):
        """
        tests. authenicated user can order a meal
        """
        meal = self.add_test_meal(self.admin)
        menu_id = self.add_test_menu()

        res = self.post_order({'meals': [meal.id], 'orderCount': 1,
                               'menuId': menu_id})
        self.assertEqual(res.status_code, 201)

    def test_cannot_modify_non_existent_order(self):
        res = self.modify_resource(self.orders_endpoint + '/{}'.format(
            100), self.customer_token, {'meals': [1], 'orderCount': 1})
        self.assertEqual(res.status_code, 400)

    def test_user_can_modify_order(self):
        meal = self.add_test_meal(self.admin)
        meals = [meal]
        menu_id = self.add_test_menu()

        # create a test order to modify later
        order = Order(total_cost=1000, catering=self.admin.catering,
                      customer=self.customer, meals=meals, menu_id=menu_id)
        order.save()
        res = self.modify_resource(self.orders_endpoint + '/{}'.format(
            order.id), self.customer_token, {'meals': [meal.id], 'orderCount': 2})
        res_data = self.get_response_data(res)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(order.id, res_data['order']['id'])

    def test_user_cannot_modify_expired_order(self):
        token, user = self.login_test_user('testorders5@test.com')
        admin = self.login_admin('ordersadmin5@test.com')[1]
        meal = self.add_test_meal(admin)
        meals = [meal]

        # create a test order to modify later
        order = Order(total_cost=1000, catering=admin.catering,
                      customer=user, meals=meals)
        order.expires_at = datetime.datetime.now(
        ) - datetime.timedelta(minutes=current_app.config['ORDER_EXPIRES_IN'])
        order.save()
        res = self.modify_resource(self.orders_endpoint + '/{}'.format(
            order.id), self.customer_token, {'meals': [meal.id], 'orderCount': 1})
        self.assertEqual(res.status_code, 400)
        res_data = self.get_response_data(res)
        self.assertIn('message', res_data)

    def test_user_cannot_make_order_non_existent_meals(self):
        # create a test meal
        meals = [100, 300]
        menu_id = self.add_test_menu()
        res = self.post_order({'meals': meals, 'orderCount': 1,
                               'menuId': menu_id})
        res_data = self.get_response_data(res)
        self.assertEqual(res.status_code, 400)
        self.assertEqual('No meal exists with id: 100',
                         res_data['message'])

    def test_user_cannot_make_order_without_meals(self):
        meals = []
        menu_id = self.add_test_menu()
        res = self.post_order({'meals': meals, 'menuId': menu_id,
                               'orderCount': 1})
        res_data = self.get_response_data(res)
        self.assertEqual(res.status_code, 400)
        self.assertEqual('Missing required parameter in the JSON body or the post body or the query string',
                         res_data['errors']['meals'])

    def test_user_can_access_order(self):
        token = self.login_test_user('testorders8@test.com')[0]
        res = self.client().get(self.myorders_endpoint, headers={
            'Authorization': token,
            'Content-Type': 'application/json'
        })
        res_data = self.get_response_data(res)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(isinstance(res_data['orders'], list))

    def test_user_can_get_their_orders(self):
        token, user = self.login_test_user('testorders2@test.com')
        # create a meal by the admin
        admin = self.login_admin('ordersadmin1@test.com')[1]
        meal = self.add_test_meal(admin)
        menu_id = self.add_test_menu()
        menu = Menu.query.get(menu_id)

        order = Order(total_cost=meal.price, meals=[meal],
                      customer=user, catering=menu.catering, menu=menu,
                      order_count=2)
        order.save()

        res = self.client().get('/api/v1/orders/{0}'.format(order.id), headers={
            'Authorization': token
        })
        res_data = self.get_response_data(res)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_data['order']['id'], order.id)

    def test_user_cannot_get_non_existent_order(self):
        res = self.client().get('/api/v1/orders/{0}'.format(100), headers={
            'Authorization': self.customer_token
        })
        res_data = self.get_response_data(res)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res_data['message'],
                         'Order with such id 100 doesnot exist')
