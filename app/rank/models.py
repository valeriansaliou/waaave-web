from django.db import models
from django.contrib.auth.models import User as AuthUser

from _commons.fields import IdField


# Useful to recompute the rank of each Waaaver if we process changes in our algorithm
class Record(models.Model):
    """
    Database [rank.records]
    """
    recipient = models.ForeignKey(AuthUser, related_name='rank_record_recipient')
    recipient_rank = models.PositiveIntegerField()

    sender = models.ForeignKey(AuthUser, related_name='rank_record_sender', null=True, default=None)
    sender_rank = models.PositiveIntegerField(null=True, default=None)
    sender_rank_impact = models.DecimalField(null=True, default=None, max_digits=3, decimal_places=2)

    entity_id = IdField(db_index=True)
    entity_type = models.CharField(db_index=True, max_length=255)
    
    action_type = models.CharField(max_length=255)
    action_exp = models.DecimalField(max_digits=5, decimal_places=2)
    action_exp_with_impact = models.DecimalField(max_digits=5, decimal_places=2)
    action_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        recipient = self.recipient_set.all()[:1].get();
        sender = self.sender_set.all()[:1].get();
        return u'%s %s %s' % (recipient.username, sender.username, self.action_type)
