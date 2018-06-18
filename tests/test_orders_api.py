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

    def test_only_admin_can_get_orders(self):
        """
        Test only an admin can order a meal
        """
        token = self.login_test_user('testorders1@test.com')[0]
        res = self.client().get(self.orders_endpoint, headers={
            'Authorization': token
        })
        self.assertEqual(res.status_code, 403)

    def test_admin_can_get_orders(self):
        """
        Test an admin can get orders from their customers to their catering
        """
        token = self.login_admin('ordersadmin1@test.com')[0]
        res = self.client().get(self.orders_endpoint, headers={
            'Authorization': token
        })
        self.assertEqual(res.status_code, 200)

    def test_unauthenticated_user_cannot_order_meal(self):
        """
        Test unathenticated user cannot order for a meal
        """
        res = self.client().post(self.orders_endpoint, data={'meals': []})
        self.assertEqual(res.status_code, 401)

    def test_authenticated_user_can_order_meal(self):
        """
        tests. authenicated user can order a meal
        """
        token = self.login_test_user('testorders2@test.com')[0]
        # create a meal by the admin
        admin = self.login_admin('ordersadmin1@test.com')[1]
        meal = self.add_test_meal(admin)
        menu_id = self.add_test_menu()

        res = self.client().post(
            self.orders_endpoint,
            headers={
                'Authorization': token,
                'Content-Type': 'application/json'
            },
            data=json.dumps(
                {'meals': [meal.id], 'cateringId': admin.catering.id,
                 'menuId': menu_id})
        )
        self.assertEqual(res.status_code, 201)

    def test_cannot_modify_non_existent_order(self):
        token = self.login_test_user('testorders3@test.com')[0]
        meals = [1]
        res = self.client().put(
            self.orders_endpoint + '/100',
            headers={
                'Authorization': token,
                'Content-Type': 'application/json'
            },
            data=json.dumps({'meals': meals})
        )
        self.assertEqual(res.status_code, 400)

    def test_user_can_modify_order(self):
        token, user = self.login_test_user('testorders4@test.com')
        admin = self.login_admin('ordersadmin4@test.com')[1]
        meal = self.add_test_meal(admin)
        meals = [meal]
        menu_id = self.add_test_menu()

        # create a test order to modify later
        order = Order(total_cost=1000, catering=admin.catering,
                      customer=user, meals=meals, menu_id=menu_id)
        order.save()

        res = self.client().put(
            self.orders_endpoint + '/{}'.format(order.id),
            headers={
                'Authorization': token,
                'Content-Type': 'application/json'
            },
            data=json.dumps({'meals': [meal.id], 'orderCount': 2})
        )
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

        res = self.client().put(
            self.orders_endpoint + '/{}'.format(order.id),
            headers={
                'Authorization': token,
                'Content-Type': 'application/json'
            },
            data=json.dumps({'meals': [meal.id]})
        )
        self.assertEqual(res.status_code, 400)
        res_data = self.get_response_data(res)
        self.assertIn('error', res_data)

    def test_user_cannot_make_order_non_existent_meals(self):
        token = self.login_test_user('testorders6@test.com')[0]
        admin = self.login_admin('ordersadmin@test.com')[1]
        # create a test meal
        meals = [100, 300]

        menu_id = self.add_test_menu()

        res = self.client().post(
            self.orders_endpoint,
            headers={
                'Authorization': token,
                'Content-Type': 'application/json'
            },
            data=json.dumps(
                {'meals': meals, 'cateringId': admin.catering.id,
                 'menuId': menu_id})
        )
        res_data = self.get_response_data(res)
        self.assertEqual(res.status_code, 400)
        self.assertEqual('No meal exists with id: 100',
                         res_data['errors']['meals'])

    def test_user_cannot_make_order_without_meals(self):
        token = self.login_test_user('testorders7@test.com')[0]
        admin = self.login_admin('ordersadmin@test.com')[1]
        meals = []

        menu_id = self.add_test_menu()

        res = self.client().post(
            self.orders_endpoint,
            headers={
                'Authorization': token,
                'Content-Type': 'application/json'
            },
            data=json.dumps({'meals': meals, 'menuId': menu_id,
                             'cateringId': admin.catering.id})
        )
        res_data = self.get_response_data(res)
        self.assertEqual(res.status_code, 400)
        self.assertEqual('List of meals cannot be empty',
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
        token = self.login_test_user('testorders2@test.com')[0]

        res = self.client().get('/api/v1/orders/{0}'.format(100), headers={
            'Authorization': token
        })
        res_data = self.get_response_data(res)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res_data['error'],
                         'Order with such id 100 doesnot exist')
