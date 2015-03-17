from datetime import timedelta
from types import MethodType

from django.db.models.query import QuerySet
from django.contrib.auth.models import User as AuthUser

from _commons.helpers.types import TypesHelper
from _commons.helpers.cache import CacheHelper
from _index.helpers import ContentHelper as _IndexContentHelper
from tutorial.helpers.process import ProcessHelper as TutorialProcessHelper
from account.helpers import SettingsHelper
from share.helpers import FollowShareHelper

from _index.models import Ids as _IndexIds
from comment.models import Active as CommentActive
from share.models import Waaave as ShareWaaave
from share.models import Follow as ShareFollow
from tag.models import List as TagList

from timeline.factories import BaseTimelineFactory

from .models import *
from .helpers import *
from .emails import *
from .events import *


class ReadNotificationFactory(BaseTimelineFactory):
    """
    Interface to read notification data
    """
    
    def __init__(self, user, notification_type=None, notification_id=None):
        super(ReadNotificationFactory, self).__init__()

        self.__user = user
        self.__notification_type = notification_type
        self.__notification_id = notification_id

        if self.__notification_type and self.__notification_id:
            self.__prepare_single()
        else:
            self._prepare()


    def __generate_comment(self, cur_comment):
        """
        Generate a comment notification
        """
        assert cur_comment['type'] == 'comment'

        gen_comment = {}
        
        try:
            cur_comment_foreign = CommentActive.objects.get(id=cur_comment['comment_id'])

            item_type, item_data = NotificationHelper.get_item_data(cur_comment_foreign.item.item_type, cur_comment_foreign.item.item_id)
            if not item_data or not item_type: return

            gen_comment = {
                'type': ('response' if cur_comment_foreign.in_reply_to else 'comment'),
                'id': cur_comment['id'],
                'new': cur_comment['is_new'],
                'date': cur_comment['date'],

                'data': {
                    'user': cur_comment_foreign.author,
                    'comment': cur_comment_foreign,
                    'item_type': item_type,
                    'item_data': item_data,
                },
            }
        except CommentActive.DoesNotExist:
            pass
        finally:
            return gen_comment


    def __generate_spot(self, cur_spot):
        """
        Generate a spot notification
        """
        assert cur_spot['type'] == 'spot'

        gen_spot = {}

        try:
            cur_spot_tag = TagList.objects.get(id=cur_spot['spot_id'])
            cur_spot_foreign = _IndexIds.objects.get(id=cur_spot['index_id'])

            item_type, item_data = NotificationHelper.get_item_data(cur_spot_foreign.item_type, cur_spot_foreign.item_id)
            if not item_data or not item_type: return

            gen_spot = {
                'type': 'spot',
                'id': cur_spot['id'],
                'new': cur_spot['is_new'],
                'date': cur_spot['date'],

                'data': {
                    'spot': cur_spot_tag,
                    'item_type': item_type,
                    'item_data': item_data,
                },
            }
        except (TagList.DoesNotExist, _IndexIds.DoesNotExist):
            pass
        finally:
            return gen_spot


    def __generate_waaave(self, cur_waaave):
        """
        Generate a waaave notification
        """
        assert cur_waaave['type'] == 'waaave'

        data = []

        item_type, item_data = None, None

        for sub_waaave in cur_waaave['items']:
            try:
                sub_waaave_foreign = ShareWaaave.objects.get(id=sub_waaave['waaave_id'])
            except ShareWaaave.DoesNotExist:
                continue

            if not (item_type and item_data):
                item_type, item_data = NotificationHelper.get_item_data(sub_waaave_foreign.item.item_type, sub_waaave_foreign.item.item_id)

            data.append({
                'id': sub_waaave['id'],
                'date': sub_waaave['date'],
                'new': sub_waaave['is_new'],

                'data': {
                    'user': sub_waaave_foreign.user,
                },
            })

        if not (item_type and item_data): return

        return {
            'type': 'waaave',
            'id': cur_waaave['id'],
            'new': cur_waaave['is_new'],
            'date': cur_waaave['date'],
            'data': data,

            'meta': {
                'item_type': item_type,
                'item_data': item_data,
            }
        }


    def __generate_follow(self, cur_follow):
        """
        Generate a follow notification
        """
        assert cur_follow['type'] == 'follow'

        data = []

        for sub_follow in cur_follow['items']:
            try:
                sub_follow_foreign = ShareFollow.objects.get(id=sub_follow['follow_id'])
            except ShareFollow.DoesNotExist:
                continue

            data.append({
                'id': sub_follow['id'],
                'date': sub_follow['date'],
                'new': sub_follow['is_new'],

                'data': {
                    'user': sub_follow_foreign.follower,
                },
            })

        return {
            'type': 'follow',
            'id': cur_follow['id'],
            'new': cur_follow['is_new'],
            'date': cur_follow['date'],
            'data': data,
        }


    def __generate_follow_add(self, cur_follow_add):
        """
        Generate a follow add notification
        """
        assert cur_follow_add['type'] == 'follow-add'

        gen_follow_add = {}

        try:
            cur_follow_add_foreign = _IndexIds.objects.get(id=cur_follow_add['index_id'])

            item_type, item_data = NotificationHelper.get_item_data(cur_follow_add_foreign.item_type, cur_follow_add_foreign.item_id)
            if not item_data or not item_type: return

            gen_follow_add = {
                'type': 'follow-add',
                'id': cur_follow_add['id'],
                'new': cur_follow_add['is_new'],
                'date': cur_follow_add['date'],

                'data': {
                    'user': item_data['author'],
                    'item_type': item_type,
                    'item_data': item_data,
                },
            }
        except _IndexIds.DoesNotExist:
            pass
        finally:
            return gen_follow_add


    def _generate(self, start=0, end=None):
        """
        Generate the whole notifications
        """
        namespace = CacheHelper.ns('notification:factories:read:_generate', self.__user, start=start, end=end)
        notifications = CacheHelper.io.get(namespace)

        if notifications is None:
            notifications = []

            for cur_notification in self._timeline[start:end]:
                if cur_notification['type'] == 'comment':
                    notifications.append(self.__generate_comment(cur_notification))
                elif cur_notification['type'] == 'spot':
                    notifications.append(self.__generate_spot(cur_notification))
                elif cur_notification['type'] == 'waaave':
                    notifications.append(self.__generate_waaave(cur_notification))
                elif cur_notification['type'] == 'follow':
                    notifications.append(self.__generate_follow(cur_notification))
                elif cur_notification['type'] == 'follow-add':
                    notifications.append(self.__generate_follow_add(cur_notification))
                else:
                    raise Exception("Unknown Model Generator")

            CacheHelper.io.set(namespace, notifications)
            NotificationHelper.set_cached_namespace(self.__user, namespace)

        return notifications


    def _preprocess_unbuffer(self, buffer_type, buffer_items, buffer_date):
        """
        Preprocess the items buffered data
        """
        buffer_has_new = False

        for item in buffer_items:
            if item['is_new']:
                buffer_has_new = True
                break

        unbuffered = super(ReadNotificationFactory, self)._preprocess_unbuffer(buffer_type, buffer_items, buffer_date)
        unbuffered.update({
            'is_new': buffer_has_new,
        })

        return unbuffered


    def __modificator_waaaves(self, instance, item):
        """
        Modifies the waaave item data
        """
        item.update({
            'item_id': instance.waaave.item.id,
        })


    def _fetch_item(self, model, verbose, notification_id=None):
        """
        Fetch the given item notifications
        """
        filtered = model if isinstance(model, QuerySet) else model.objects

        if notification_id is not None:
            instance = filtered.filter(id=notification_id, user=self.__user, is_active=True)
            items = instance.values()
        else:
            instance = filtered.filter(user=self.__user, is_active=True)
            items = instance.values()

        for item in items:
            item.update({
                'type': verbose,
            })

        return instance, items


    def __fetch_comments(self, notification_id=None):
        """
        Fetch the comment notifications
        """
        _, fetched = self._fetch_item(
            model=Comment,
            verbose='comment',
            notification_id=notification_id,
        )

        return fetched


    def __fetch_spots(self, notification_id=None):
        """
        Fetch the spot notifications
        """
        _, fetched = self._fetch_item(
            model=Spot,
            verbose='spot',
            notification_id=notification_id,
        )

        return fetched


    def __fetch_waaaves(self, notification_id=None):
        """
        Fetch the waaave notifications
        """
        if notification_id is None:
            preprocessed = []

            fetched_groups = self._fetch_item_groups(
                model=Waaave,
                verbose='waaave',
                group_key='item_id',
                modificator=self.__modificator_waaaves,
            )

            for fetched in fetched_groups:
                preprocessed += self._preprocess(
                    items=fetched,
                    verbose='waaave',
                    date_threshold=timedelta(weeks=4)
                )

            return preprocessed

        _, fetched = self._fetch_item(
            model=Waaave,
            verbose='waaave',
            notification_id=notification_id,
        )

        if len(fetched):
            return [self._preprocess_unbuffer('waaave', fetched, fetched[0]['date'])]

        return []


    def __fetch_follows(self, notification_id=None):
        """
        Fetch the follow notifications
        """
        _, fetched = self._fetch_item(
            model=Follow,
            verbose='follow',
            notification_id=notification_id,
        )

        if notification_id is None:
            return self._preprocess(
                items=fetched,
                verbose='follow',
                date_threshold=timedelta(days=4)
            )

        if len(fetched):
            return [self._preprocess_unbuffer('follow', fetched, fetched[0]['date'])]

        return []


    def __fetch_follow_adds(self, notification_id=None):
        """
        Fetch the follow add notifications
        """
        _, fetched = self._fetch_item(
            model=FollowAdd,
            verbose='follow-add',
            notification_id=notification_id,
        )

        return fetched


    def _fetch(self):
        """
        Fetch the whole notifications
        """
        namespace = CacheHelper.ns('notification:factories:read:_fetch', self.__user)
        fetch_data = CacheHelper.io.get(namespace)

        if fetch_data is None:
            fetch_data = []

            fetch_data += self.__fetch_comments()
            fetch_data += self.__fetch_spots()
            fetch_data += self.__fetch_waaaves()
            fetch_data += self.__fetch_follows()
            fetch_data += self.__fetch_follow_adds()

            CacheHelper.io.set(namespace, fetch_data)
            NotificationHelper.set_cached_namespace(self.__user, namespace)

        return fetch_data


    def __fetch_single(self):
        """
        Fetch a single notification
        """

        fetch_data = []

        if self.__notification_type == 'comment'\
           or self.__notification_type == 'response':
            fetch_data += self.__fetch_comments(self.__notification_id)
        elif self.__notification_type == 'spot':
            fetch_data += self.__fetch_spots(self.__notification_id)
        elif self.__notification_type == 'waaave':
            fetch_data += self.__fetch_waaaves(self.__notification_id)
        elif self.__notification_type == 'follow':
            fetch_data += self.__fetch_follows(self.__notification_id)
        elif self.__notification_type == 'follow-add':
            fetch_data += self.__fetch_follow_adds(self.__notification_id)
        else:
            raise Exception("Unknown Notification Type")

        return fetch_data


    def __prepare_single(self):
        """
        Prepare notification data (single variant)
        """
        self._timeline += self.__fetch_single()



class PushNotificationFactory(object):
    """
    Interface to push (store) notification data
    """

    def __init__(self, request=None, user=None, target_user=None, item_id=None, item_type=None):
        self._request = request
        self._user = user or (request.user if request else None)
        self._target_user = target_user
        self._model = None
        self._item_id = item_id

        self._notification_type = None
        self._notification_id = None

        if item_type is None:
            self._item_type = None
        elif type(item_type) is int:
            self._item_type = item_type
        else:
            self._item_type = TypesHelper.encode(item_type)

        self._prepare(item_id, item_type)


    def _can_set(self):
        """
        Return whether the notification can be set or not
        """
        if self._has_target_user() and not self._same_user():
            return True

        return False


    def _can_unset(self):
        """
        Return whether the notification can be unset or not
        """
        return self._has_target_user()


    def _has_target_user(self):
        """
        Return whether the target user exists or not
        """
        return True if self._target_user else False


    def _same_user(self):
        """
        Return whether the notification targets us or not
        """
        if not self._user:
            return False

        if self._target_user:
            return True if (self._user.id == self._target_user.id) else False

        return True


    def _prepare(self, item_id, item_type):
        """
        Prepare initial data (if required)
        """
        if item_type and item_id and not self._target_user:
            _, target_user_id = _IndexContentHelper.validate(item_id, item_type)

            if target_user_id:
                self._target_user = AuthUser.objects.get(id=target_user_id)


    def _store(self, instance, is_active):
        """
        Store notification data
        """
        notification, initial = self._db(instance)

        if notification.is_active is not is_active:
            notification.is_active = is_active
            notification.save()

        self._purge_cache()

        return notification, initial


    def _signal(self):
        """
        Signal given notification (used for real-time client push)
        """
        assert self._notification_type is not None and self._notification_id is not None

        NotificationEvent.push(
            user=self._target_user,
            notif_type=self._notification_type,
            notif_id=self._notification_id,
        )


    def _counter_increment(self):
        """
        Increments user's notification counter
        """
        if self._target_user is not None:
            namespace = CacheHelper.ns('notification:helpers:count_new', self._target_user)

            try:
                CacheHelper.io.incr(namespace)
            except ValueError:
                CacheHelper.io.set(namespace, 1)


    def _purge_cache(self):
        """
        Purges notification cache for target user
        """
        if self._can_set():
            for namespace in NotificationHelper.get_cached_namespace(self._target_user):
                CacheHelper.io.delete(namespace)

            NotificationHelper.purge_cached_namespace(self._target_user)



class PushCommentNotificationFactory(PushNotificationFactory):
    """
    Interface to push (store) comment notification data
    """

    def __init__(self, request=None, user=None, target_user=None, item_id=None, item_type=None):
        super(PushCommentNotificationFactory, self).__init__(
            request=request,
            user=user,
            target_user=target_user,
            item_id=item_id,
            item_type=item_type,
        )

        self._model = Comment
    

    def __email(self, comment, notif_type):
        """
        E-Mail given notification
        """
        if self._item_type is None or self._item_id is None:
            raise Exception("Not Enough Data")

        item_type, item_data = NotificationHelper.get_item_data(self._item_type, self._item_id)

        if not item_data or not item_type:
            raise Exception("Not Enough Item Data")

        if notif_type == 'comment':
            comment_email(self._request, self._user, self._target_user, comment, item_data['url_full'])
        elif notif_type == 'response':
            response_email(self._request, self._user, self._target_user, comment, item_data['url_full'])
        else:
            raise Exception("Unknown Notification Type")


    def _db(self, comment):
        return self._model.objects.get_or_create(
            user_id=self._target_user.id,
            comment=comment,
        )


    def set(self, comment):
        """
        Write given notification
        """
        if not self._can_set(): return

        is_response = True if comment.in_reply_to else False

        has_notif = SettingsHelper.has_notif_respond(self._target_user.id)
        has_email = SettingsHelper.has_email_respond(self._target_user.id)

        notification, initial = self._store(
            instance=comment,
            is_active=has_notif,
        )

        self._notification_type = 'response' if is_response else 'comment'
        self._notification_id = notification.id

        if notification.is_new and initial:
            if has_notif:
                self._signal()
                self._counter_increment()

            if has_email:
                self.__email(
                    comment=comment,
                    notif_type=('response' if is_response else 'comment'),
                )


    def unset(self, comment):
        """
        Remove given notification
        """
        if not self._can_unset(): return

        self._store(
            instance=comment,
            is_active=False,
        )



class PushSpotNotificationFactory(PushNotificationFactory):
    """
    Interface to push (store) spot notification data
    """

    def __init__(self, target_user, spot):
        super(PushSpotNotificationFactory, self).__init__(
            target_user=target_user,
        )

        self.__spot = spot
        self._model = Spot


    def _db(self, index):
        return self._model.objects.get_or_create(
            user_id=self._target_user.id,
            spot=self.__spot,
            index=index,
        )


    def set(self, index):
        """
        Write given notification
        """
        if not self._can_set(): return

        has_notif = SettingsHelper.has_notif_spot(self._target_user.id)

        notification, initial = self._store(
            instance=index,
            is_active=has_notif,
        )

        self._notification_type = 'spot'
        self._notification_id = notification.id

        if notification.is_new and initial:
            if has_notif:
                self._signal()
                self._counter_increment()


    def unset(self, index):
        """
        Remove given notification
        """
        if not self._can_unset(): return

        self._store(
            instance=index,
            is_active=False,
        )



class PushWaaaveNotificationFactory(PushNotificationFactory):
    """
    Interface to push (store) waaave notification data
    """

    def __init__(self, request=None, target_user=None, item_id=None, item_type=None):
        super(PushWaaaveNotificationFactory, self).__init__(
            request=request,
            target_user=target_user,
            item_id=item_id,
            item_type=item_type,
        )

        self._model = Waaave


    def _db(self, waaave):
        return self._model.objects.get_or_create(
            user_id=self._target_user.id,
            waaave=waaave,
        )
    

    def set(self, waaave):
        """
        Write given notification
        """
        if not self._can_set(): return

        has_notif = SettingsHelper.has_notif_waaave(self._target_user.id)

        notification, initial = self._store(
            instance=waaave,
            is_active=has_notif,
        )

        self._notification_type = 'waaave'
        self._notification_id = notification.id

        if notification.is_new and initial:
            if has_notif:
                self._signal()
                self._counter_increment()


    def unset(self, waaave):
        """
        Remove given notification
        """
        if not self._can_unset(): return

        self._store(
            instance=waaave,
            is_active=False,
        )



class PushFollowNotificationFactory(PushNotificationFactory):
    """
    Interface to push (store) follow notification
    """

    def __init__(self, request, target_user):
        super(PushFollowNotificationFactory, self).__init__(
            request=request,
            target_user=target_user,
        )

        self._model = Follow


    def __email(self):
        """
        E-Mail given notification
        """
        follow_email(self._request, self._target_user)


    def _db(self, follow):
        return self._model.objects.get_or_create(
            user_id=self._target_user.id,
            follow=follow,
        )
    

    def set(self, follow):
        """
        Write given notification
        """
        if not self._can_set(): return

        has_notif = SettingsHelper.has_notif_follow(self._target_user.id)
        has_email = SettingsHelper.has_email_follow(self._target_user.id)

        notification, initial = self._store(
            instance=follow,
            is_active=has_notif,
        )

        self._notification_type = 'follow'
        self._notification_id = notification.id

        if notification.is_new and initial:
            if has_notif:
                self._signal()
                self._counter_increment()

            if has_email:
                self.__email()


    def unset(self, follow):
        """
        Remove given notification
        """
        if not self._can_unset(): return

        self._store(
            instance=follow,
            is_active=False,
        )



class PushFollowAddNotificationFactory(PushNotificationFactory):
    """
    Interface to push (store) follow add notification
    """

    def __init__(self, request, user=None):
        super(PushFollowAddNotificationFactory, self).__init__(
            request=request,
            user=(user or request.user),
        )

        self._model = FollowAdd
        self._target_user = None


    def __email(self, index):
        """
        E-Mail given notification
        """
        item_type_humanized = TypesHelper.reverse(index.item_type)
        item_type, item_data = NotificationHelper.get_item_data(index.item_type, index.item_id)

        if not item_data or not item_type:
            raise Exception("Not Enough Item Data")

        follow_add_email(
            request=self._request,
            user=self._target_user,
            item_type=item_type_humanized,
            item_title=item_data['title'],
            url_full=item_data['url_full'],
        )


    def _db(self, index):
        return self._model.objects.get_or_create(
            user_id=self._target_user.id,
            index=index,
        )
    

    def set(self, index):
        """
        Write given notification
        """
        for cur_target_user in FollowShareHelper.follow_users(self._user):
            self._target_user = cur_target_user

            if self._same_user(): continue

            has_notif = SettingsHelper.has_notif_follow_add(self._target_user.id)
            has_email = SettingsHelper.has_email_follow_add(self._target_user.id)

            notification, initial = self._store(
                instance=index,
                is_active=has_notif,
            )

            self._notification_type = 'follow-add'
            self._notification_id = notification.id

            if notification.is_new and initial:
                if has_notif:
                    self._signal()
                    self._counter_increment()

                if has_email:
                    self.__email(index)


    def unset(self, index):
        """
        Remove given notification
        """
        for cur_target_user in FollowShareHelper.follow_users(self._user):
            self._target_user = cur_target_user

            self._store(
                instance=index,
                is_active=False,
            )
