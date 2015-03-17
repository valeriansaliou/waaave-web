from django.db import models
from django.contrib.auth.models import User as AuthUser

from _index.models import Ids as _IndexIds


class CommentAbstract(models.Model):
    """
    Abstract (common model fields)
    """
    item = models.ForeignKey(_IndexIds)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


# Active: active comments stored here
class Active(CommentAbstract):
    """
    Database [comment.active]
    """
    author = models.ForeignKey(AuthUser, related_name='comment_active_author')
    in_reply_to = models.ForeignKey('self', related_name='comment_active_reply', blank=True, null=True)
    is_hidden = models.BooleanField(db_index=True, default=False)
    edit_date = models.DateTimeField(auto_now=True)
    hidden_date = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return u'%s' % (self.body)


# Pool: pooled comments stored here (thus pending for user registration)
class Pool(CommentAbstract):
    """
    Database [comment.pool]
    """
    in_reply_to = models.ForeignKey(Active, related_name='comment_pool_reply', blank=True, null=True)

    def __unicode__(self):
        return u'%s' % (self.body)


# Flag: flag data is stored there
class Flag(models.Model):
    """
    Database [comment.flag]
    """
    comment = models.ForeignKey(Active)
    author = models.ForeignKey(AuthUser)
    date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        flagger = self.author_set.all()[:1].get();
        return u'%s %s' % (flagger.first_name, flagger.last_name)

