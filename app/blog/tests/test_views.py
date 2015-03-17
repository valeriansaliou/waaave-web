from django.test import TestCase
from django.core.urlresolvers import reverse


class ViewsTest(TestCase):
    def test_page(self):
        response = self.client.get(reverse('blog.views.page', kwargs={
            'page_number': 1,
        }))
        self.assertEqual(response.status_code, 200)


    def test_date(self):
        response = self.client.get(reverse('blog.views.date'))
        self.assertEqual(response.status_code, 200)

        # TODO: passing URL args does not work!
        """
        response = self.client.get(reverse('blog.views.date', kwargs={
            'date_year': 2013,
            'date_month': 10,
            'date_day': 23,
        }))
        """


    def test_category(self):
        response = self.client.get(reverse('blog.views.category', kwargs={
            'category_slug': 'dummy',
        }))
        self.assertEqual(response.status_code, 200)


    def test_post(self):
        response = self.client.get(reverse('blog.views.post', kwargs={
            'post_year': 2011,
            'post_slug': 'dummy',
        }))
        self.assertEqual(response.status_code, 200)