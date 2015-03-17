import os, time

from django.conf import settings
from django.http import HttpResponse, Http404
from django.views.decorators.http import condition
from django.utils.http import http_date
from django.contrib.auth.models import User as AuthUser

from _commons.helpers.cache import CacheHelper

from .models import *
from .helpers import *
from .exceptions import *
from .utils import *


@condition(last_modified_func=avatar_last_modified)
def view(request, username=None, size=None):
    """
    Avatar > View
    """
    expirity_timeout = 60

    try:
        if not username:
            raise Http404

        render = 'circle' if request.GET.get('circle', None) is not None else 'default'
        size = size or 'normal'
        avatar_file = None
        
        namespace = CacheHelper.ns('avatar:views:view', username=username)
        avatar_data = CacheHelper.io.get(namespace)

        # Build avatar data
        if avatar_data is None:
            try:
                if username == 'default':
                    avatar_exists = True
                    avatar_mime = settings.AVATAR_DEFAULT_MIME
                    avatar_path = settings.AVATAR_DEFAULT_PATH
                else:
                    try:
                        user = AuthUser.objects.get(username=username)
                    except AuthUser.DoesNotExist:
                        try:
                            user = AuthUser.objects.get(email=username)
                        except AuthUser.DoesNotExist:
                            raise AvatarNotFound

                    try:
                        avatar = user.binding
                    except Binding.DoesNotExist:
                        try:
                            avatar = AvatarHelper.initialize(user)
                        except OSError:
                            raise AvatarNotFound

                    user_store = os.path.join(settings.AVATAR_ROOT, str(user.id))

                    avatar_exists = True
                    avatar_mime = avatar.mime
                    avatar_path = {
                        'default': {
                            'large': os.path.join(user_store, 'large.%s' % avatar.extension),
                            'normal': os.path.join(user_store, 'normal.%s' % avatar.extension),
                            'small': os.path.join(user_store, 'small.%s' % avatar.extension),
                        },

                        'circle': {
                            'large': os.path.join(user_store, 'large_circle.%s' % avatar.extension),
                            'normal': os.path.join(user_store, 'normal_circle.%s' % avatar.extension),
                            'small': os.path.join(user_store, 'small_circle.%s' % avatar.extension),
                        },
                    }

                    # Attempt to open avatar (if DB is out-of-sync, avoids 500 errors)
                    try:
                        avatar_file = open(avatar_path[render][size], 'r')
                    except IOError:
                        avatar_file = None
                        raise AvatarNotFound

            except AvatarNotFound:
                avatar_exists = False
                avatar_mime = settings.AVATAR_DEFAULT_MIME
                avatar_path = settings.AVATAR_DEFAULT_PATH

            avatar_data = {
                'exists': avatar_exists,
                'content_type': avatar_mime,
                'path': {},
            }

            for cur_render, cur_data in avatar_path.items():
                avatar_data['path'][cur_render] = {}

                for cur_size, cur_path in cur_data.items():
                    avatar_data['path'][cur_render][cur_size] = os.path.join(settings.STATIC_SRC_ROOT, cur_path)

            CacheHelper.io.set(namespace, avatar_data, 300)

        # Read & return avatar file
        if avatar_file is None:
            avatar_file = open(avatar_data['path'][render][size], 'r')

        response = HttpResponse(
            avatar_file,
            content_type=avatar_data['content_type'],
            status=(200 if avatar_data['exists'] else 404),
        )
    except Http404:
        response = HttpResponse('Not Found', content_type='text/plain', status=404)

    response['Expires'] = http_date(time.time() + expirity_timeout)

    return response
