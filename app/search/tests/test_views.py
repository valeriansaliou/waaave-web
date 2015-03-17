from django.test import TestCase
from django.core.urlresolvers import reverse


class ViewsTest(TestCase):
    def test_root(self):
        """
        Tests that: response['search.views.root'] is 200
        """

        response = self.client.get('%s?t=%s&q=%s' % (reverse('search.views.root'),'tutorials','dummy',))
        self.assertEqual(response.status_code, 200)


    def test_suggest(self):
        """
        Tests that: response['search.views.suggest'] is 200
        """

        response = self.client.get('%s?t=%s&q=%s' % (reverse('search.views.suggest'),'users','dummy',))
        self.assertEqual(response.status_code, 200)