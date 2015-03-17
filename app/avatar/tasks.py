import logging
from celery import task


logger = logging.getLogger('celery.task')


@task
def update_avatars():
    """
    Proceed the avatars update
    """
    from helpers import AvatarHelper

    expired = AvatarHelper.list_expired(sources=['gravatar', 'url'])

    if expired:
        logger.info('There are %s expired avatar(s) to update.' % len(expired))

        for binding in expired:
            user = binding.user

            try:
                logger.info('Updating avatar for user: %s...' % user.username)

                AvatarHelper.update(user, binding.source)

                logger.info('Updated avatar for user: %s.' % user.username)
            except Exception as e:
                logger.error('Error while updating avatar for user: %s (%s)' % (user.username, e))
                continue
    else:
        logger.info('No avatar to update. Yay!')
