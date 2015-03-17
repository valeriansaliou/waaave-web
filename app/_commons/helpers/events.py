import redis, json
from datetime import datetime

from django.conf import settings
#from django.contrib.sessions.models import Session


class EventsHelper(object):
    """
    An helper on events operations
    """

    redis_broker = redis.StrictRedis(
        host=settings.REDIS['host'],
        port=settings.REDIS['port'],
        db=settings.REDIS['db']
    )

    @classmethod
    def send(_class, data, user=None):
        """
        Send some data to a channel
        """
        is_private = (user is not None)
        channel = ('private' if is_private else 'public')

        payload = {
            'auth': {
                'has': is_private
            },

            'data': data
        }

        if is_private:
            payload['auth']['user'] = user.id

        payload = json.dumps(payload)

        _class.redis_broker.publish(channel, payload)
