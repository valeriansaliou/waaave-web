from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete
from _commons.helpers.cache import CacheHelper

from .models import *


@receiver(post_save, sender=Comment)
@receiver(pre_delete, sender=Comment)
@receiver(post_save, sender=Waaave)
@receiver(pre_delete, sender=Waaave)
@receiver(post_save, sender=Follow)
@receiver(pre_delete, sender=Follow)
@receiver(post_save, sender=FollowAdd)
@receiver(pre_delete, sender=FollowAdd)
def clear_cache_notification_all(sender, instance, **kwargs):
    """
    Automatically clears associated cache when a notification (all) record is updated
    """
    if instance.user:
        CacheHelper.io.delete(
            CacheHelper.ns('notification:factories:read:_fetch', instance.user)
        )
