from django.test import TestCase
from django.core.exceptions import ValidationError


def _assert_valid_value(fn, value, **kwargs):
    try:
        fn(value, **kwargs)
    except ValidationError:
        return False
    return True


class ValidatorsTest(TestCase):
    def test__validate_regex(self):
        """
        Tests that: * 'MySuperValue', '[A-Za-z]+' is {valid}
                    * '__-CONTAINS-!!', '[A-Z]+', restrictive=False is {valid}
                    * '', '[0-9]+', blank=True is {valid}
                    * '__-CONTAINS-!!', '[A-Z]+' is {invalid}
                    * '', '[0-9]+' is {invalid}
        """

        from _commons.validators import validate_regex

        def assert_valid_value(value, pattern, **kwargs):
            return _assert_valid_value(validate_regex, value, pattern=pattern, **kwargs)

        self.assertTrue(
            assert_valid_value('MySuperValue', '[A-Za-z]+'),
            "Valid value (variant 1)"
        )

        self.assertTrue(
            assert_valid_value('__-CONTAINS-!!', '[A-Z]+', restrictive=False),
            "Valid value (variant 2)"
        )

        self.assertTrue(
            assert_valid_value('', '[0-9]+', blank=True),
            "Valid value (variant 3)"
        )

        self.assertFalse(
            assert_valid_value('__-CONTAINS-!!', '[A-Z]+'),
            "Invalid value (variant 1)"
        )

        self.assertFalse(
            assert_valid_value('', '[0-9]+'),
            "Invalid value (variant 2)"
        )
