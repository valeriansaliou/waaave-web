from django import template

register = template.Library()


@register.simple_tag
def subtract(value, arg):
    """
    Substract 2 numbers
    """
    if value or arg:
        return int(value or 0) - int(arg or 0)
    
    return ''