from django.test import TestCase
from django.core.urlresolvers import reverse


class ViewsTest(TestCase):
    def test_root(self):
        response = self.client.get(reverse('services.views.root'))
        self.assertEqual(response.status_code, 200)


    def test_advertise(self):
        response = self.client.get(reverse('services.views.advertise'))
        self.assertEqual(response.status_code, 200)


    def test_bootstrap(self):
        response = self.client.get(reverse('services.views.bootstrap'))
        self.assertEqual(response.status_code, 200)


    def test_api(self):
        response = self.client.get(reverse('services.views.api'))
        self.assertEqual(response.status_code, 200)