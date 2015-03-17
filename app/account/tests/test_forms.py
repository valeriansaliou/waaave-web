from django.test import TestCase


class FormsTest(TestCase):
    def test_login_root_form(self):
        """
        Tests that: form works properly in various cases
        """

        from account.forms import LoginRootForm

        self.assertFalse(
            LoginRootForm(data={
                'username': 'username@server.com',
                'password': 'blah!',
                'remember': '1',
            }).is_valid(),
            "Password too short"
        )

        self.assertTrue(
            LoginRootForm(data={
                'username': 'username',
                'password': 'blahblihbleh',
            }).is_valid(),
            "Valid input (username)"
        )

        self.assertTrue(
            LoginRootForm(data={
                'username': 'username@server.org',
                'password': 'roadtoeuphoria2000',
            }).is_valid(),
            "Valid input (email)"
        )


    def test_register_go_form(self):
        """
        Tests that: form works properly in various cases
        """

        from account.forms import RegisterGoForm

        self.assertFalse(
            RegisterGoForm(data={
                'email': 'username@server.com',
                'password': 'thebestofthebest',
                'password_confirm': 'thebestofthebest',
            }).is_valid(),
            "Not agreeing to terms"
        )

        self.assertFalse(
            RegisterGoForm(data={
                'email': 'username',
                'password': 'thebestofthebest',
                'password_confirm': 'thebestofthebest',
                'terms_agree': True,
            }).is_valid(),
            "E-Mail field not containing a valid email address"
        )

        self.assertFalse(
            RegisterGoForm(data={
                'email': 'username@server.com',
                'password': 'thebestofthebest',
                'password_confirm': 'thebestofthebet',
                'terms_agree': True,
            }).is_valid(),
            "Password not matching"
        )

        self.assertTrue(
            RegisterGoForm(data={
                'email': 'username@server.com',
                'password': 'thebestofthebest',
                'password_confirm': 'thebestofthebest',
                'terms_agree': True,
            }).is_valid(),
            "Filled up correctly"
        )


    def test_register_profile_form(self):
        """
        Tests that: form works properly in various cases
        """

        from account.forms import RegisterProfileForm

        self.assertFalse(
            RegisterProfileForm(data={
                'first_name': '',
                'last_name': 'Saloche',
                'city': 'Brest',
                'country': 'FR',
            }).is_valid(),
            "First name missing"
        )

        self.assertFalse(
            RegisterProfileForm(data={
                'first_name': 'Valoche',
                'last_name': '',
                'city': 'Brest',
                'country': 'FR',
            }).is_valid(),
            "Last name missing"
        )

        self.assertFalse(
            RegisterProfileForm(data={
                'first_name': 'Valoche',
                'last_name': 'Saloche',
                'city': '',
                'country': 'FR',
            }).is_valid(),
            "City missing"
        )

        self.assertFalse(
            RegisterProfileForm(data={
                'first_name': 'Valoche',
                'last_name': 'Saloche',
                'city': 'Brest',
                'country': '',
            }).is_valid(),
            "Country missing"
        )

        self.assertTrue(
            RegisterProfileForm(data={
                'first_name': 'Valoche',
                'last_name': 'Saloche',
                'city': 'Brest',
                'country': 'FR',
            }).is_valid(),
            "Filled up correctly"
        )


    def test_register_about_form(self):
        """
        Tests that: form works properly in various cases
        """

        from account.forms import RegisterAboutForm

        self.assertTrue(
            RegisterAboutForm(data={
                'specialty': 'Python',
                'company': 'FrenchTouch Web Agency',
                'freelancing': '1',
                'hiring': '1',
            }).is_valid(),
            "Filled up correctly"
        )

        self.assertTrue(
            RegisterAboutForm(data={
                'specialty': 'Python',
                'company': 'FrenchTouch Web Agency',
            }).is_valid(),
            "Filled up correctly (no freelancing, no hiring)"
        )

        self.assertTrue(
            RegisterAboutForm(data={
                'specialty': 'Python',
            }).is_valid(),
            "Filled up correctly (no company)"
        )

        self.assertFalse(
            RegisterAboutForm(data={
                'company': 'FrenchTouch Web Agency',
                'freelancing': '1',
            }).is_valid(),
            "Specialty missing"
        )


    def test_recover_root_form(self):
        """
        Tests that: form works properly in various cases
        """

        from account.forms import RecoverRootForm

        self.assertFalse(
            RecoverRootForm().is_valid(),
            "Username missing"
        )

        self.assertTrue(
            RecoverRootForm(data={
                'username': 'username@server.com',
            }).is_valid(),
            "Filled up correctly"
        )


    def test_recover_proceed_form(self):
        """
        Tests that: form works properly in various cases
        """

        from account.forms import RecoverProceedForm

        self.assertFalse(
            RecoverProceedForm(data={
                'password': 'plop',
                'password_confirm': 'plop',
            }).is_valid(),
            "Password too short"
        )

        self.assertFalse(
            RecoverProceedForm(data={
                'password': 'plopipouet',
                'password_confirm': 'plopipoueti',
            }).is_valid(),
            "Password not matching"
        )

        self.assertTrue(
            RecoverProceedForm(data={
                'password': 'plopipouet',
                'password_confirm': 'plopipouet',
            }).is_valid(),
            "Filled up correctly"
        )


    def test_settings_root_user_form(self):
        """
        Tests that: form works properly in various cases
        """

        from account.forms import SettingsRootUserForm

        self.assertTrue(
            SettingsRootUserForm(data={
                'email': 'valerian@valeriansaliou.name',
                'first_name': 'Valerian',
                'last_name': 'Saliou',
            }).is_valid(),
            "Filled up correctly"
        )

        self.assertFalse(
            SettingsRootUserForm(data={
                'email': 'valerian[AT]valeriansaliou.name',
                'first_name': 'Valerian',
                'last_name': 'Saliou',
            }).is_valid(),
            "Invalid email"
        )

        self.assertFalse(
            SettingsRootUserForm(data={
                'first_name': 'Valerian',
                'last_name': 'Saliou',
            }).is_valid(),
            "Email missing"
        )

        self.assertFalse(
            SettingsRootUserForm(data={
                'email': 'valerian@valeriansaliou.name',
                'first_name': '',
                'last_name': 'Saliou',
            }).is_valid(),
            "First name missing"
        )

        self.assertFalse(
            SettingsRootUserForm(data={
                'email': 'valerian@valeriansaliou.name',
                'first_name': 'Valerian',
                'last_name': '',
            }).is_valid(),
            "Last name missing"
        )


    def test_settings_root_profile_form(self):
        """
        Tests that: form works properly in various cases
        """

        from account.forms import SettingsRootProfileForm

        self.assertTrue(
            SettingsRootProfileForm(data={
                'email': 'valerian@valeriansaliou.name',
                'city': 'Brest',
                'country': 'FR',
                'website': 'http://valeriansaliou.name/',
                'specialty': 'Python',
                'company': 'FrenchTouch Web Agency',
                'freelancing': '1',
                'hiring': '1',
            }).is_valid(),
            "Filled up correctly"
        )

        self.assertFalse(
            SettingsRootProfileForm(data={
                'first_name': 'Valerian',
                'last_name': 'Saliou',
                'email': 'valerian@valeriansaliou.name',
                'city': 'Brest',
                'country': '',
            }).is_valid(),
            "Country missing"
        )


    def test_settings_credentials_form(self):
        """
        Tests that: form works properly in various cases
        """

        from account.forms import SettingsCredentialsForm
        from django.contrib.auth.models import User as AuthUser

        self.assertTrue(
            SettingsCredentialsForm(
                user=AuthUser(),
                data={
                    'current_password': 'testify',
                    'new_password': '@newPWD!',
                    'verify_password': '@newPWD!',
                }
            ).is_valid(),
            "Filled up correctly"
        )

        self.assertFalse(
            SettingsCredentialsForm(
                user=AuthUser(),
                data={
                    'current_password': 'testify',
                    'new_password': '@newPWD!',
                    'verify_password': '@newPWD!2',
                }
            ).is_valid(),
            "Password not matching"
        )

        self.assertFalse(
            SettingsCredentialsForm(
                user=AuthUser(),
                data={
                    'current_password': 'testify',
                    'new_password': '',
                    'verify_password': '',
                }
            ).is_valid(),
            "New password missing"
        )


    def test_settings_notification_form(self):
        """
        Tests that: form works properly in various cases
        """

        from account.forms import SettingsNotificationForm

        self.assertTrue(
            SettingsNotificationForm(data={
                'email_respond': '1',
                'email_follow_add': '1',
                'notif_respond': '1',
            }).is_valid(),
            "Filled up correctly (variant 1)"
        )

        self.assertTrue(
            SettingsNotificationForm(data={
                'email_respond': '1',
                'email_follow': '1',
                'email_follow_add': '1',
                'notif_respond': '1',
                'notif_follow': '1',
                'notif_follow_add': '1',
                'notif_waaave': '1',
            }).is_valid(),
            "Filled up correctly (variant 2)"
        )

        self.assertTrue(
            SettingsNotificationForm(data={}).is_valid(),
            "Filled up correctly (variant 3)"
        )
