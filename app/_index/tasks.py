import logging
from celery import task

from haystack.management.commands import update_index as haystack_update_index


logger = logging.getLogger('celery.task')


@task
def update_index():
    """
    Proceed the index update
    """
    logger.info('Updating index...')

    haystack_update_index.Command().handle(remove=True)
    
    logger.info('Index updated.')