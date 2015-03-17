from django.test import TestCase
from django.core.urlresolvers import reverse


class ViewsTest(TestCase):
    def test_root(self):
        response = self.client.get(reverse('dashboard.views.root'))
        self.assertEqual(response.status_code, 302)


    def test_shot_root(self):
        response = self.client.get(reverse('dashboard.views.shot_root'))
        self.assertEqual(response.status_code, 302)


    def test_shot_new(self):
        response = self.client.get(reverse('dashboard.views.shot_new'))
        self.assertEqual(response.status_code, 302)


    def test_shot_edit(self):
        response = self.client.get(reverse('dashboard.views.shot_edit', kwargs={
            'shot_id': 1,
        }))
        self.assertEqual(response.status_code, 302)


    def test_tutorial_root(self):
        response = self.client.get(reverse('dashboard.views.tutorial_root'))
        self.assertEqual(response.status_code, 302)


    def test_tutorial_new(self):
        response = self.client.get(reverse('dashboard.views.tutorial_new'))
        self.assertEqual(response.status_code, 302)


    def test_tutorial_edit(self):
        response = self.client.get(reverse('dashboard.views.tutorial_edit', kwargs={
            'tutorial_id': 1,
        }))
        self.assertEqual(response.status_code, 302)


    def test_tutorial_trash(self):
        response = self.client.get(reverse('dashboard.views.tutorial_trash'))
        self.assertEqual(response.status_code, 302)


    def test_followings(self):
        response = self.client.get(reverse('dashboard.views.followings'))
        self.assertEqual(response.status_code, 302)


    def test_profile_settings(self):
        response = self.client.get(reverse('dashboard.views.profile_settings'))
        self.assertEqual(response.status_code, 302)
