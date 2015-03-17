from django_cron import CronJobBase, Schedule

from .tasks import update_avatars as task_update_avatars


class UpdateAvatarCronJob(CronJobBase):
    """
    Job to update the expired user avatars
    """
    RUN_EVERY_MINS = 15
    MIN_NUM_FAILURES = 1

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'avatar.update'

    def do(self):
        task_update_avatars()
