from django.db import models
from django.contrib.auth.models import User as AuthUser

from comment.models import Active as CommentActive
from tag.models import List as TagList
from share.models import Waaave as ShareWaaave
from share.models import Follow as ShareFollow

from _index.models import Ids as _IndexIds


class Notification(models.Model):
    """
    Abstract (common model fields)
    """
    is_active = models.BooleanField(db_index=True, default=True)
    is_new = models.BooleanField(db_index=True, default=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def __unicode__(self):
        return u'%s [%s] - %s %s' % (self.__class__.__name__, self.id, self.user.first_name, self.user.last_name)


# Comment: comment (and replies) notifications
class Comment(Notification):
    """
    Database [notification.comment]
    """
    user = models.ForeignKey(AuthUser, related_name='notification_comment_user')
    comment = models.ForeignKey(CommentActive, related_name='notification_comment_comment')


# Spot: spot (and replies) notifications
class Spot(Notification):
    """
    Database [notification.spot]
    """
    user = models.ForeignKey(AuthUser, related_name='notification_spot_user')
    spot = models.ForeignKey(TagList, related_name='notification_spot_spot')
    index = models.ForeignKey(_IndexIds, related_name='notification_spot_index')


# Waaave: waaave button notifications
class Waaave(Notification):
    """
    Database [notification.waaave]
    """
    user = models.ForeignKey(AuthUser, related_name='notification_waaave_user')
    waaave = models.ForeignKey(ShareWaaave, related_name='notification_waaave_waaave')


# Follow: follow button notifications
class Follow(Notification):
    """
    Database [notification.follow]
    """
    user = models.ForeignKey(AuthUser, related_name='notification_follow_user')
    follow = models.ForeignKey(ShareFollow, related_name='notification_follow_follow')


# Follow Add: follow add (tutorial) notifications
class FollowAdd(Notification):
    """
    Database [notification.follow_add]
    """
    user = models.ForeignKey(AuthUser, related_name='notification_followadd_user')
    index = models.ForeignKey(_IndexIds, related_name='notification_followadd_index')
