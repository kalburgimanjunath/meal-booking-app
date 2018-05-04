import unittest
from tests.base_test_case import ApiTestCase
from app.models import data, Order
import datetime
import json
from flask import current_app


class TestOrdersApiTestCase(ApiTestCase):
    def test_only_admin_can_get_orders(self):
        token = self.login_test_user()
        res = self.client().get(self.orders_endpoint, headers={
            'Authorization': token
        })
        self.assertEqual(res.status_code, 403)

    def test_admin_can_get_orders(self):
        token = self.login_admin()
        res = self.client().get(self.orders_endpoint, headers={
            'Authorization': token
        })
        self.assertEqual(res.status_code, 200)

    def test_unauthenticated_user_cannot_order_meal(self):
        meals = [meal.id for meal in data.meals]
        res = self.client().post(self.orders_endpoint, data={'meals': meals})
        self.assertEqual(res.status_code, 401)

    def test_authenticated_user_can_order_meal(self):
        token = self.login_test_user()
        meals = [meal.id for meal in data.meals]
        res = self.client().post(
            self.orders_endpoint,
            headers={
                'Authorization': token,
                'Content-Type': 'application/json'
            },
            data=json.dumps({'meals': meals})
        )
        self.assertEqual(res.status_code, 201)

    def test_cannot_modify_non_existent_order(self):
        token = self.login_test_user()
        meals = [meal.id for meal in data.meals]
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
        token = self.login_test_user()
        meals = [meal.id for meal in data.meals]

        # create an order
        order = Order()
        order.total_cost = 10000
        order.meals = data.meals
        order.save()

        res = self.client().put(
            self.orders_endpoint + '/{}'.format(order.id),
            headers={
                'Authorization': token,
                'Content-Type': 'application/json'
            },
            data=json.dumps({'meals': meals})
        )

        self.assertEqual(res.status_code, 200)

    def test_user_cannot_modify_expired_order(self):
        token = self.login_test_user()
        # create a test meal

        self.add_mock_meals()

        meals = [meal.id for meal in data.meals]
        # create an order
        order = Order()
        order.total_cost = 10000
        order.meals = data.meals
        order.expires_at = datetime.datetime.now(
        ) - datetime.timedelta(minutes=current_app.config['ORDER_EXPIRES_IN'])
        order.save()

        res = self.client().put(
            self.orders_endpoint + '/{}'.format(order.id),
            headers={
                'Authorization': token,
                'Content-Type': 'application/json'
            },
            data=json.dumps({'meals': meals})
        )
        self.assertEqual(res.status_code, 400)
