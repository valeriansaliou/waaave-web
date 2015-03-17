from django.db import models
from django.contrib.auth.models import User as AuthUser

from tag.models import List as TagList


class DatedAbstract(models.Model):
    """
    Abstract for dated fields (common model fields)
    """
    date_update = models.DateTimeField(auto_now=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class TagAbstract(DatedAbstract):
    """
    Abstract for tags (common model fields)
    """
    tag = models.ForeignKey(TagList, related_name='%(app_label)s_tag_list')

    class Meta:
        abstract = True
