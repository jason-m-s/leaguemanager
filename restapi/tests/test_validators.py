from django.test import TestCase
from rest_framework.exceptions import ValidationError

from restapi.validators import validate_percentile


class PercentileValidatorTestCase(TestCase):
    def test_non_number_fails(self):
        with self.assertRaises(ValidationError):
            validate_percentile('a')

        with self.assertRaises(ValidationError):
            validate_percentile('#')

    def test_percentile_bounds(self):
        with self.assertRaises(ValidationError):
            validate_percentile(-1)

        with self.assertRaises(ValidationError):
            validate_percentile(101)

        self.assertTrue(validate_percentile(30))


