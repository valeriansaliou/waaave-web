from django.db import models
from django.contrib.auth.models import User as AuthUser

from tag.models import List as TagList


# Spot: Join button
class Membership(models.Model):
    """
    Database [spot.membership]
    """
    spot = models.ForeignKey(TagList)
    user = models.ForeignKey(AuthUser)
    is_active = models.BooleanField(db_index=True, default=True)
    
    date = models.DateTimeField(auto_now=True)
