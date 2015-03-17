from django import template

register = template.Library()


@register.inclusion_tag('share/stumble_btn_small.jade')
def stumble_btn_small():
    return {}


@register.inclusion_tag('share/stumble_btn_large.jade')
def stumble_btn_large():
    return {}