from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import *


@receiver(post_save, sender=Meta)
def notify_tutorial_published_in_spot(sender, instance, **kwargs):
    """
    Notifies spot followers when a tutorial is published
    """
    # Prevents circular imports
    from spot.helpers import SpotHelper

    if instance.is_visible():
        spots = [tag_all.tag for tag_all in instance.tutorial_tags.all()]
        author_user_ids = [a.user.id for a in instance.author_set.all()]

        SpotHelper.notify_followers(
            spots=spots,
            item_type='tutorial',
            item_id=instance.id,
            ignore_user_ids=author_user_ids,
            date_threshold=instance.publish_date,
        )
