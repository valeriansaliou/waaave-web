from django.db import models
from django.contrib.auth.models import User as AuthUser
from bbcode.fields import BBCodeTextField

from _commons.models import TagAbstract
from _commons.helpers.statuses import StatusesHelper

from .settings import *


# Meta: stores meta data about tutorials
class Meta(models.Model):
    """
    Database [tutorial.meta]
    """
    title = models.CharField(max_length=TUTORIAL_TITLE_MAX)

    is_online = models.BooleanField(db_index=True, default=False)
    status = models.PositiveSmallIntegerField(db_index=True, default=0)

    level = models.PositiveSmallIntegerField(default=0)
    shares = models.PositiveIntegerField(default=0)

    publish_date = models.DateTimeField(blank=True, null=True)
    moderation_message = models.TextField(default='')
    date_update = models.DateTimeField(auto_now=True)
    date = models.DateTimeField(auto_now_add=True)

    def is_visible(self):
        if self.is_online and self.status is StatusesHelper.encode('accepted'):
            return True
        return False

    def __unicode__(self):
        return u'%s' % (self.title)


# Author: binds an author to its tutorial
class Author(models.Model):
    """
    Database [tutorial.author]
    """
    tutorial = models.ForeignKey(Meta)
    user = models.ForeignKey(AuthUser)
    is_master = models.BooleanField(db_index=True, default=False)
    date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        user = self.user_set.all()[:1].get();
        return u'%s %s' % (user.first_name, user.last_name)


# Content: stores the tutorial text content
class Content(models.Model):
    """
    Database [tutorial.content]
    """
    tutorial = models.OneToOneField(Meta)
    user = models.ForeignKey(AuthUser)
    body = BBCodeTextField()
    date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u'%s' % (self.body)


# Url: stores URLs of tutorials (with URL change tracking)
class Url(models.Model):
    """
    Database [tutorial.url]
    """
    tutorial = models.ForeignKey(Meta)

    tag = models.CharField(db_index=True, max_length=TUTORIAL_TAG_MAX)
    slug = models.CharField(db_index=True, max_length=TUTORIAL_SLUG_MAX)
    is_alias = models.BooleanField(db_index=True, default=False)
    
    date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'%s' % (self.slug)


# Tag: stores tags that are mapped to a given tutorial
class Tag(TagAbstract):
    """
    Database [tutorial.tag]
    """
    tutorial = models.ForeignKey(Meta, related_name='tutorial_tags')
