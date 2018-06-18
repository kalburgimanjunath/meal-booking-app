"""
Module for testing util functions
"""
from app.api_1_0.common import validate_date, validate_email_type, \
    is_list, price_type, str_type, menu_date_type, type_menu_id
from tests.base_test_case import ApiTestCase


class UtilsTestCase(ApiTestCase):
    """
    Tests for the user model object
    """

    def test_validate_email(self):
        """
        tests email validation
        """
        email = 'solo@gmail.com'
        is_valid = validate_email_type(email)
        self.assertTrue(is_valid)

        is_not_valid = validate_email_type('solo@')
        self.assertFalse(is_not_valid)

    def test_validate_date_format(self):
        """
        tests date format validation
        """
        is_valid = validate_date('2018-05-05')
        self.assertTrue(is_valid)
        is_not_valid = validate_date('05-05-2018')
        self.assertFalse(is_not_valid)

    def test_is_list(self):
        """
        tests the is_list func
        """
        is_valid = is_list([])
        self.assertTrue(is_valid)

        is_invalid = is_list('str not list')
        self.assertFalse(is_invalid)

    def test_is_price_type(self):
        """
        tests meal price_type
        """
        price = 100
        val = price_type(price)
        self.assertEqual(price, val)

        with self.assertRaises(ValueError) as ctx:
            price = ""
            price_type(price)
        self.assertEqual('Price value must be a integer',
                         str(ctx.exception))

        with self.assertRaises(ValueError) as ctx:
            price = -1
            price_type(price)
        self.assertEqual(
            'Price cannot be less or equal to zero / empty', str(ctx.exception))

    def test_str_type(self):
        """
        tests str_type
        """
        val = str_type("test")
        self.assertEqual(val, "test")

        with self.assertRaises(ValueError) as ctx:
            str_type(121)
        self.assertEqual("Field value must be a string", str(ctx.exception))

        with self.assertRaises(ValueError) as ctx:
            str_type('  ')
        self.assertEqual("This field cannot be empty", str(ctx.exception))

    def test_index_page(self):
        """
        tests rendering of index page
        """
        r = self.client().get('/')
        self.assertEqual(r.status_code, 200)

    def test_menu_date_type(self):
        """
        tests a menu date
        """
        self.add_test_menu()
        with self.assertRaises(ValueError) as ctx:
            menu_date = "2018-04-26"
            menu_date_type(menu_date)
        self.assertEqual(
            'Menu for the specific date {} is already set'.format(menu_date), str(ctx.exception))

    def test_type_menu_id(self):
        with self.assertRaises(ValueError) as ctx:
            type_menu_id("1")
        self.assertEqual('Field value must be an integer', str(ctx.exception))

    def test_type_menu_id_must_exist(self):
        with self.assertRaises(ValueError) as ctx:
            type_menu_id(1000)
        self.assertEqual('Menu with id 1000 does not exist',
                         str(ctx.exception))
