import re

from django.db import models
from django_countries.fields import CountryField
from django.contrib.auth.models import User as AuthUser

from _commons.forms import defaults


# Profile: stores user profile
class Profile(models.Model):
    """
    Database [account.profile]
    """
    # System fields
    user = models.OneToOneField(AuthUser, primary_key=True)

    # Identity fields
    city = models.CharField(max_length=defaults.DEFAULT_MAX,
        db_index=True,
        verbose_name="City",
        help_text="We like to know where you all come from to make the UX better.",
        error_messages={
            'required': "Please enter your city.",
        },
    )

    country = CountryField(
        db_index=True,
        verbose_name="Country",
        help_text="Are you from the United States, England, France, China?",
        error_messages={
            'required': "Please enter your country.",
            'invalid': "Your country does not exist!",
        },
    )

    specialty = models.CharField(max_length=defaults.DEFAULT_MAX,
        db_index=True,
        verbose_name="Specialty",
        help_text="Are you a Ruby, Front-End, Node JS Developer?",
        error_messages={
            'required': "Please enter your specialty.",
        },
    )

    company = models.CharField(max_length=defaults.DEFAULT_MAX,
        db_index=True,
        blank=True,
        verbose_name="Company",
        help_text="What company are you working for? (or school)",
    )

    freelancing = models.BooleanField(
        default=False,
        verbose_name="Freelancing",
        help_text="I'm available for freelancing.",
    )

    hiring = models.BooleanField(
        default=False,
        verbose_name="Hiring",
        help_text="I'm available for hiring requests.",
    )

    # Networking states
    rank = models.PositiveSmallIntegerField(default=1)
    experience = models.DecimalField(default=0, max_digits=19, decimal_places=2)

    # External connections
    website = models.URLField(
        blank=True,
        verbose_name="Website",
        help_text="Your portfolio, blog or company site. e.g. elonmusk.com",
        error_messages={
            'invalid': "Your website address is invalid.",
        },
    )
 
    # Verification status
    register_complete = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    identity_verified = models.BooleanField(default=False)
    website_verified = models.BooleanField(default=False)

    date_update = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u'%s %s %s' % (self.user.first_name, self.user.last_name, self.user.profile.city)

    def website_url(self):
        if re.match(r'^https?://', self.website) or not self.website:
            return self.website
        else:
            return 'http://%s' % self.website


# Settings: stores user settings
class Settings(models.Model):
    """
    Database [account.settings]
    """
    # System fields
    user = models.OneToOneField(AuthUser, primary_key=True)

    # E-Mail notification settings
    email_respond = models.BooleanField(
        blank=False,
        default=True,
        verbose_name="E-Mail Respond",
        help_text="Someone adds a comment or replies to one of mine.",
    )

    email_follow = models.BooleanField(
        blank=False,
        default=True,
        verbose_name="E-Mail Follow",
        help_text="Someone follows me.",
    )

    email_follow_add = models.BooleanField(
        blank=False,
        default=True,
        verbose_name="E-Mail Follow Add",
        help_text="Someone I follow adds a new tutorial.",
    )

    # Web notification settings
    notif_respond = models.BooleanField(
        blank=False,
        default=True,
        verbose_name="Notification Respond",
        help_text="Someone adds a comment or replies to one of mine.",
    )

    notif_spot = models.BooleanField(
        blank=False,
        default=True,
        verbose_name="Notification Spot",
        help_text="New content is added in a spot you follow.",
    )

    notif_follow = models.BooleanField(
        blank=False,
        default=True,
        verbose_name="Notification Follow",
        help_text="Someone follows me.",
    )

    notif_follow_add = models.BooleanField(
        blank=False,
        default=True,
        verbose_name="Notification Follow Add",
        help_text="Someone I follow adds a new tutorial.",
    )

    notif_waaave = models.BooleanField(
        blank=False,
        default=True,
        verbose_name="Notification Waaave",
        help_text="Someone waaaves one of my tutorials.",
    )

    date_update = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u'%s %s' % (self.user.first_name, self.user.last_name)


# Register: stores registration information (for metrics + abuse control)
class Register(models.Model):
    """
    Database [account.register]
    """
    # System fields
    user = models.OneToOneField(AuthUser, primary_key=True)

    # Registration fields
    complete = models.BooleanField(default=False)
    step_current = models.PositiveSmallIntegerField(default=1)
    resumed_count = models.PositiveSmallIntegerField(default=0)
    date_start = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    date_complete = models.DateTimeField(blank=True, null=True)
    ip_start = models.GenericIPAddressField(blank=True, null=True)
    ip_update = models.GenericIPAddressField(blank=True, null=True)
    ip_complete = models.GenericIPAddressField(blank=True, null=True)

    def __unicode__(self):
        return u'%i' % (self.complete)


# Recover: stores password recovery keys + states
class Recover(models.Model):
    """
    Database [account.recover]
    """
    # System fields
    user = models.OneToOneField(AuthUser, primary_key=True)

    # Recovery
    recovered = models.BooleanField(default=False)
    date_generated = models.DateTimeField(auto_now_add=True)
    date_recovered = models.DateTimeField(blank=True, null=True)
    date_expire = models.DateTimeField(blank=True, null=True)
    key_uidb36 = models.CharField(max_length=3)
    key_token = models.CharField(max_length=20)
    key_random = models.CharField(max_length=40)

    def __unicode__(self):
        return u'%i' % (self.recovered)


# Confirm: stores account confirm keys + states
class Confirm(models.Model):
    """
    Database [account.confirm]
    """
    # System fields
    user = models.OneToOneField(AuthUser, primary_key=True)

    # Confirmation
    confirmed = models.BooleanField(default=False)
    date_generated = models.DateTimeField(auto_now_add=True)
    date_confirmed = models.DateTimeField(blank=True, null=True)
    key_uidb36 = models.CharField(max_length=3)
    key_token = models.CharField(max_length=20)
    key_random = models.CharField(max_length=40)

    def __unicode__(self):
        return u'%i' % (self.confirmed)

