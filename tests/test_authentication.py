from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from tests.base_test_case import ApiTestCase
from app.models import User


class AuthenticationTestCase(ApiTestCase):
    """
    Test for authentication endpoints
    """

    def set_empty_field(self, field):
        self.test_user[field] = ''
        res = self.make_post_request(
            '/api/v1/auth/signup', self.test_user)
        self.assertEqual(res.status_code, 400)
        data = self.get_response_data(res)
        self.assertIn('errors', data)

    def test_api_cannot_register_user_with_empty_email(self):
        self.set_empty_field('email')

    def test_api_cannot_register_user_with_empty_password(self):
        self.set_empty_field('password')

    def test_wrong_token_doesnot_authenticated(self):
        s = Serializer('-secret', expires_in=360000)
        token = s.dumps({
            'id': 'id'
        }).decode('ascii')

        res = self.client().get(self.meals_endpoint, headers={
            'Authorization': token
        })
        res_data = self.get_response_data(res)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(res_data['message'], 'Authorization failed try again')

    def test_api_can_register_user(self):
        res = self.make_post_request(
            '/api/v1/auth/signup', self.test_user)
        self.assertEqual(res.status_code, 201)

    def test_api_can_login_registered_user(self):
        # register user first
        user = User(name='solo', email='solo@yahoo.com', password='test')
        user.save()

        res = self.make_post_request(
            '/api/v1/auth/login', {'email': 'solo@yahoo.com',
                                   'password': 'test'})
        self.assertEqual(res.status_code, 200)
        data = self.get_response_data(res)
        self.assertIn('token', data)

    def test_api_cannot_login_unregistered_user(self):
        res = self.make_post_request(
            '/api/v1/auth/login', self.test_login_user)
        self.assertEqual(res.status_code, 401)
        data = self.get_response_data(res)
        self.assertEqual('Wrong username or password',
                         data['errors']['form'])

    def test_token_returned_on_authenticating(self):
        user = User(name='solo', email='solo1@yahoo.com', password='test')
        user.save()
        res = self.make_post_request(
            '/api/v1/auth/login', {'email': 'solo1@yahoo.com',
                                   'password': 'test'})
        self.assertEqual(res.status_code, 200)
        self.assertIn('token', str(res.data))

    def test_can_register_business(self):
        res = self.make_post_request(
            '/api/v1/auth/business/signup', {
                'email': 'biz@gmail.com',
                'name': 'your biz',
                'password': 'AwesomeBiz',
                'businessAddress': 'Kampala',
                'businessName': 'Cater1'
            })
        data = self.get_response_data(res)
        self.assertEqual(res.status_code, 201)
        self.assertEqual('biz@gmail.com', data['user']['email'])

    def test_cannot_register_with_invalid_email(self):
        res = self.make_post_request('/api/v1/auth/signup', data={
            'email': 'sdosdoso',
            'name': 'my name',
            'password': 'passwdsd'
        })
        self.assertEqual(res.status_code, 400)
        data = self.get_response_data(res)
        self.assertIn('errors', data)
