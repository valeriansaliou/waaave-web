from django.test import TestCase
from django.core.urlresolvers import reverse


class ViewsTest(TestCase):
    def test_uploader(self):
        response = self.client.get(reverse('upload.views.uploader'))
        self.assertEqual(response.status_code, 302)