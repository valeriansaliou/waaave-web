from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import *


@receiver(post_save, sender=Item)
def notify_book_published_in_spot(sender, instance, **kwargs):
    """
    Notifies spot followers when a book is published
    """
    # Prevents circular imports
    from spot.helpers import SpotHelper
    
    if instance.is_visible:
        spots = [tag_all.tag for tag_all in instance.book_tags.all()]

        SpotHelper.notify_followers(
            spots=spots,
            item_type='book',
            item_id=instance.id,
        )
