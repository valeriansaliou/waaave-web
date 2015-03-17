from django.test import TestCase
from django.core.urlresolvers import reverse


class ViewsTest(TestCase):
    def test_root(self):
        response = self.client.get(reverse('activity.views.root'))
        self.assertEqual(response.status_code, 302)


    def test_statistics(self):
        response = self.client.get(reverse('activity.views.statistics'))
        self.assertEqual(response.status_code, 302)


    def test_comments(self):
        response = self.client.get(reverse('activity.views.comments'))
        self.assertEqual(response.status_code, 302)
