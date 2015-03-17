from django.db import models
from django.contrib.auth.models import User as AuthUser


# Contact: stores the contact messages that are sent
class Contact(models.Model):
    """
    Database [company.contact]
    """
    user = models.ForeignKey(AuthUser, blank=True, null=True, default=None)
    full_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    reason = models.CharField(max_length=255)
    message = models.TextField()
    date = models.DateTimeField(auto_now=True)
