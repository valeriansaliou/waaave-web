from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete
from _commons.helpers.cache import CacheHelper

from .models import *


@receiver(post_save, sender=Binding)
@receiver(pre_delete, sender=Binding)
def clear_cache_avatar_binding(sender, instance, **kwargs):
    """
    Automatically clears associated cache when an avatar (binding) record is updated
    """
    if instance.user:
        CacheHelper.io.delete(
            CacheHelper.ns('avatar:views:view', username=instance.user.username)
        )

        CacheHelper.io.delete(
            CacheHelper.ns('avatar:utils:avatar_last_modified', username=instance.user.username)
        )
