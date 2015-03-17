from django.test import TestCase



class ProcessHelperHelpersTest(TestCase):
    def test_duration(self):
        """
        Tests that: * "Blah Bluh Bleh", 2 == 6
                    * "Hello World", 3 == 6
        """

        from tutorial.helpers.process import ProcessHelper

        self.assertEqual(
            ProcessHelper.duration('Blah Bluh Bleh', 2),
            6
        )

        self.assertEqual(
            ProcessHelper.duration('Hello World', 3),
            6
        )


    def test_url(self):
        """
        Tests that: * None ~= {None}
                    * None ~= {None}
        """

        from tutorial.helpers.process import ProcessHelper

        tutorial_url_none = {
            'tag': None,
            'slug': None,
        }

        self.assertDictEqual(
            ProcessHelper.url(None),
            tutorial_url_none
        )

        self.assertDictEqual(
            ProcessHelper.url(1),
            tutorial_url_none
        )


    def test_title(self):
        """
        Tests that: * None ~= {None}
                    * None ~= {None}
        """

        from tutorial.helpers.process import ProcessHelper

        self.assertEqual(
            ProcessHelper.title(None),
            None
        )

        self.assertEqual(
            ProcessHelper.title(1),
            None
        )


    def test_author(self):
        """
        Tests that: * None ~= {None}
                    * None ~= {None}
        """

        from tutorial.helpers.process import ProcessHelper

        self.assertEqual(
            ProcessHelper.author(None),
            None
        )

        self.assertEqual(
            ProcessHelper.author(1),
            None
        )


    def test_check(self):
        """
        Tests that: * 'view', 'dummy', 'dummy' ~= (None)
                    * 'view', None, None ~= (None)
        """

        from tutorial.helpers.process import ProcessHelper

        tutorial_checker_none = (None, 'not_found', None)

        self.assertTupleEqual(
            ProcessHelper.check('view', 'dummy', 'dummy'),
            tutorial_checker_none
        )

        self.assertTupleEqual(
            ProcessHelper.check('view', None, None),
            tutorial_checker_none
        )



class ReadHelperHelpersTest(TestCase):
    def test_status(self):
        """
        Tests that: * None == 'none'
                    * 69 => 'none'
        """

        from tutorial.helpers.read import ReadHelper

        self.assertEqual(
            ReadHelper.status(None),
            'none'
        )

        self.assertEqual(
            ReadHelper.status(69),
            'none'
        )



class TagHelperHelpersTest(TestCase):    
    def test_list(self):
        """
        Tests that: * None == []
        """

        from tutorial.helpers.tag import TagHelper
        from collections import Iterable

        self.assertIsInstance(
            TagHelper.list(None),
            Iterable
        )
