from _commons.helpers.cache import CacheHelper
from _commons.helpers.types import TypesHelper
from _commons.helpers.numbers import percentage_of
from _commons.helpers.rank import RankHelper
from _index.helpers import ContentHelper

from comment.models import Active as CommentActive
from account.models import Profile as AccountProfile
from tutorial.helpers.process import ProcessHelper as TutorialProcessHelper
from rank.helpers import RankProcessHelper

from .models import *


class RelevanceHelper(object):
    """
    An helper on relevance operations
    """

    @staticmethod
    def __base_relevance_data():
        """
        Returns base relevance data object
        """
        return {
            'count_relevant': 0,
            'count_irrelevant': 0,
            'has_relevant': False,
            'has_irrelevant': False,
        }


    @classmethod
    def __read(_class, item, user=None):
        """
        Read an item's relevance
        """
        uid = user.id if user and user.is_authenticated() else None

        namespace = CacheHelper.ns('relevance:helpers:__read', item_id=item.id, uid=uid)
        relevance_data = CacheHelper.io.get(namespace)

        if relevance_data is None:
            record = Record.objects.filter(item=item)

            relevant = record.filter(is_relevant=True)
            irrelevant = record.filter(is_relevant=False)

            relevance_data = _class.__base_relevance_data()

            relevance_data['count_relevant'] = relevant.count()
            relevance_data['count_irrelevant'] = irrelevant.count()
            relevance_data['has_relevant'] = uid and relevant.filter(user_id=uid).exists()
            relevance_data['has_irrelevant'] = uid and irrelevant.filter(user_id=uid).exists()

            CacheHelper.io.set(namespace, relevance_data)

        return relevance_data


    @staticmethod
    def __update_rank(user, item, record):
        """
        Update rank according to new relevance
        """
        recipient, sender, entity = None, None, None
        action = RankHelper.get_action_by_name('click_relevant')\
                  if record.is_relevant\
                  else RankHelper.get_action_by_name('click_irrelevant')

        # Get rank data according to item type
        if item.item_type == TypesHelper.encode('tutorial'):
            try:
                recipient = AccountProfile.objects.get(
                    user_id=TutorialProcessHelper.author(item.item_id)
                )
            except AccountProfile.DoesNotExist:
                pass
        elif item.item_type == TypesHelper.encode('comment'):
            try:
                recipient = CommentActive.objects.get(id=item.item_id).author.profile
            except CommentActive.DoesNotExist:
                pass

        sender = user.profile
        entity = [item.item_id, TypesHelper.reverse(item.item_type)]

        if recipient and sender and entity:
            # Cancel the record and update experience
            if not record or not record.is_relevant:
                RankProcessHelper.cancel(
                    recipient,
                    sender,
                    entity,
                    action,
                )
            else:
                # Create the record and update experience
                RankProcessHelper.create(
                    recipient,
                    sender,
                    entity,
                    action,
                )


    @classmethod
    def get(_class, item_type, item_id, user=None):
        """
        Get relevance data
        """
        index = ContentHelper.get(item_id, item_type)

        if index:
            relevance_data = _class.__read(index, user)
        else:
            relevance_data = _class.__base_relevance_data()

        relevance_data.update({
            'percent_relevant': percentage_of(
                relevance_data['count_relevant'],
                relevance_data['count_irrelevant'],
            )
        })

        return relevance_data


    @classmethod
    def update(_class, user, item, value):
        """
        Save relevance data
        """
        # Update relevance
        record = Record.objects.get_or_create(
            item=item,
            user=user,
            defaults={
                'is_relevant': (value != 'relevant' and True),
            },
        )[0]

        # Remove our relevance choice?
        if record.is_relevant is (value == 'relevant'):
            record.delete()
        else:
            record.is_relevant = (value == 'relevant' and True)
            record.save()

        # Update associated rank
        _class.__update_rank(user, item, record)

        return record
