from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete
from _commons.helpers.cache import CacheHelper

from .models import *


@receiver(post_save, sender=Record)
@receiver(pre_delete, sender=Record)
def clear_cache_relevance_record(sender, instance, **kwargs):
    """
    Automatically clears associated cache when a relevance (record) record is updated
    """
    if instance.user:
        CacheHelper.io.delete(
            CacheHelper.ns('relevance:helpers:__read', item_id=instance.item.id, uid=instance.user.id)
        )
