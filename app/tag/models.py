from django.db import models
from django.contrib.auth.models import User as AuthUser

from _commons.fields import ColorField

from .helpers import *
from .settings import *


# List: lists available tags
class List(models.Model):
    """
    Database [tag.list]
    """
    name = models.CharField(db_index=True, max_length=TAG_NAME_MAX_LENGTH)
    description = models.CharField(max_length=TAG_DESC_MAX_LENGTH, default='')
    slug = models.CharField(db_index=True, max_length=TAG_SLUG_MAX_LENGTH)
    color = ColorField(blank=True)

    author = models.ForeignKey(AuthUser)
    date = models.DateTimeField(auto_now_add=True)

    picture_original = models.FileField(upload_to=TagHelper.get_picture_path_original)
    picture_small = models.FileField(upload_to=TagHelper.get_picture_path_small)
    picture_normal = models.FileField(upload_to=TagHelper.get_picture_path_normal)
    picture_large = models.FileField(upload_to=TagHelper.get_picture_path_large)

    def __unicode__(self):
        return u'%s' % (self.name)

    def url_picture_original(self):
        return TagHelper.get_picture_absolute_url(
            self.picture_original or DEFAULT_PICTURE_PATH['original']
        )

    def url_picture_small(self):
        return TagHelper.get_picture_absolute_url(
            self.picture_small or DEFAULT_PICTURE_PATH['small']
        )

    def url_picture_normal(self):
        return TagHelper.get_picture_absolute_url(
            self.picture_normal or DEFAULT_PICTURE_PATH['normal']
        )

    def url_picture_large(self):
        return TagHelper.get_picture_absolute_url(
            self.picture_large or DEFAULT_PICTURE_PATH['large']
        )
