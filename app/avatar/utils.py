from datetime import datetime
from django.contrib.auth.models import User as AuthUser

from _commons.helpers.cache import CacheHelper

from .models import *


def avatar_last_modified(request, username=None, size=None):
    if username:
        namespace = CacheHelper.ns('avatar:utils:avatar_last_modified', username=username)
        avatar_data = CacheHelper.io.get(namespace)

        if not avatar_data:
            avatar_data = {
                'last_modified': None
            }

            try:
                user = AuthUser.objects.get(username=username)
            except AuthUser.DoesNotExist:
                try:
                    user = AuthUser.objects.get(email=username)
                except AuthUser.DoesNotExist:
                    user = None

            if user:
                try:
                    avatar_data['last_modified'] = user.binding.date
                except Binding.DoesNotExist:
                    pass

            CacheHelper.io.set(namespace, avatar_data, 300)

        return avatar_data['last_modified']

    return None