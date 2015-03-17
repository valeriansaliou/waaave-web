from django.test import TestCase
from django.core.urlresolvers import reverse


class ViewsTest(TestCase):
    def test_root(self):
        response = self.client.get(reverse('tutorial.views.root'))
        self.assertEqual(response.status_code, 301)


    def test_view(self):
        response = self.client.get(reverse('tutorial.views.view', kwargs={
            'tag': 'dummy',
            'slug': 'dummy',
        }))
        self.assertEqual(response.status_code, 404)


    def test_view_related_tutorials(self):
        response = self.client.get(reverse('tutorial.views.view_related_tutorials', kwargs={
            'tag': 'dummy',
            'slug': 'dummy',
        }))
        self.assertEqual(response.status_code, 404)


    def test_view_related_developers(self):
        response = self.client.get(reverse('tutorial.views.view_related_developers', kwargs={
            'tag': 'dummy',
            'slug': 'dummy',
        }))
        self.assertEqual(response.status_code, 404)
