from django import template

register = template.Library()


def class_tag(context, pattern, class_value):
    """
    Return the provided class tag
    """
    import re
    if re.search(pattern, context['request'].path):
        return class_value
    return ''


@register.simple_tag(takes_context=True)
def active(context, pattern):
    """
    Return the active class tag
    """
    return class_tag(context, pattern, 'active')


@register.simple_tag(takes_context=True)
def done(context, pattern):
    """
    Return the done class tag
    """
    return class_tag(context, pattern, 'done')