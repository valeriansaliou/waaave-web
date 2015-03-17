from django import template
from django.core.context_processors import csrf

from _index.helpers import ContentHelper as _IndexContentHelper
from _commons.helpers.cache import CacheHelper
from _commons.helpers.types import TypesHelper

from share.models import *

register = template.Library()


def waaave_btn(context):
    namespace = CacheHelper.ns(
        'share:templatetags:waaave_btn',
        context['request'].user,
        item_type=TypesHelper.encode(context['item_type']),
        item_id=context['item_id'],
    )

    response = CacheHelper.io.get(namespace)

    if response is None:
        response = {}

        item = _IndexContentHelper.get(context['item_id'], context['item_type'])

        if item:
            db_waaave = Waaave.objects.filter(item=item, is_active=True)
            user = context['request'].user
            uid = user.id if user.is_authenticated() else None

            response['user'] = user

            response['item_type'] = context['item_type']
            response['item_id'] = context['item_id']

            response['waaave_btn_is_active'] = db_waaave.filter(user_id=uid).exists()
            response['waaave_btn_counter'] = db_waaave.count()

        CacheHelper.io.set(namespace, response, 600)

    return response


@register.inclusion_tag('share/waaave_btn_small.jade', takes_context=True)
def waaave_btn_small(context):
    kwargs = waaave_btn(context)
    kwargs.update(csrf(context['request']))

    return kwargs


@register.inclusion_tag('share/waaave_btn_large.jade', takes_context=True)
def waaave_btn_large(context):
    kwargs = waaave_btn(context)
    kwargs.update(csrf(context['request']))

    return kwargs
