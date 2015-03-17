from django.test import TestCase
from django.core.urlresolvers import reverse


class ViewsTest(TestCase):
    def test_root(self):
        response = self.client.get(reverse('company.views.root'))
        self.assertEqual(response.status_code, 301)


    def test_about(self):
        response = self.client.get(reverse('company.views.about'))
        self.assertEqual(response.status_code, 200)


    def test_terms(self):
        response = self.client.get(reverse('company.views.terms'))
        self.assertEqual(response.status_code, 200)


    def test_privacy(self):
        response = self.client.get(reverse('company.views.privacy'))
        self.assertEqual(response.status_code, 200)


    def test_contact(self):
        response = self.client.get(reverse('company.views.contact'))
        self.assertEqual(response.status_code, 200)
