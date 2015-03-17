from django.test import TestCase



class RegisterHelperHelpersTest(TestCase):
    def test_steps(self):
        """
        Tests that: RegisterHelper.steps == (itself)
        """

        from account.helpers import RegisterHelper

        self.assertListEqual(
            RegisterHelper.steps,
            [
                'go',
                'profile',
                'about',
                'done'
            ]
        )


    def test_step_name(self):
        """
        Tests that: * 0 == 'go'
                    * 1 == 'profile'
                    * 2 == 'about'
                    * 3 == 'done'
                    * 4 == 'profile'
        """

        from account.helpers import RegisterHelper

        self.assertEqual(
            RegisterHelper.step_name(0),
            'go'
        )

        self.assertEqual(
            RegisterHelper.step_name(1),
            'profile'
        )

        self.assertEqual(
            RegisterHelper.step_name(2),
            'about'
        )

        self.assertEqual(
            RegisterHelper.step_name(3),
            'done'
        )

        self.assertEqual(
            RegisterHelper.step_name(4),
            'profile'
        )



class SettingsHelperHelpersTest(TestCase):
    def test_has_email_respond(self):
        """
        Tests that: * count_new returns an instance of bool
        """

        from account.helpers import SettingsHelper

        user_id = 1

        self.assertIsInstance(
            SettingsHelper.has_email_respond(user_id),
            bool
        )


    def test_has_email_follow(self):
        """
        Tests that: * count_new returns an instance of bool
        """

        from account.helpers import SettingsHelper

        user_id = 1

        self.assertIsInstance(
            SettingsHelper.has_email_follow(user_id),
            bool
        )


    def test_has_email_follow_add(self):
        """
        Tests that: * count_new returns an instance of bool
        """

        from account.helpers import SettingsHelper

        user_id = 1

        self.assertIsInstance(
            SettingsHelper.has_email_follow_add(user_id),
            bool
        )


    def test_has_notif_respond(self):
        """
        Tests that: * count_new returns an instance of bool
        """

        from account.helpers import SettingsHelper

        user_id = 1

        self.assertIsInstance(
            SettingsHelper.has_notif_respond(user_id),
            bool
        )


    def test_has_notif_follow(self):
        """
        Tests that: * count_new returns an instance of bool
        """

        from account.helpers import SettingsHelper

        user_id = 1

        self.assertIsInstance(
            SettingsHelper.has_notif_follow(user_id),
            bool
        )


    def test_has_notif_follow_add(self):
        """
        Tests that: * count_new returns an instance of bool
        """

        from account.helpers import SettingsHelper

        user_id = 1

        self.assertIsInstance(
            SettingsHelper.has_notif_follow_add(user_id),
            bool
        )


    def test_has_notif_waaave(self):
        """
        Tests that: * count_new returns an instance of bool
        """

        from account.helpers import SettingsHelper

        user_id = 1

        self.assertIsInstance(
            SettingsHelper.has_notif_waaave(user_id),
            bool
        )
