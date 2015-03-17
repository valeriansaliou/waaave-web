from django.db import models
from django.contrib.auth.models import User as AuthUser

from .helpers import *


class Upload(models.Model):
    """
    Database [upload.files]
    """
    user = models.ForeignKey(AuthUser)
    upload = models.FileField(upload_to=UploadHelper.get_upload_path)
    name = models.CharField(max_length=255)
    extension = models.CharField(max_length=10)
    date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u'%s' % (self.name)