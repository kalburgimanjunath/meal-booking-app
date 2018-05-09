from app.api_1_0.common import validate_date, validate_email_type
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
