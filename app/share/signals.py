from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete
from _commons.helpers.cache import CacheHelper

from .models import *


@receiver(post_save, sender=Waaave)
@receiver(pre_delete, sender=Waaave)
def clear_cache_share_waaave(sender, instance, **kwargs):
    """
    Automatically clears associated cache when a share (waaave) record is updated
    """
    if instance.user and instance.item:
        CacheHelper.io.delete(
            CacheHelper.ns(
                'share:templatetags:waaave_btn',
                instance.user,
                item_type=instance.item.item_type,
                item_id=instance.item.item_id,
            )
        )


@receiver(post_save, sender=Follow)
@receiver(pre_delete, sender=Follow)
def clear_cache_share_follow(sender, instance, **kwargs):
    """
    Automatically clears associated cache when a share (follow) record is updated
    """
    if instance.user and instance.follower:
        CacheHelper.io.delete(
            CacheHelper.ns(
                'share:templatetags:follow_btn',
                instance.follower,
                user_id=instance.user.id,
            )
        )
