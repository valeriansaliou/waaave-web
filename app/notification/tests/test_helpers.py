from django.test import TestCase



class NotificationHelperHelpersTest(TestCase):
    def test_filter_models(self):
        """
        Tests that: * filter_models returns an instance of dict
        """

        from notification.helpers import NotificationHelper

        user_id = 1

        self.assertIsInstance(
            NotificationHelper.filter_models(user_id),
            dict
        )


    def test_normalize_type(self):
        """
        Tests that: * 'comment' == 'comment'
                    * 'response' == 'comment'
                    * 'follow-add' == 'follow-add'
        """

        from notification.helpers import NotificationHelper

        self.assertEqual(NotificationHelper.normalize_type('comment'), 'comment')
        self.assertEqual(NotificationHelper.normalize_type('response'), 'comment')
        self.assertEqual(NotificationHelper.normalize_type('follow-add'), 'follow-add')
