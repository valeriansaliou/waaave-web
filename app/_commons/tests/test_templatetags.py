from django.test import TestCase


class PageTemplatetagsTest(TestCase):
    def test_pagination(self):
        """
        Tests that: * long paging works
                    * short paging works
        """

        from _commons.templatetags.page import pagination

        self.assertDictEqual(
            pagination('search.views.root', 7, 20, url_params={'t': 'all', 'q': 'dummy'}),
            {
                'url_params': '&q=dummy&t=all',
                'page_route': 'search.views.root',
                'page_current': 7,
                'page_total': 20,

                'page_previous': 6,
                'page_next': 8,

                'pagination_left': [1,2],
                'pagination_center': [6,7,8],
                'pagination_right': [19,20],

                'has_more_hidden': True,
            }
        )

        self.assertDictEqual(
            pagination('search.views.root', 1, 3),
            {
                'url_params': '',
                'page_route': 'search.views.root',
                'page_current': 1,
                'page_total': 3,

                'page_previous': 1,
                'page_next': 2,

                'pagination_left': [],
                'pagination_center': [1,2,3],
                'pagination_right': [],

                'has_more_hidden': False,
            }
        )
