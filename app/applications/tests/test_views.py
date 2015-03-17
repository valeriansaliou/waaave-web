from django.test import TestCase
from django.core.urlresolvers import reverse


class ViewsTest(TestCase):
    def test_root(self):
        response = self.client.get(reverse('applications.views.root'))
        self.assertEqual(response.status_code, 200)


    def test_ios(self):
        response = self.client.get(reverse('applications.views.ios'))
        self.assertEqual(response.status_code, 200)


    def test_android(self):
        response = self.client.get(reverse('applications.views.android'))
        self.assertEqual(response.status_code, 200)
