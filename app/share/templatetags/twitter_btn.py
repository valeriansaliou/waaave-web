from django import template

register = template.Library()


@register.inclusion_tag('share/twitter_btn_small.jade', takes_context=True)
def twitter_btn_small(context):
    return {'twitter_btn_href': context['request'].build_absolute_uri()}


@register.inclusion_tag('share/twitter_btn_large.jade', takes_context=True)
def twitter_btn_large(context):
    return {'twitter_btn_href': context['request'].build_absolute_uri()}