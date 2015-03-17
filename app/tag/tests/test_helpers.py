from django.test import TestCase


class TagHelperHelpersTest(TestCase):
    def test_unpack(self):
        """
        Tests that: * '' == ['']
                    * 'plop, pouet, yup' == ['plop', ' pouet', ' yup']
                    * 'plop, pouet, ,,,' == ['plop', ' pouet', ' ', '', '', '']
        """

        from tag.helpers import TagHelper

        self.assertListEqual(
            TagHelper.unpack(''),
            ['']
        )

        self.assertListEqual(
            TagHelper.unpack('plop, pouet, yup'),
            ['plop', ' pouet', ' yup']
        )

        self.assertListEqual(
            TagHelper.unpack('plop, pouet, ,,,'),
            ['plop', ' pouet', ' ', '', '', '']
        )


    def test_normalize(self):
        """
        Tests that: * [''] == []
                    * ['Pouet', 'plop pouet', ''] == [('pouet','Pouet',), ('plop-pouet','Plop Pouet',)]
                    * ['plop', 'plipED'] == [('plop','Plop',), ('pliped','Pliped',)]
        """

        from tag.helpers import TagHelper

        self.assertListEqual(
            TagHelper.normalize(['']),
            []
        )

        self.assertListEqual(
            TagHelper.normalize(['Pouet', 'plop pouet', '']),
            [('pouet','Pouet',), ('plop-pouet','Plop Pouet',)]
        )

        self.assertListEqual(
            TagHelper.normalize(['plop', 'plipED']),
            [('plop','Plop',), ('pliped','Pliped',)]
        )


    def test_string_to_list(self):
        """
        Tests that: * '' == []
                    * ', ,,  , ,,   ' == []
                    * 'PLOP, pouet, yup' == [('plop','Plop',), ('pouet','Pouet',), ('yup','Yup',)]
        """

        from tag.helpers import TagHelper

        self.assertListEqual(
            TagHelper.string_to_list(''),
            []
        )

        self.assertListEqual(
            TagHelper.string_to_list(', ,,  , ,,   '),
            []
        )

        self.assertListEqual(
            TagHelper.string_to_list('PLOP, pouet, yup'),
            [('plop','Plop',), ('pouet','Pouet',), ('yup','Yup',)]
        )


    def test_validate(self):
        """
        Tests that: * ('','Plop',) == False
                    * ('plopipouetpeipeo-etara','Plopipouetpeipeo Etara',) == False
                    * ('plop','Plop',) == True
        """

        from tag.helpers import TagHelper

        self.assertEqual(
            TagHelper.validate(('','Plop',)),
            False
        )

        self.assertEqual(
            TagHelper.validate(('plopipouetpeipeo-etara','Plopipouetpeipeo Etara',)),
            False
        )

        self.assertEqual(
            TagHelper.validate(('plop','Plop',)),
            True
        )