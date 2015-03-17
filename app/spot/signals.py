from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete
from _commons.helpers.cache import CacheHelper

from .models import *


@receiver(post_save, sender=Membership)
@receiver(pre_delete, sender=Membership)
def clear_cache_spot_membership(sender, instance, **kwargs):
    """
    Automatically clears associated cache when a spot (membership) record is updated
    """
    if instance.user and instance.spot:
        CacheHelper.io.delete(
            CacheHelper.ns(
                'spot:templatetags:join_btn',
                instance.user,
                spot_id=instance.spot.id,
            )
        )
