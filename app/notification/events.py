from django.core.urlresolvers import reverse

from _commons.helpers.events import EventsHelper


class NotificationEvent(object):
    """
    An helper on notification events
    """

    @staticmethod
    def push(user, notif_type, notif_id):
        """
        Push the provided notification to the user channel
        """
        assert notif_type is not None and notif_id is not None
        
        EventsHelper.send(
            {
                'type': 'notification',
                'data': {
                    'url': reverse('notification.views.fetch_single', kwargs={
                        'notif_type': notif_type,
                        'notif_id': notif_id,
                    }),
                }
            },

            user=user
        )
