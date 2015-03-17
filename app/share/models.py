from django.db import models
from django.contrib.auth.models import User as AuthUser

from _index.models import Ids as _IndexIds


# Share: Waaave button
class Waaave(models.Model):
    """
    Database [share.waaave]
    """
    user = models.ForeignKey(AuthUser, related_name='waaave_user')
    item = models.ForeignKey(_IndexIds)
    is_active = models.BooleanField(db_index=True, default=True)
    date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        user = self.user_set.all()[:1].get();
        return u'%s %s' % (user.first_name, user.last_name)


# Share: Follow button
class Follow(models.Model):
    """
    Database [share.follow]
    """
    user = models.ForeignKey(AuthUser)
    follower = models.ForeignKey(AuthUser, related_name='follow_follower')
    is_active = models.BooleanField(db_index=True, default=True)
    date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        user = self.user_set.all()[:1].get();
        return u'%s %s' % (user.first_name, user.last_name)

