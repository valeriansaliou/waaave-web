from markdown import markdown
from BeautifulSoup import BeautifulSoup

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(is_safe=True)
@stringfilter
def markdown_to_html(value):
    extensions = [
        'codehilite',
        'fenced_code',
        'nl2br',
        'sane_lists',
        'smart_strong'
    ]

    extension_configs = {
        'codehilite': [
            ('linenums', False),
            ('css_class', 'highlight code-lines-simple')
        ]
    }

    return mark_safe(
        markdown(
            force_unicode(value),
            extensions=extensions,
            extension_configs=extension_configs,
            safe_mode='escape',
            enable_attributes=False
        )
    )


@register.filter
@stringfilter
def markdown_to_text(value):
    return ''.join(
        BeautifulSoup(
            markdown(value)
        ).findAll(text=True)
    )
