from datetime import datetime

from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify

from _commons.helpers.cache import CacheHelper
from _commons.helpers.levels import LevelsHelper
from _commons.helpers.types import TypesHelper
from _commons.helpers.statuses import StatusesHelper

from _index.models import Ids as _IndexIds

from tag.factories import *

from .helpers import *
from .models import *


class TutorialSaver(object):
    """
    Saves a provided tutorial to the database
    """

    def __init__(self, request, tutorial=None, tutorial_id=None):
        self.__request = request
        self.__tutorial = tutorial

        if not self.__tutorial and tutorial_id:
            self.__tutorial = Meta.objects.get(id=tutorial_id)


    def __gen_values(self, form):
        """
        Generates tutorial values
        """
        # Retrieve data
        data_ret = {
            'title': form.cleaned_data['title'],
            'tags': form.cleaned_data['tags'],
            'tag': form.cleaned_data['tags'][0][0],
            'online': form.cleaned_data['online'],
            'level': form.cleaned_data['level'],
            'content': form.cleaned_data['content'],
            'moderation_message': form.cleaned_data['moderation_message'],
        }

        # Encode data
        data_enc = {
            'level_num': LevelsHelper.encode(data_ret['level']),
            'type_num': TypesHelper.encode('tutorial'),
        }

        # Process data
        data_proc = {
            'title_slug': slugify(data_ret['title']),
        }

        data_ret.update(data_enc)
        data_ret.update(data_proc)

        return data_ret


    def __save_meta(self, values, first_save):
        """
        Save tutorial meta model
        """
        self.__tutorial.title = values['title']
        self.__tutorial.level = values['level_num']

        if not self.__tutorial.is_online and values['online']:
            self.__tutorial.publish_date = datetime.now()

        self.__tutorial.is_online = values['online']

        if first_save:
            self.__tutorial.status = StatusesHelper.encode('none')

        self.__tutorial.save()


    def __save_content(self, values, first_save):
        """
        Save tutorial content model
        """
        db_content = self.__tutorial.content if not first_save else Content()
        db_content.tutorial = self.__tutorial
        db_content.user = self.__request.user
        db_content.body = values['content']
        db_content.save()


    def __save_url(self, values):
        """
        Save tutorial URL model
        """
        # Url (current)
        db_url = Url.objects.get_or_create(
            tutorial=self.__tutorial,
            tag=values['tag'],
            slug=values['title_slug'],
        )[0]
        db_url.is_alias = False
        db_url.save()

        # Url (others)
        db_url_all = [c for c
                        in Url.objects.filter(tutorial=self.__tutorial, is_alias=False)
                        if not (c.tag == values['tag'] and c.slug == values['title_slug'])]

        for cur_db_url_all in db_url_all:
            # Tutorial has already been online: better set a redirect
            if self.__tutorial.publish_date:
                cur_db_url_all.is_alias = True
                cur_db_url_all.save()
            else:
                cur_db_url_all.delete()


    def __save_tag(self, values):
        """
        Save tutorial tag model
        """
        Tag.objects.filter(tutorial=self.__tutorial).delete()

        for cur_tag in values['tags']:
            cur_tag_factory = TagFactory(slug=cur_tag[0], uid=self.__request.user.id)
            cur_tag = cur_tag_factory.store({
                        'name': cur_tag[1],
                        'desc': 'Tagged %s' % cur_tag[1],
                      })

            if cur_tag:
                Tag(
                    tutorial=self.__tutorial,
                    tag=cur_tag,
                ).save()


    def __save_author_new(self):
        """
        Save tutorial author model
        """
        Author(
            tutorial=self.__tutorial,
            user=self.__request.user,
            is_master=True,
        ).save()


    def __save_index(self, values):
        """
        Save index model for tutorial
        """
        return _IndexIds.objects.get_or_create(
            item_id=self.__tutorial.id,
            item_type=values['type_num'],
        )[0]


    def __store_values(self, values):
        """
        Stores tutorial values
        """
        store_status, store_redirect = 'save_error', None
        first_save = False

        if not self.__tutorial:
            self.__tutorial = Meta()

            first_save = True
            store_status = 'save_done'
       
        else:
            # Get db objects
            if self.__request.user.is_staff or self.__request.user.is_superuser\
               or Author.objects.filter(tutorial=self.__tutorial, user=self.__request.user).exists():
                store_status = 'save_done'
            else:
                store_status = 'not_allowed'

        # Save DB data
        if store_status == 'save_done':
            # Update metas and indexes
            self.__save_meta(values, first_save)
            self.__save_index(values)

            # First save operations?
            if first_save:
                store_redirect = '%s?saved' % reverse('dashboard.views.tutorial_edit', kwargs={'tutorial_id': self.__tutorial.id})
                self.__save_author_new()

            # Update contents
            self.__save_content(values, first_save)
            self.__save_url(values)
            self.__save_tag(values)

        return store_status, store_redirect


    def __purge_cache(self, tag, slug):
        """
        Delete tutorial cache
        """
        namespaces = [
            CacheHelper.ns('tutorial:views:view', tag=tag, slug=slug),
            CacheHelper.ns('tutorial:views:view_related_tutorials', tag=tag, slug=slug),
            CacheHelper.ns('tutorial:views:view_related_developers', self.__request.user, tag=tag, slug=slug),
        ]

        for namespace in namespaces:
            CacheHelper.io.delete(namespace)


    def save(self, form):
        """
        Saves tutorial values
        """
        # Generate values
        values = self.__gen_values(form)

        # Check URL availability
        try:
            db_url_check = Url.objects.get(
                tag=values['tag'],
                slug=values['title_slug'],
            )

            if not self.__tutorial or db_url_check.tutorial_id != self.__tutorial.id:
                return 'namespace_unavailable', None
        except Url.DoesNotExist:
            pass

        # Purge caches
        self.__purge_cache(values['tag'], values['title_slug'])

        # Store values in DB (we're GTG!)
        return self.__store_values(values)


    def remove(self):
        """
        Removes tutorial values
        """
        result = []

        try:
            garbage = [
                self.__tutorial,
                _IndexIds.objects.get(item_id=self.__tutorial.id, item_type=TypesHelper.encode('tutorial')),
            ]

            for cur_garbage in garbage:
                cur_garbage.delete()
                result.append(1)

            # Purge caches
            self.__purge_cache(self.__tutorial.tag, self.__tutorial.slug)
        except (Meta.DoesNotExist, _IndexIds.DoesNotExist):
            pass
        finally:
            return result
