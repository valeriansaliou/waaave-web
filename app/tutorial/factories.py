from django.db.models.query import QuerySet

from _commons.helpers.statuses import StatusesHelper
from _commons.helpers.cache import CacheHelper

from timeline.factories import BaseTimelineFactory

from .helpers.process import *
from .models import *


class RelatedFactory(BaseTimelineFactory):
    """
    Builds tutorial related data
    """
    
    def __init__(self, instance, fetch_type):
        super(RelatedFactory, self).__init__()

        self.__instance = instance
        self.__fetch_type = fetch_type

        self.__tutorial_ids = []
        self.__user_ids = []

        self._prepare()


    def __fetch_item(self, filtered, verbose):
        """
        Fetch the given timeline item
        """
        items = []

        if not isinstance(filtered, QuerySet):
            filtered = [filtered]

        for cur_filtered in filtered:
            can_append = True

            if self.__fetch_type == 'developers':
                cur_user_id = cur_filtered.author_set.filter(is_master=True).first().user_id

                if cur_user_id in self.__user_ids:
                    can_append = False
                else:
                    self.__user_ids.append(cur_user_id)

            if can_append:
                items.append({
                    'type': verbose,
                    'id': cur_filtered.id,
                    'date': cur_filtered.date,
                })

        return items


    def __fetch_same_tags(self):
        """
        Fetch the tutorials that are tagged the same
        """
        tutorial_list = []

        # List tags of this tutorial (reverse)
        for cur_tag in self.__instance.tutorial_tags.all():
            for cur_rel_tag in cur_tag.tag.tutorial_tag_list.exclude(tutorial_id=self.__instance.id):
                if cur_rel_tag.tutorial.is_visible():
                    fetched_items = self.__fetch_item(
                        cur_rel_tag.tutorial,
                        'tutorial'
                    )

                    for cur_tutorial in fetched_items:
                        if not cur_tutorial['id'] in self.__tutorial_ids:
                            self.__tutorial_ids.append(cur_tutorial['id'])
                            tutorial_list.append(cur_tutorial)

        return tutorial_list


    def _fetch(self):
        """
        Fetch the whole activity of a user
        """

        namespace = CacheHelper.ns('tutorial:factories:related:_fetch', fetch_type=self.__fetch_type)
        fetch_data = CacheHelper.io.get(namespace)

        if fetch_data is None:
            fetch_data = []

            fetch_data += self.__fetch_same_tags()

            CacheHelper.io.set(namespace, fetch_data)

        return fetch_data


    def __generate_tutorials(self, tutorial_id):
        """
        Generate the tutorials data
        """
        tutorial_data = {}

        cur_tutorial_meta = Meta.objects.get(id=tutorial_id)
        cur_tutorial_author = cur_tutorial_meta.author_set.filter(is_master=True).first()

        tutorial_data = {
            'tutorial_id': cur_tutorial_meta.id,
            'user_id': cur_tutorial_author.user_id,
            'type': 'tutorial',
            'date': cur_tutorial_author.date,
            
            'data': ProcessHelper.generate_data(
                tutorial=cur_tutorial_meta,
                author=cur_tutorial_author,
            ),
        }

        return tutorial_data


    def _generate(self, start=0, end=None):
        """
        Generate the whole timeline data
        """
        namespace = CacheHelper.ns('tutorial:factories:related:_generate', fetch_type=self.__fetch_type, start=start, end=end)
        related = CacheHelper.io.get(namespace)

        if related is None:
            related = []

            for cur_related in self._timeline[start:end]:
                if cur_related['type'] == 'tutorial':
                    related.append(self.__generate_tutorials(cur_related['id']))
                else:
                    raise Exception("Unknown Model Generator")

            CacheHelper.io.set(namespace, related)

        return related
