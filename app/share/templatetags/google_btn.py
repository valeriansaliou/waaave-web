from django import template

register = template.Library()


@register.inclusion_tag('share/google_btn_small.jade')
def google_btn_small():
    return {}


@register.inclusion_tag('share/google_btn_large.jade')
def google_btn_large():
    return {}