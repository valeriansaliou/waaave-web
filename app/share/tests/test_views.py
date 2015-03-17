from django.test import TestCase
from django.core.urlresolvers import reverse


class ViewsTest(TestCase):
    def test_waaave(self):
        response = self.client.get(reverse('share.views.waaave', kwargs={
            'item_type': 'tutorial',
            'item_id': 1,
        }))
        self.assertEqual(response.status_code, 200)


    def test_follow(self):
        response = self.client.get(reverse('share.views.follow', kwargs={
            'user_id': 1,
        }))
        self.assertEqual(response.status_code, 200)