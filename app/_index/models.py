from django.db import models

from _commons.fields import IdField


# IDs: stores content relationships (per ID)
class Ids(models.Model):
    """
    Database [_index.ids]
    """
    # System fields
    item_id = IdField(db_index=True)
    item_type = models.PositiveSmallIntegerField(db_index=True)
    date = models.DateTimeField(auto_now_add=True)