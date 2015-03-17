from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User as AuthUser

from _commons.helpers.types import TypesHelper
from _commons.helpers.cache import CacheHelper

from tutorial.helpers.process import ProcessHelper as TutorialProcessHelper

from .models import *



class NotificationHelper(object):
    """
    An helper on notification operations
    """

    @staticmethod
    def get_tutorial_data(tutorial_id):
        """
        Returns notification data for a tutorial
        """
        return {
            'url': TutorialProcessHelper.url(tutorial_id),
            'url_full': TutorialProcessHelper.url_full(tutorial_id),
            'title': TutorialProcessHelper.title(tutorial_id),
            'author': AuthUser.objects.get(id=TutorialProcessHelper.author(tutorial_id)),
        }


    @staticmethod
    def get_book_data(book_id):
        """
        Returns notification data for a book
        """
        from book.helpers import BookHelper
        
        book = BookHelper.resolve(book_id)

        return {
            'url': BookHelper.url(book) if book else None,
            'url_full': BookHelper.url_full(book) if book else None,
            'title': BookHelper.title(book) if book else None,
        }


    @classmethod
    def get_item_data(_class, item_type, item_id):
        """
        Returns generated item data
        """
        item_data = {
            'url': None,
            'url_full': None,
            'title': None,
        }

        item_type_humanized = TypesHelper.reverse(item_type)

        if item_type_humanized == 'tutorial':
            item_data = _class.get_tutorial_data(tutorial_id=item_id)
        elif item_type_humanized == 'book':
            item_data = _class.get_book_data(book_id=item_id)

        if not item_data['url'] or not item_data['title']:
            return None, None

        return item_type_humanized, item_data


    @staticmethod
    def filter_models(user):
        """
        Returns the filtered notification querysets for given user
        """
        return {
            'comment': Comment.objects.filter(user=user),
            'spot': Spot.objects.filter(user=user),
            'waaave': Waaave.objects.filter(user=user),
            'follow': Follow.objects.filter(user=user),
            'follow-add': FollowAdd.objects.filter(user=user),
        }


    @classmethod
    def count_new(_class, user):
        """
        Counts the number of new (unread) notifications
        """
        namespace = CacheHelper.ns('notification:helpers:count_new', user)
        count = CacheHelper.io.get(namespace)

        if count is None:
            count = 0

            for _, cur_filter in _class.filter_models(user).iteritems():
                count += cur_filter.filter(is_new=True, is_active=True).count() or 0

            CacheHelper.io.set(namespace, count)

        return count


    @classmethod
    def normalize_type(_class, notif_type):
        """
        Normalize notification type (some types are just aliases of others)
        """
        if notif_type == 'response':
            return 'comment'
        
        return notif_type


    @staticmethod
    def ns_cached_namespace(user):
        """
        Returns the cached namespace for given user
        """
        return CacheHelper.ns('notification:helpers:ns_cached_namespace', user)


    @classmethod
    def get_cached_namespace(_class, user):
        """
        Get all cached namespaces in the register for given user
        """
        return CacheHelper.io.get(
            _class.ns_cached_namespace(user)
        ) or set()


    @classmethod
    def set_cached_namespace(_class, user, namespace):
        """
        Adds a cached namespace to the register for given user
        """
        caches = _class.get_cached_namespace(user)
        caches.add(namespace)

        CacheHelper.io.set(
            _class.ns_cached_namespace(user),
            caches
        )


    @classmethod
    def purge_cached_namespace(_class, user):
        """
        Purges all cached namespaces for given user
        """
        CacheHelper.io.delete(
            _class.ns_cached_namespace(user)
        )


    @classmethod
    def mark_read_all(_class, user):
        """
        Mark all notifications as read
        """
        # Reset new counter cache
        CacheHelper.io.set(
            CacheHelper.ns('notification:helpers:count_new', user),
            0
        )

        result = 0

        try:
            for _, cur_filter in _class.filter_models(user).iteritems():
                result += cur_filter.filter(is_new=True).update(is_new=False)
        except ObjectDoesNotExist:
            pass
        finally:
            return result


    @classmethod
    def mark_read_single(_class, user, notif_type, notif_id):
        """
        Mark a single notification as read
        """
        result = False

        try:
            notif_models = _class.filter_models(user)
            notif_type = _class.normalize_type(notif_type)

            assert notif_type in notif_models

            if notif_models[notif_type].filter(id=notif_id, is_new=True).update(is_new=False) > 0:
                result = True
        except ObjectDoesNotExist:
            pass
        
        # Decrement new counter cache
        if result:
            try:
                CacheHelper.io.decr(
                    CacheHelper.ns('notification:helpers:count_new', user)
                )
            except ValueError:
                pass

        return result


    @classmethod
    def build_response_page(_class, request, page=1, items_per_page=10):
        """
        Builds the follow timeline response
        """
        from .factories import *

        notification_feed, has_show_more = ReadNotificationFactory(user=request.user).get(
            page=page,
            items_per_page=items_per_page,
        )

        response_data = {
            'notification_feed': notification_feed,
            'has_show_more': has_show_more,
            'next_page': page + 1,
        }

        return response_data


    @classmethod
    def build_response_single(_class, request, notif_type, notif_id):
        """
        Builds the follow timeline response
        """
        from .factories import *

        notification_feed, _ = ReadNotificationFactory(
            user=request.user,
            notification_type=notif_type,
            notification_id=notif_id
        ).get()

        return {
            'notification_feed': notification_feed,
        }
