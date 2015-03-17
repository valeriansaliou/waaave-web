from django.conf import settings

from _commons.helpers.numbers import cached_randint

from security.defaults import is_register_complete, user_confirmed
from notification.helpers import NotificationHelper
from moderation.helpers import ModerationHelper

from account.helpers import UserHelper as AccountUserHelper
from book.helpers import BookHelper
from tutorial.helpers.read import ReadHelper as TutorialReadHelper
from spot.helpers import SpotHelper


def sidebar_left(request):
    """
    Return the left sidebar values in context
    """
    if request.user.is_authenticated():
        moderation_obj = {
            'is_visible': False,
            'count_notifs': 0,
        }

        if request.user.is_staff:
            moderation_obj['is_visible'] = True
            moderation_obj['count_notifs'] = ModerationHelper.count_unmoderated(request.user)

        return {
            'sidebar_left': {
                'moderation': moderation_obj,
            },
        }
    
    return {}


def sidebar_right(request):
    """
    Return the right sidebar values in context
    """
    user = request.user if request.user.is_authenticated() else None

    sidebar_right_data = {
        # Suggestion data
        'waaavers': AccountUserHelper.suggestions(user, maximum=3, ignore_user=user),
        'tutorials': TutorialReadHelper.suggestions(user, maximum=3),
        'books': BookHelper.suggestions(user, maximum=2),
        'spots': SpotHelper.suggestions(user, maximum=2),

        # Suggestion context
        'context': {
            'variant': cached_randint(1, 2, 30),
        },
    }

    # Optimize variant context data (in case the chosen variant has no data)
    if sidebar_right_data['context']['variant'] is 1\
       and not sidebar_right_data['waaavers']:
       sidebar_right_data['context']['variant'] = 2

    if sidebar_right_data['context']['variant'] is 2\
       and not sidebar_right_data['spots']:
       sidebar_right_data['context']['variant'] = 1

    return {
        'sidebar_right': sidebar_right_data,
    }


def notification(request):
    """
    Return the user notification in context
    """
    if request.user.is_authenticated():
        return {
            'notification': {
                'count_new': NotificationHelper.count_new(request.user),
            },
        }

    return {}


def alert(request):
    """
    Return the user alert status in context
    """
    alert_id, alert_data = None, None

    if request.user.is_authenticated():
        # Get alert ID
        alert_id = request.session.get('alert', None)
        alert_id_session = alert_id

        if not alert_id:
            if not user_confirmed(request):
                alert_id = 'confirm_pending_resent'\
                           if (alert_id_session == 'confirm_pending_resent')\
                           else 'confirm_pending'

        # Get alert data
        alert_data = request.session.get('alert_data')

        # Clean alert values
        if 'alert' in request.session:
            del request.session['alert']
        if 'alert_data' in request.session:
            del request.session['alert_data']
    else:
        alert_id = 'user_register_invite'

    return {
        'alert': alert_id,
        'alert_data': alert_data,
    }


def conf(request):
    """
    Return the settings in context
    """
    return {
        'conf': settings,
    }
