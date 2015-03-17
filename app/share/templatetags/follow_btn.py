from django import template
from django.core.context_processors import csrf

from _commons.helpers.cache import CacheHelper

from share.models import Follow


register = template.Library()


def follow_btn(context, user_id):
    namespace = CacheHelper.ns(
        'share:templatetags:follow_btn',
        context['request'].user,
        user_id=user_id,
    )

    res = CacheHelper.io.get(namespace)

    if res is None:
        user = context['request'].user
        uid = context['request'].user.id if context['request'].user.is_authenticated() else None

        follow_all = Follow.objects.filter(user_id=user_id, is_active=True)
        me_is_following = Follow.objects.filter(user_id=user_id, follower_id=uid, is_active=True).exists() if uid else False

        res = {
            'user': user,
            'follow_user_id': user_id,
            'follow_counter': follow_all.count(),
            'follow_btn_is_active': me_is_following,
            'follow_is_me': str(uid) == str(user_id),
        }

        CacheHelper.io.set(namespace, res, 300)

    return res


@register.inclusion_tag('share/follow_btn_small.jade', takes_context=True)
def follow_btn_small(context, user):
    kwargs = follow_btn(context, user.id)
    kwargs.update(csrf(context['request']))

    return kwargs


@register.inclusion_tag('share/follow_btn_large.jade', takes_context=True)
def follow_btn_large(context, user):
    kwargs = follow_btn(context, user.id)
    kwargs.update(csrf(context['request']))

    return kwargs
