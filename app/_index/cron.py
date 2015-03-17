from django_cron import CronJobBase, Schedule

from .tasks import update_index as task_update_index


class UpdateIndexCronJob(CronJobBase):
    """
    Job to update the indexed content (with fresh data pulled from database)
    """
    RUN_EVERY_MINS = 20
    MIN_NUM_FAILURES = 5

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = '_index.update'

    def do(self):
        task_update_index()
