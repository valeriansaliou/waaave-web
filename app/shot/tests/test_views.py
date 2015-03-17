from django.test import TestCase
from django.core.urlresolvers import reverse


class ViewsTest(TestCase):
    def test_root(self):
        response = self.client.get(reverse('shot.views.root'))
        self.assertEqual(response.status_code, 200)


    def test_tag(self):
        response = self.client.get(reverse('shot.views.tag', kwargs={
            'tag': 'dummy',
        }))
        self.assertEqual(response.status_code, 200)


    def test_view(self):
        response = self.client.get(reverse('shot.views.view', kwargs={
            'tag': 'dummy',
            'slug': 'dummy',
        }))
        self.assertEqual(response.status_code, 200)