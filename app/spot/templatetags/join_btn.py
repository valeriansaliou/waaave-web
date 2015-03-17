from django import template
from django.core.context_processors import csrf

from _commons.helpers.cache import CacheHelper

from ..helpers import *
from ..models import *


register = template.Library()


def join_btn(context, spot):
    namespace = CacheHelper.ns(
        'spot:templatetags:join_btn',
        context['request'].user,
        spot_id=spot.id,
    )

    response = CacheHelper.io.get(namespace)

    if response is None:
        user = context['request'].user if context['request'].user.is_authenticated() else None

        join_all = Membership.objects.filter(spot=spot, is_active=True)
        me_is_in = join_all.filter(spot=spot, user=user).exists() if user else False

        response = {
            'join_spot': spot,
            'join_counter': join_all.count(),
            'join_btn_is_active': me_is_in,
        }

        CacheHelper.io.set(namespace, response, 300)

    return response


@register.inclusion_tag('spot/_spot_join_btn_label.jade', takes_context=True)
def join_btn_label(context, spot):
    kwargs = join_btn(context, spot)
    kwargs.update(csrf(context['request']))

    return kwargs


@register.inclusion_tag('spot/_spot_join_btn_count_small.jade', takes_context=True)
def join_btn_count_small(context, spot):
    kwargs = join_btn(context, spot)
    kwargs.update(csrf(context['request']))

    return kwargs


@register.inclusion_tag('spot/_spot_join_btn_count_large.jade', takes_context=True)
def join_btn_count_large(context, spot):
    kwargs = join_btn(context, spot)
    kwargs.update(csrf(context['request']))

    return kwargs
