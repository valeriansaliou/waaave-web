import re

from django.core.exceptions import ValidationError


def _is_valid(self, form):
    """
    Check if a form field is valid
    """
    ret = form.is_valid(self)

    for f in self.errors:
        class_prev = self.fields[f].widget.attrs.get('class', '')
        self.fields[f].widget.attrs.update({
            'class': class_prev + ' input-error'
        })

    return ret


def validate_regex(value, pattern, invalid_code='invalid', restrictive=True, blank=False):
    """
    Validate value against any provided pattern
    """
    if not value and blank is True:
        return

    regex = re.compile(('(:?.*)%s(:?.*)' if not restrictive else '^%s$') % pattern)

    if not regex.match(value):
        raise ValidationError('', code=invalid_code)