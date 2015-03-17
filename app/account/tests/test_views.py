from django.test import TestCase
from django.core.urlresolvers import reverse


class LoginViewsTest(TestCase):
    def test_login_root(self):
        """
        Tests that: response['account.views.login_root'] is 200
        """
        
        response = self.client.get(reverse('account.views.login_root'))
        self.assertEqual(response.status_code, 200)


class LogoutViewsTest(TestCase):
    def test_login_root(self):
        """
        Tests that: response['account.views.logout_root'] is 302
        """
        
        response = self.client.get(reverse('account.views.logout_root'))
        self.assertEqual(response.status_code, 302)


class RegisterViewsTest(TestCase):
    def test_register_root(self):
        """
        Tests that: response['account.views.register_root'] is 200
        """
        
        response = self.client.get(reverse('account.views.register_root'))
        self.assertEqual(response.status_code, 200)


    def test_register_go(self):
        """
        Tests that: response['account.views.register_go'] is 200
        """
        
        response = self.client.get(reverse('account.views.register_go'))
        self.assertEqual(response.status_code, 200)


    def test_register_profile(self):
        """
        Tests that: response['account.views.register_profile'] is 302
        """
        
        response = self.client.get(reverse('account.views.register_profile'))
        self.assertEqual(response.status_code, 302)


    def test_register_about(self):
        """
        Tests that: response['account.views.register_about'] is 302
        """
        
        response = self.client.get(reverse('account.views.register_about'))
        self.assertEqual(response.status_code, 302)


    def test_register_done(self):
        """
        Tests that: response['account.views.register_done'] is 302
        """
        
        response = self.client.get(reverse('account.views.register_done'))
        self.assertEqual(response.status_code, 302)


class ConfirmViewsTest(TestCase):
    def test_confirm_key(self):
        """
        Tests that: response['account.views.confirm_key'] is 404
        """
        
        response = self.client.get(reverse('account.views.confirm_key', kwargs={
            'uidb36': '0'*3,
            'token': '0'*20,
            'random': '0'*40,
        }))
        self.assertEqual(response.status_code, 404)


    def test_confirm_retry(self):
        """
        Tests that: response['account.views.confirm_retry'] is 302
        """
        
        response = self.client.get(reverse('account.views.confirm_retry'))
        self.assertEqual(response.status_code, 302)


class SettingsViewsTest(TestCase):
    def test_settings_root(self):
        """
        Tests that: response['account.views.settings_root'] is 302
        """
        
        response = self.client.get(reverse('account.views.settings_root'))
        self.assertEqual(response.status_code, 302)


    def test_settings_credentials(self):
        """
        Tests that: response['account.views.settings_credentials'] is 302
        """
        
        response = self.client.get(reverse('account.views.settings_credentials'))
        self.assertEqual(response.status_code, 302)


    def test_settings_notifications(self):
        """
        Tests that: response['account.views.settings_notifications'] is 302
        """
        
        response = self.client.get(reverse('account.views.settings_notifications'))
        self.assertEqual(response.status_code, 302)


    def test_settings_notifications_fetch(self):
        """
        Tests that: response['account.views.settings_notifications_fetch'] is 302
        """
        
        response = self.client.get(reverse('account.views.settings_notifications_fetch', kwargs={
            'page': 2,
        }))
        self.assertEqual(response.status_code, 302)


class RecoverViewsTest(TestCase):
    def test_recover_root(self):
        """
        Tests that: response['account.views.recover_root'] is 200
        """
        
        response = self.client.get(reverse('account.views.recover_root'))
        self.assertEqual(response.status_code, 200)


    def test_recover_key(self):
        """
        Tests that: response['account.views.recover_key'] is 404
        """
        
        response = self.client.get(reverse('account.views.recover_key', kwargs={
            'uidb36': '0'*3,
            'token': '0'*20,
            'random': '0'*40,
        }))
        self.assertEqual(response.status_code, 404)


    def test_recover_proceed(self):
        """
        Tests that: response['account.views.recover_proceed'] is 302
        """
        
        response = self.client.get(reverse('account.views.recover_proceed'))
        self.assertEqual(response.status_code, 302)
