import logging
from datetime import datetime, timedelta

from django_cron import CronJobBase, Schedule
from django.contrib.auth.models import User as AuthUser

from models import *
from emails import *


logger = logging.getLogger('django.cron')


class InviteFeedbackCronJob(CronJobBase):
    """
    Job to update the expired user avatars
    """
    RUN_EVERY_MINS = 60
    MIN_NUM_FAILURES = 1

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'feedback.invite'


    def __invite_user(self, user):
        invite = Invite.objects.get_or_create(
            user=user
        )[0]

        if invite.is_invited is False:
            invite.is_invited = True
            invite.save()
            invite_email(user)

            logger.info('Feedback invite: %s' % user)

            return 1

        return 0


    def do(self):
        logger.info('Checking for users to invite for feedback...')

        count = 0

        for user in AuthUser.objects.all():
            # Don't invite new users too early (wait 2 days)
            if (datetime.now() - user.date_joined) > timedelta(days=2):
                try:
                    if user.report:
                        continue
                except Report.DoesNotExist:
                    count += self.__invite_user(user)

        logger.info('Invited {count} user{s} to feedback.'.format(
            count=count,
            s=('' if count is 1 else 's')
        ))
