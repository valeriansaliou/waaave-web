from datetime import datetime

from _commons.helpers.statuses import StatusesHelper
from _commons.helpers.types import TypesHelper
from _commons.helpers.rank import RankHelper
from _commons.helpers.cache import CacheHelper

from rank.helpers import RankProcessHelper
from _index.models import Ids as _IndexIds

from notification.factories import PushFollowAddNotificationFactory

from .models import *
from .emails import *


class TutorialModerator(object):
    """
    Moderates a provided tutorial
    """

    def __init__(self, request, tutorial):
        self.__request = request
        self.__tutorial = tutorial
        self.__tutorial_author = self.__tutorial.author_set.filter(is_master=True).first()
        self.__tutorial_url = self.__tutorial.url_set.filter(is_alias=False).first()


    def __is_allowed(self):
        """
        Checks if user is allowed to moderate
        """
        return self.__request.user.is_staff


    def __decrement_counter_cache(self):
        try:
            CacheHelper.io.decr(
                CacheHelper.ns('tutorial:helpers:read:count_unmoderated', self.__request.user)
            )
        except ValueError:
            pass


    def __proceed(self, status, moderation_message):
        """
        Proceeds tutorial moderation
        """
        assert status == 'accepted' or status == 'refused'

        if not self.__is_allowed():
            return False

        # Proceed acceptance jobs
        if status == 'accepted':
            # Notify all followers about this
            PushFollowAddNotificationFactory(request=self.__request, user=self.__tutorial_author.user).set(
                _IndexIds.objects.get(
                    item_id=self.__tutorial.id,
                    item_type=TypesHelper.encode('tutorial'),
                )
            )

            if not self.__tutorial.publish_date:
                self.__tutorial.publish_date = datetime.now()

            # Create the record and upgrade experience
            RankProcessHelper.create(
                self.__tutorial_author.user.profile,
                None, # Keep None (do not assign the moderator profile because of the cancel below)
                [self.__tutorial.id, 'tutorial'],
                RankHelper.get_action_by_name('tuto_validation'),
            )
        elif status == 'refused':
            # check if the tutorial was previously accepted and cancel the record if required
            if self.__tutorial.status == StatusesHelper.encode('accepted'):
                RankProcessHelper.cancel(
                    self.__tutorial_author.user.profile,
                    None,
                    [self.__tutorial.id, 'tutorial'],
                    RankHelper.get_action_by_name('tuto_validation'),
                )
        
        # Apply new moderation status
        self.__tutorial.status = StatusesHelper.encode(status)
        self.__tutorial.moderation_message = moderation_message or ''
        self.__tutorial.save()

        # Decrement cached notification counter
        self.__decrement_counter_cache()

        # Send notification email
        tutorial_moderated_email(
            self.__request,
            
            status,
            moderation_message,

            self.__tutorial_author.user.email,
            self.__tutorial.id,
            self.__tutorial.title,
            self.__tutorial_url.tag,
            self.__tutorial_url.slug,
        )

        return True


    def pending(self):
        """
        Sets tutorial moderation status to 'pending'
        """
        status_moderated_num = StatusesHelper.encode('moderated')

        if self.__tutorial.status <= status_moderated_num:
            self.__tutorial.status = status_moderated_num
            self.__tutorial.save()


    def accept(self, moderation_message):
        """
        Sets tutorial moderation status to 'accepted'
        """
        return self.__proceed('accepted', moderation_message)
    

    def refuse(self, moderation_message):
        """
        Sets tutorial moderation status to 'refused'
        """
        return self.__proceed('refused', moderation_message)
