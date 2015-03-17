from django.db import models
from django.contrib.auth.models import User as AuthUser


SATISFACTION_LEVELS = (
    ('great', 'Satisfied'),
    ('can_improve', 'Can be improved'),
    ('not_satisfied', 'Not satisfied'),
    ('dont_know', 'I don\'t know'),
)

FEATURE_RELEVANT = (
    ('tutorials', 'Tutorials'),
    ('books', 'Books'),
    ('spots', 'Spots'),
    ('profiles', 'Profiles'),
    ('timeline', 'Timeline'),
)

FEATURE_IRRELEVANT = FEATURE_RELEVANT

FEATURE_SUGGESTED = (
    ('code_snippets', 'Code snippets'),
    ('questions', 'Questions'),
    ('communities', 'Communities'),
    ('jobs', 'Jobs'),
)


# Report: stores the feedback reports from users
class Report(models.Model):
    """
    Database [feedback.report]
    """
    user = models.OneToOneField(AuthUser, primary_key=True)

    # Satisfaction levels
    satisfaction_general = models.CharField(
        max_length=16,
        blank=False,
        default=None,

        choices=SATISFACTION_LEVELS,

        verbose_name="General Satisfaction",
        help_text="How are you satisfied of Waaave in general?",
    )

    satisfaction_design = models.CharField(
        max_length=16,
        blank=False,
        default=None,

        choices=SATISFACTION_LEVELS,

        verbose_name="Design Satisfaction",
        help_text="How are you satisfied with Waaave design?",
    )

    satisfaction_usability = models.CharField(
        max_length=16,
        blank=False,
        default=None,

        choices=SATISFACTION_LEVELS,

        verbose_name="Usability Satisfaction",
        help_text="Is it easy enough to use Waaave?",
    )

    satisfaction_speed = models.CharField(
        max_length=16,
        blank=False,
        default=None,

        choices=SATISFACTION_LEVELS,

        verbose_name="Speed Satisfaction",
        help_text="Is the Waaave website fast enough?",
    )

    satisfaction_mobile = models.CharField(
        max_length=16,
        blank=False,
        default=None,

        choices=SATISFACTION_LEVELS,

        verbose_name="Mobile Satisfaction",
        help_text="Is your Waaave mobile experience good?",
    )

    satisfaction_search = models.CharField(
        max_length=16,
        blank=False,
        default=None,

        choices=SATISFACTION_LEVELS,

        verbose_name="Search Satisfaction",
        help_text="How is your search experience on Waaave?",
    )

    # Feature choices
    feature_relevant = models.CharField(
        max_length=16,
        blank=False,
        default=None,

        choices=FEATURE_RELEVANT,

        verbose_name="Most Relevant Feature",
        help_text="What's the most relevant feature on Waaave?",
    )

    feature_irrelevant = models.CharField(
        max_length=16,
        blank=False,
        default=None,

        choices=FEATURE_IRRELEVANT,

        verbose_name="Less Relevant Feature",
        help_text="What's the less relevant feature on Waaave?",
    )

    feature_suggested = models.CharField(
        max_length=16,
        blank=False,
        default=None,

        choices=FEATURE_SUGGESTED,

        verbose_name="Suggested Feature",
        help_text="What's the feature we should add?",
    )

    feature_ideas = models.TextField(
        blank=True,
        null=True,

        verbose_name="Personal Feature Ideas",
        help_text="Tell us which features you'd want to see in Waaave.",
    )

    # Custom message reports
    custom_message = models.TextField(
        blank=True,
        null=True,

        verbose_name="Feedback Message",
        help_text="Tell us anything you want now, feel free to write anything you want there.",
    )

    date_update = models.DateTimeField(auto_now=True)
    date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'Feedback Report > %s %s' % (self.user.first_name, self.user.last_name)


# Invite: stores the feedback invites to users
class Invite(models.Model):
    """
    Database [feedback.invite]
    """
    user = models.OneToOneField(AuthUser, primary_key=True)

    is_invited = models.BooleanField(default=False)

    date_update = models.DateTimeField(auto_now=True)
    date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'Feedback Invite > %s %s' % (self.user.first_name, self.user.last_name)
