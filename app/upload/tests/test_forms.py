from django.test import TestCase


class FormsTest(TestCase):
    def test_uploader_form(self):
        """
        Tests that: (nothing)
        """

        from upload.forms import UploaderForm

        self.assertFalse(
            UploaderForm().is_valid(),
            "No file provided"
        )