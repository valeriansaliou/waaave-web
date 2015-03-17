from django.test import TestCase
from django.core.urlresolvers import reverse


class ViewsTest(TestCase):
    def test_view(self):
        response = self.client.get(reverse('avatar.views.view', kwargs={
            'username': 'dummy.user',
            'size': 'normal'
        }))
        self.assertEqual(response.status_code, 404)

        response = self.client.get(reverse('avatar.views.view', kwargs={
            'username': 'default',
            'size': 'large'
        }))
        self.assertEqual(response.status_code, 200)
