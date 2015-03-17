from django.test import TestCase
from django.core.urlresolvers import reverse


class ViewsTest(TestCase):
    def test_main(self):
        response = self.client.get(reverse('user.views.main', kwargs={
            'username': 'dummy',
        }))
        self.assertEqual(response.status_code, 404)


    def test_main_fetch(self):
        response = self.client.get(reverse('user.views.main_fetch', kwargs={
            'username': 'dummy',
            'page': 2,
        }))
        self.assertEqual(response.status_code, 404)


    def test_me(self):
        response = self.client.get(reverse('user.views.me'))
        self.assertEqual(response.status_code, 404)