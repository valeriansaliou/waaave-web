from django.test import TestCase
from django.core.urlresolvers import reverse


class ViewsTest(TestCase):
    def test_root(self):
        response = self.client.get(reverse('spot.views.root'))
        self.assertEqual(response.status_code, 301)


    def test_view_root(self):
        response = self.client.get(reverse('spot.views.view_root', kwargs={
            'tag': 'dummy',
        }))
        self.assertEqual(response.status_code, 404)


    def test_view_root_fetch(self):
        response = self.client.get(reverse('spot.views.view_root_fetch', kwargs={
            'tag': 'dummy',
            'page': '1',
        }))
        self.assertEqual(response.status_code, 404)


    def test_view_tutorials(self):
        response = self.client.get(reverse('spot.views.view_tutorials', kwargs={
            'tag': 'dummy',
            'page': '1',
        }))
        self.assertEqual(response.status_code, 404)


    def test_view_books(self):
        response = self.client.get(reverse('spot.views.view_books', kwargs={
            'tag': 'dummy',
            'page': '1',
        }))
        self.assertEqual(response.status_code, 404)


    def test_view_waaavers(self):
        response = self.client.get(reverse('spot.views.view_waaavers', kwargs={
            'tag': 'dummy',
            'page': '1',
        }))
        self.assertEqual(response.status_code, 404)


    def test_join(self):
        response = self.client.get(reverse('spot.views.join', kwargs={
            'tag': 'dummy',
        }))
        self.assertEqual(response.status_code, 200)
