import datetime
import json
from tests.base_test_case import ApiTestCase
from app.models import Order, Meal
from flask import current_app
from app import db


class TestOrdersApiTestCase(ApiTestCase):
    def test_only_admin_can_get_orders(self):
        token = self.login_test_user('testorders1@test.com')[0]
        res = self.client().get(self.orders_endpoint, headers={
            'Authorization': token
        })
        self.assertEqual(res.status_code, 403)

    def test_admin_can_get_orders(self):
        token = self.login_admin('ordersadmin1@test.com')[0]
        res = self.client().get(self.orders_endpoint, headers={
            'Authorization': token
        })
        self.assertEqual(res.status_code, 200)

    def test_unauthenticated_user_cannot_order_meal(self):
        res = self.client().post(self.orders_endpoint, data={'meals': []})
        self.assertEqual(res.status_code, 401)

    def test_authenticated_user_can_order_meal(self):
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
        db.session.add(order)
        db.session.commit()

        res = self.client().put(
            self.orders_endpoint + '/{}'.format(order.id),
            headers={
                'Authorization': token,
                'Content-Type': 'application/json'
            },
            data=json.dumps({'meals': [meal.id], 'orderCount': 2})
        )
        self.assertEqual(res.status_code, 200)
        res_data = self.get_response_data(res)
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
        db.session.add(order)
        db.session.commit()

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
