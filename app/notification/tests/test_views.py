from django.test import TestCase
from django.core.urlresolvers import reverse


class ViewsTest(TestCase):
    def test_root(self):
        response = self.client.get(reverse('notification.views.root'))
        self.assertEqual(response.status_code, 302)


    def test_fetch_page(self):
        response = self.client.get(reverse('notification.views.fetch_page', kwargs={
            'page': 1,
        }))
        self.assertEqual(response.status_code, 302)


    def test_fetch_single(self):
        response = self.client.get(reverse('notification.views.fetch_single', kwargs={
            'notif_type': 'follow',
            'notif_id': 69,
        }))
        self.assertEqual(response.status_code, 302)


    def test_read(self):
        response_all = self.client.get(reverse('notification.views.read', kwargs={
            'read_type': 'all',
        }))
        self.assertEqual(response_all.status_code, 302)

        response_single = self.client.get(reverse('notification.views.read', kwargs={
            'read_type': 'single',
            'notif_type': 'comment',
            'notif_id': 1,
        }))
        self.assertEqual(response_single.status_code, 302)