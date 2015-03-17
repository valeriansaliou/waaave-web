from django.test import TestCase
from django.core.urlresolvers import reverse


class ViewsTest(TestCase):
    def test_root(self):
        response = self.client.get(reverse('moderation.views.root'))
        self.assertEqual(response.status_code, 302)


    def test_tutorials(self):
        response = self.client.get(reverse('moderation.views.tutorials'))
        self.assertEqual(response.status_code, 302)


    def test_tutorial_trash(self):
        response = self.client.get(reverse('moderation.views.tutorial_trash'))
        self.assertEqual(response.status_code, 302)


    def test_shots(self):
        response = self.client.get(reverse('moderation.views.shots'))
        self.assertEqual(response.status_code, 302)


    def test_comments(self):
        response = self.client.get(reverse('moderation.views.comments'))
        self.assertEqual(response.status_code, 302)


    def test_users(self):
        response = self.client.get(reverse('moderation.views.users'))
        self.assertEqual(response.status_code, 302)


    def test_advertising(self):
        response = self.client.get(reverse('moderation.views.advertising'))
        self.assertEqual(response.status_code, 302)