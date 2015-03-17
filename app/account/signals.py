from django.dispatch import receiver
from django.db.models.signals import post_save

from spot.helpers import SpotHelper

from .models import *


@receiver(post_save, sender=Profile)
def autojoin_spot_for_specialty(sender, instance, **kwargs):
    """
    Automatically joins specified specialty spot when an account (profile) record is updated
    """
    if instance.user and instance.specialty:
        SpotHelper.autojoin(
            user=instance.user,
            name=instance.specialty,
        )
