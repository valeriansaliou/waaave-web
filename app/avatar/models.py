from django.db import models
from django.contrib.auth.models import User as AuthUser


# Binding: bind the disk-stored avatar information
class Binding(models.Model):
    """
    Database [avatar.binding]
    """
    user = models.OneToOneField(AuthUser, unique=True)
    mime = models.CharField(max_length=255)
    extension = models.CharField(max_length=10)
    source = models.CharField(max_length=14)
    url = models.URLField(blank=True)
    date = models.DateTimeField(auto_now=True)
