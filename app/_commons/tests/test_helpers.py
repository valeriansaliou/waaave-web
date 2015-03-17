# -*- coding: utf-8 -*- 

from django.test import TestCase


class CacheHelperHelpersTest(TestCase):
    def test_ns(self):
        """
        Tests that: * "app:module:method" == "app:module:method[anonymous]"
                    * "app:module:method", l={} == "app:module:method[anonymous](l={})"
                    * "app:module:method", a=2, b="plop" == "app:module:method[anonymous](a=2|b=plop)"
        """

        from _commons.helpers.cache import CacheHelper

        self.assertEqual(CacheHelper.ns('app:module:method', hash=False), 'app:module:method[anonymous]')
        self.assertEqual(CacheHelper.ns('app:module:method', l={}, hash=False), 'app:module:method[anonymous](l={})')
        self.assertEqual(CacheHelper.ns('app:module:method', a=2, b='plop', hash=False), 'app:module:method[anonymous](a=2|b=plop)')


class DurationsHelpersTest(TestCase):
    def test_humanize(self):
        """
        Tests that: * 60s == "1 minute"
                    * 600s == "10 minutes"
                    * 7200 == "2 hours"
                    * 86400 == "1 day"
        """

        from _commons.helpers.durations import humanize

        self.assertEqual(humanize(60), '1 minute')
        self.assertEqual(humanize(600), '10 minutes')
        self.assertEqual(humanize(7200), '2 hours')
        self.assertEqual(humanize(86400), '1 day')


class LevelsHelperHelpersTest(TestCase):
    def test_encode(self):
        """
        Tests that: * "dummy" == 0
                    * "intermediate" == 2
        """

        from _commons.helpers.levels import LevelsHelper

        self.assertEqual(LevelsHelper.encode('dummy'), 0)
        self.assertEqual(LevelsHelper.encode('intermediate'), 2)


    def test_reverse(self):
        """
        Tests that: * 1 == "novice"
                    * 3 == "advanced"
        """

        from _commons.helpers.levels import LevelsHelper

        self.assertEqual(LevelsHelper.reverse(1)[0], 'novice')
        self.assertEqual(LevelsHelper.reverse(3)[0], 'advanced')


class NumbersHelpersTest(TestCase):
    def test_percentage_of(self):
        """
        Tests that: * 30,0 == 0
                    * 0,1 == 0
                    * 10,50 == 20
                    * 25,100 == 25
                    * 10,10 == 100
        """

        from _commons.helpers.numbers import percentage_of

        self.assertEqual(percentage_of(30,0), 100)
        self.assertEqual(percentage_of(0,1), 0)
        self.assertEqual(percentage_of(10,50), 16)
        self.assertEqual(percentage_of(25,100), 20)
        self.assertEqual(percentage_of(10,10), 50)


class RedirectsHelpersTest(TestCase):
    def test_login_required_url(self):
        """
        Tests that: * "/dashboard/tutorial/new/" == "/account/login/?next=%2Fdashboard%2Ftutorial%2Fnew%2F&required"
        """

        from _commons.helpers.redirects import login_required_url

        self.assertEqual(\
            login_required_url('/dashboard/tutorial/new/'),\
            '/account/login/?next=%2Fdashboard%2Ftutorial%2Fnew%2F&required'\
        )


    def test_register_required_url(self):
        """
        Tests that: * None == "/account/register/"
        """

        from _commons.helpers.redirects import register_required_url

        self.assertEqual(register_required_url(), '/account/register/')


class StatusesHelperHelpersTest(TestCase):
    def test_encode(self):
        """
        Tests that: * "moderated" == 1
                    * "accepted" == 2
        """

        from _commons.helpers.statuses import StatusesHelper

        self.assertEqual(StatusesHelper.encode('moderated'), 1)
        self.assertEqual(StatusesHelper.encode('accepted'), 2)


    def test_reverse(self):
        """
        Tests that: * 1 == "moderated"
                    * 2 == "accepted"
        """

        from _commons.helpers.statuses import StatusesHelper

        self.assertEqual(StatusesHelper.reverse(1)[0], 'moderated')
        self.assertEqual(StatusesHelper.reverse(2)[0], 'accepted')


class StringsHelpersTest(TestCase):
    def test_strip_accents(self):
        """
        Tests that: * "valérian" == "valerian"
                    * "ALLÔ" == "ALLO"
        """

        from _commons.helpers.strings import StringsHelper

        self.assertEqual(StringsHelper.strip_accents(u'valérian'), 'valerian')
        self.assertEqual(StringsHelper.strip_accents(u'ALLÔ'), 'ALLO')


    def test_downcode(self):
        """
        Tests that: * u"Καλημέρα Joe!" == "Kalhmera Joe!"
                    * "Test Normal" == "Test Normal"
        """

        from _commons.helpers.strings import StringsHelper

        self.assertEqual(StringsHelper.downcode(u'Καλημέρα Joe!'), 'Kalhmera Joe!')
        self.assertEqual(StringsHelper.downcode('Test Normal'), 'Test Normal')


class TypesHelperHelpersTest(TestCase):
    def test_encode(self):
        """
        Tests that: * "comment" == 0
                    * "tutorial" == 1
        """

        from _commons.helpers.types import TypesHelper

        self.assertEqual(TypesHelper.encode('comment'), 0)
        self.assertEqual(TypesHelper.encode('tutorial'), 1)


    def test_reverse(self):
        """
        Tests that: * 0 == "comment"
                    * 1 == "tutorial"
        """

        from _commons.helpers.types import TypesHelper

        self.assertEqual(TypesHelper.reverse(0), 'comment')
        self.assertEqual(TypesHelper.reverse(1), 'tutorial')
