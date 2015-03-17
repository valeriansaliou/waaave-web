from django.db import models
from django.contrib.auth.models import User as AuthUser

from _index.models import Ids as _IndexIds
from _commons.models import DatedAbstract


class Record(DatedAbstract):
    """
    Database [relevance.record]
    """
    item = models.ForeignKey(_IndexIds)
    user = models.ForeignKey(AuthUser)
    is_relevant = models.BooleanField(db_index=True, default=False)

    def __unicode__(self):
        return u'%i' % (self.is_relevant)
