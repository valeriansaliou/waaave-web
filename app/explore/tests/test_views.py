from django.test import TestCase
from django.core.urlresolvers import reverse


class ViewsTest(TestCase):
    def test_root(self):
        response = self.client.get(reverse('explore.views.root'))
        self.assertEqual(response.status_code, 302)


    def test_spots(self):
        response = self.client.get(reverse('explore.views.spots'))
        self.assertEqual(response.status_code, 200)


    def test_spots_popular(self):
        response = self.client.get(reverse('explore.views.spots_popular', kwargs={
            'page': 1,
        }))
        self.assertEqual(response.status_code, 200)


    def test_spots_alphabetical(self):
        response = self.client.get(reverse('explore.views.spots_alphabetical', kwargs={
            'page': 1,
        }))
        self.assertEqual(response.status_code, 200)


    def test_tutorials(self):
        response = self.client.get(reverse('explore.views.tutorials'))
        self.assertEqual(response.status_code, 200)


    def test_tutorials_yours(self):
        response = self.client.get(reverse('explore.views.tutorials_yours', kwargs={
            'page': 1,
        }))
        self.assertEqual(response.status_code, 200)


    def test_tutorials_popular(self):
        response = self.client.get(reverse('explore.views.tutorials_popular', kwargs={
            'page': 1,
        }))
        self.assertEqual(response.status_code, 200)


    def test_tutorials_alphabetical(self):
        response = self.client.get(reverse('explore.views.tutorials_alphabetical', kwargs={
            'page': 1,
        }))
        self.assertEqual(response.status_code, 200)


    def test_books(self):
        response = self.client.get(reverse('explore.views.books'))
        self.assertEqual(response.status_code, 200)


    def test_books_popular(self):
        response = self.client.get(reverse('explore.views.books_popular', kwargs={
            'page': 1,
        }))
        self.assertEqual(response.status_code, 200)


    def test_books_alphabetical(self):
        response = self.client.get(reverse('explore.views.books_alphabetical', kwargs={
            'page': 1,
        }))
        self.assertEqual(response.status_code, 200)
