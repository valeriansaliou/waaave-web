from django import template
from django.conf import settings

register = template.Library()


@register.inclusion_tag('share/facebook_btn_small.jade', takes_context=True)
def facebook_btn_small(context, btn_href=None):
    return {'facebook_btn_href': settings.FACEBOOK_PAGE if btn_href == 'page' else context['request'].build_absolute_uri()}


@register.inclusion_tag('share/facebook_btn_large.jade', takes_context=True)
def facebook_btn_large(context, btn_href=None):
    return {'facebook_btn_href': settings.FACEBOOK_PAGE if btn_href == 'page' else context['request'].build_absolute_uri()}