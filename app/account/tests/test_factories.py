# -*- coding: utf-8 -*- 

from django.test import TestCase


class UserFactoryFactoriesTest(TestCase):
    def test_generate_username(self):
        """
        Tests that: * u"Valérian", "Saliou" == "valerian.saliou"
                    * "John", "Doe" == "john.doe"
                    * "Jane", "Moffit!?" == "jane.moffit"
                    * u"Καλημέρα", "Joe" == "kalhmera.joe"
        """

        from account.factories import UserFactory

        self.assertEqual(
            UserFactory.generate_username(
                first_name=u'Valérian',
                last_name='Saliou'
            ),
            'valerian.saliou'
        )

        self.assertEqual(
            UserFactory.generate_username(
                first_name='John',
                last_name='Doe'
            ),
            'john.doe'
        )

        self.assertEqual(
            UserFactory.generate_username(
                first_name='Jane',
                last_name='Moffit!?'
            ),
            'jane.moffit'
        )

        self.assertEqual(
            UserFactory.generate_username(
                first_name=u'Καλημέρα',
                last_name='Joe'
            ),
            'kalhmera.joe'
        )
