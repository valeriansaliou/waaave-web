from django.utils.html import escape
from django.conf import settings
from django import template
from django.template.loader import render_to_string

from _commons.helpers.cache import CacheHelper


register = template.Library()


def avatar(user=None, size='normal', attrs=[]):
    """
    Return the generated user avatar HTML
    """
    username = user.username if user else 'default'
    size = size or settings.AVATAR_DEFAULT_SIZE

    # Generate GET parameters URL part
    get_params = ''

    for attr in attrs:
        if attr[0]:
            get_params += '?' if not get_params else '&amp;'
            get_params += attr[0]

            if attr[1]:
                get_params += '=%s' % attr[1]

    return u'<img src="{src}" class="{class_}" alt="{alt}" height="{height}" width="{width}"/>'.format(
        src=('%s%s/%s/%s' % (settings.AVATAR_URL, username, size, get_params)),
        class_=settings.AVATAR_IMG_CLASS,
        alt='',
        height=size,
        width=size,
    )


def avatar_complete(user=None, size='normal'):
    """
    Return the complete generated user avatar HTML
    """
    if user is None:
        profile = None
        avatar_img = avatar(None, size)
        rank_scss = 0
    else:
        namespace = CacheHelper.ns('avatar:templatetags:avatar:avatar_complete', user_id=user.id)
        profile = CacheHelper.io.get(namespace)

        if profile is None:
            profile = user.profile
            CacheHelper.io.set(namespace, profile, 300)

        attrs = [('circle', None)]
        rank_scss = profile.rank - (profile.rank % 4)
        avatar_img = avatar(user, size, attrs)

    return render_to_string('avatar/_avatar.jade', {
        'user': user,
        'profile': profile,
        'avatar': avatar_img,
        'size': size,
        'rank_scss': rank_scss,
        'circle': True,
    })


@register.simple_tag
def avatar_small(user=None, complete=None):
    """
    Return user's small avatar
    """
    if complete is None:
        return avatar(user, 'small')
    else:
        return avatar_complete(user, 'small')


@register.simple_tag
def avatar_normal(user=None, complete=None):
    """
    Return user's normal avatar
    """
    if complete is None:
        return avatar(user, 'normal')
    else:
        return avatar_complete(user, 'normal')


@register.simple_tag
def avatar_large(user=None, complete=None):
    """
    Return user's large avatar
    """
    if complete is None:
        return avatar(user, 'large')
    else:
        return avatar_complete(user, 'large')
