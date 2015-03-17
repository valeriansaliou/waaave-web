from django.core.urlresolvers import reverse

from _commons.helpers.statuses import StatusesHelper
from _commons.helpers.fields import FieldsHelper
from _commons.helpers.cache import CacheHelper

from ..helpers.process import ProcessHelper
from ..models import *



class ReadHelper(object):
    """
    An helper on read operations
    """

    @staticmethod
    def list(request, list_filter):
        """
        List some tutorials
        """
        tutorial_list = []
        status_counters = {}

        # Read filter
        tut_matches = []

        if list_filter == 'author':
            db_author = Author.objects.filter(user=request.user, is_master=True)

            for cur_db_author in db_author.iterator():
                tut_matches.append(cur_db_author.tutorial)
        elif list_filter == 'unmoderated':
            tut_matches = [c for c in Meta.objects.filter(is_online=True).order_by('-status', 'date')]

        # Append data
        for cur_tutorial in tut_matches:
            try:
                cur_db_user = cur_tutorial.author_set.filter(is_master=True).first().user
                cur_db_url = cur_tutorial.url_set.filter(is_alias=False).first()

                status_tpl = StatusesHelper.reverse(cur_tutorial.status)

                # Increment status counters
                if not status_tpl[0] in status_counters:
                    status_counters[status_tpl[0]] = 1
                else:
                    status_counters[status_tpl[0]] += 1

                tutorial_list.append({
                    'id': cur_tutorial.id,
                    'is_online': cur_tutorial.is_online and status_tpl[0] == 'accepted',
                    'is_pending': (cur_tutorial.is_online and status_tpl[0] == 'none') or status_tpl[0] == 'moderated',
                    'date_edit': cur_tutorial.content.date,

                    'author': {
                        'user_id': cur_db_user.id,
                        'username': cur_db_user.username,
                        'first_name': cur_db_user.first_name,
                        'last_name': cur_db_user.last_name,
                    },

                    'title': {
                        'full': cur_tutorial.title,
                        'slug': cur_db_url.slug,
                    },

                    'tag': {
                        'short': cur_db_url.tag,
                        'full': cur_db_url.tag,
                    },

                    'status': {
                        'short': status_tpl[0],
                        'full': status_tpl[1],
                    },
                })
            except AttributeError:
                continue

        # Sort by date
        tutorial_list = sorted(tutorial_list, key=lambda k: k['date_edit'], reverse=True)

        return (tutorial_list,status_counters,)


    @staticmethod
    def list_with_tag(tag):
        """
        Return the tutorials that are tagged with provided tag
        """
        return [t.tutorial for t in Tag.objects.filter(tag=tag) if t.tutorial.is_visible()]


    @staticmethod
    def status(tutorial_id=None):
        """
        Return the validation status of a tutorial
        """
        value = 'none'

        try:
            value = StatusesHelper.reverse(
                Meta.objects.get(id=tutorial_id).status
            )[0]
        except Meta.DoesNotExist:
            pass
        finally:
            return value


    @staticmethod
    def count_unmoderated(user):
        """
        Return the number of unmoderated tutorials
        """
        namespace = CacheHelper.ns('tutorial:helpers:read:count_unmoderated', user)
        count = CacheHelper.io.get(namespace)

        if count is None:
            count = Meta.objects.filter(is_online=True, status=StatusesHelper.encode('unmoderated')).count()
            CacheHelper.io.set(namespace, count, 60)

        return count


    @staticmethod
    def suggestions(user, maximum=1):
        """
        Suggests a set of tutorials
        """
        # Prevents circular imports
        from relevance.helpers import RelevanceHelper
        
        namespace = CacheHelper.ns('tutorial:helpers:read:suggestions', user, maximum=maximum)
        results = CacheHelper.io.get(namespace)

        if results is None:
            results = []
            filtered = Meta.objects.filter(is_online=True, status=StatusesHelper.encode('accepted'))

            for tutorial in FieldsHelper.random(filtered, maximum):
                try:
                    results.append({
                        'meta': tutorial,
                        'url': tutorial.url_set.filter(is_alias=False).first(),
                        'author': tutorial.author_set.filter(is_master=True).first().user,
                        'relevance': RelevanceHelper.get('tutorial', tutorial.id)['percent_relevant'],
                        'views': ProcessHelper.views(tutorial),
                    })
                except AttributeError:
                    continue

            CacheHelper.io.set(namespace, results, 60)

        return results


    @staticmethod
    def random_for_author(user, number=1):
        """
        Retrieves a random tutorial written by provided user
        """
        results = []

        tutorial_author = FieldsHelper.random(
            model=Author.objects.filter(user_id=user.id),
            number=1,
        )
        
        for cur_tutorial_author in tutorial_author:
            cur_tutorial = cur_tutorial_author.tutorial

            if cur_tutorial.is_visible():
                results.append(
                    ProcessHelper.generate_data(
                        tutorial=cur_tutorial,
                        author=cur_tutorial_author,
                    )
                )
        
        return results
