from django import forms

from .helpers import *
from .settings import *


class TagField(forms.Field):
    def to_python(self, value):
        """
        Normalize comma-separated tag string to a list of tags.
        """
        return TagHelper.string_to_list(value)


    def validate(self, value):
        """
        Check if valid tag data has been submitted
        """
        super(TagField, self).validate(value)

        for tag in value:
            if not TagHelper.validate(tag):
                raise forms.ValidationError('Tags must be smaller than %s chars.' % TAG_NAME_MAX_LENGTH)
