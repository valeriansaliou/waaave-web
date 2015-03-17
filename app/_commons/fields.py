from django.db import models
from django.conf.global_settings import LANGUAGES

from south.modelsinspector import add_introspection_rules


add_introspection_rules([], ['^bbcode\.fields\.BBCodeTextField'])
add_introspection_rules([], ['^_commons\.fields\.IdField'])
add_introspection_rules([], ['^_commons\.fields\.ISBNField'])
add_introspection_rules([], ['^_commons\.fields\.LanguageField'])
add_introspection_rules([], ['^_commons\.fields\.ColorField'])


class IdField(models.IntegerField):
    """
    Define a field that maps a row ID value
    """
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        super(IdField, self).__init__(*args, **kwargs)


class ISBNField(models.CharField):
    """
    Define a field that maps a book ISBN value
    """
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 13

        super(ISBNField, self).__init__(*args, **kwargs)


class LanguageField(models.CharField):
    """
    Define a field that maps a language value
    """
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 2
        kwargs['choices'] = LANGUAGES
        
        super(LanguageField, self).__init__(*args, **kwargs)


class ColorField(models.CharField):
    """
    Define a field that maps an hexadecimal color value
    """
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 6
        
        super(ColorField, self).__init__(*args, **kwargs)
