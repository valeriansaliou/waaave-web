from django.test import TestCase
from django.core.urlresolvers import reverse


class ViewsTest(TestCase):
    def test_root(self):
        response = self.client.get(reverse('home.views.root'))
        self.assertEqual(response.status_code, 200)


    def test_fetch(self):
        response = self.client.get(reverse('timeline.views.fetch', kwargs={
            'fetch_filter': 'everyone',
            'page': 2,
        }))
        self.assertEqual(response.status_code, 302)


    def test_followers(self):
        response = self.client.get(reverse('timeline.views.followers'))
        self.assertEqual(response.status_code, 302)


    def test_everyone(self):
        response = self.client.get(reverse('timeline.views.everyone'))
        self.assertEqual(response.status_code, 302)