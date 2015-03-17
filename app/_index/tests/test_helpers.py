from django.test import TestCase


class ContentHelperHelpersTest(TestCase):
    def test_validate(self):
        """
        Tests that: * 1, 'tutorial' == (itself)
        """

        from _index.helpers import ContentHelper

        self.assertTupleEqual(
            ContentHelper.validate(1, 'tutorial'),
            (False, None)
        )
