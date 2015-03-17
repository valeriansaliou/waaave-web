from django import template
from django.core.urlresolvers import reverse

register = template.Library()


@register.simple_tag(takes_context=True)
def url_absolute(context, to_reverse=None, *args, **kwargs):
    """
    Build an absolute URL with the protocol and hostname part
    """
    return context['request'].build_absolute_uri(
        reverse(
            to_reverse,
            args=args,
            kwargs=kwargs
        )
    )
