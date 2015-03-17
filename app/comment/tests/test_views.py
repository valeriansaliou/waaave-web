from django.test import TestCase
from django.core.urlresolvers import reverse


class ViewsTest(TestCase):
    def test_read(self):
        response = self.client.get(reverse('comment.views.read', kwargs={
            'item_type': 'tutorial',
            'item_id': '0'*24,
        }))
        self.assertEqual(response.status_code, 404)


    def test_add(self):
        response = self.client.get(reverse('comment.views.add', kwargs={
            'item_type': 'shot',
            'item_id': '0'*24,
        }))
        self.assertEqual(response.status_code, 200)


    def test_action(self):
        response = self.client.get(reverse('comment.views.action', kwargs={
            'item_type': 'blog',
            'item_id': '0'*24,
        }))
        self.assertEqual(response.status_code, 200)
