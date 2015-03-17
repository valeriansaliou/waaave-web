from datetime import timedelta
from types import MethodType

from django.contrib.auth.models import User as AuthUser

from _commons.helpers.cache import CacheHelper
from _commons.helpers.types import TypesHelper
from _commons.helpers.statuses import StatusesHelper

from _index.models import Ids as _IndexIds

from share.models import Follow as ShareFollow
from share.models import Waaave as ShareWaaave

from tutorial.models import Meta as TutorialMeta
from tutorial.models import Author as TutorialAuthor

from comment.models import Active as CommentActive
from spot.models import Membership as SpotMembership

from tutorial.helpers.process import ProcessHelper as TutorialProcessHelper
from tutorial.helpers.read import ReadHelper as TutorialReadHelper
from user.helpers import StatsUserHelper


class BaseTimelineFactory(object):
    """
    Base superclass for any timeline-oriented data builder (factory)
    """

    def __init__(self):
        self._timeline = []


    def _fetch_item_groups(self, model, verbose, group_key, modificator=None):
        """
        Fetch the given grouped timeline item
        """
        grouped = {}
        instance, items = self._fetch_item(model, verbose)

        if isinstance(modificator, MethodType):
            for item in items:
                cur_instance = instance.filter(id=item['id']).first()
                modificator(cur_instance, item)

        for item in items:
            key = item[group_key]
            if not key in grouped: grouped[key] = []
            grouped[key].append(item)

        for _, item in grouped.items():
            yield item


    def _order(self, items):
        """
        Order timeline data by date
        """
        if len(items):
            items = sorted(items, key=lambda k: k['date'])
            items.reverse()

        return items


    def _preprocess_unbuffer(self, buffer_type, buffer_items, buffer_date):
        """
        Preprocess the items buffered data
        """
        return {
            'type': buffer_type,
            #'id': md5(str(buffer_date)).hexdigest(),
            'id': buffer_items[0]['id'],
            'date': buffer_date,
            'items': buffer_items,
        }


    def _preprocess(self, items, verbose, date_threshold):
        """
        Preprocess the items data
        """
        preprocessed = []

        cur_date = None
        cur_buffer = []

        items = self._order(items)

        for item in items:
            # Initiate a new group?
            if not cur_date or (cur_date - item['date']) >= date_threshold:
                if len(cur_buffer):
                    preprocessed.append(
                        self._preprocess_unbuffer(verbose, cur_buffer, cur_date)
                    )

                cur_date = item['date']
                cur_buffer = []

            cur_buffer.append(item)

        # Process remaining items in buffer?
        if len(cur_buffer):
            preprocessed.append(
                self._preprocess_unbuffer(verbose, cur_buffer, cur_date)
            )

        return preprocessed


    def _prepare(self):
        """
        Prepare timeline data
        """
        self._timeline += self._fetch()
        self._timeline = self._order(self._timeline)


    def __has_more(self, end_index):
        """
        Checks if more items exist after end index
        """
        try:
            self._timeline[end_index]
            return True
        except IndexError:
            return False


    def get(self, page=0, items_per_page=10):
        """
        Return usable timeline data
        """
        assert type(page) is int and type(items_per_page) is int

        if page is 0:
            return self._generate(), False

        timeline_count = len(self._timeline)
        page_total = timeline_count // items_per_page\
                     + (1 if timeline_count % items_per_page else 0)

        if page > page_total:
            return [], False

        start = (page - 1) * items_per_page
        end = start + items_per_page

        return self._generate(start, end), self.__has_more(end)



class TimelineFactory(BaseTimelineFactory):
    """
    Builds timeline data
    """
    
    def __init__(self, me_user):
        super(TimelineFactory, self).__init__()

        self._me_user = me_user


    def _fetch_item(self, filtered, verbose):
        """
        Fetch the given timeline item
        """
        items = filtered.values()

        for item in items:
            item.update({
                'type': verbose,
            })

        return filtered, items


    def __fetch_tutorials(self, user_ids=[], item_ids=[]):
        """
        Fetch the tutorials activity of a user
        """
        if user_ids:
            item_ids = [t.tutorial.id for t in TutorialAuthor.objects.filter(user_id__in=user_ids)]

        filtered = TutorialMeta.objects.filter(id__in=item_ids)

        _, fetched = self._fetch_item(
            filtered=filtered,
            verbose='tutorial',
        )

        # Replace 'date' with 'publish_date' (for ordering purposes)
        for cur_item in fetched:
            if cur_item['publish_date']:
                cur_item['date'] = cur_item['publish_date']
            
            del cur_item['publish_date']

        return fetched


    def __fetch_books(self, item_ids=[]):
        """
        Fetch the books activity
        """
        # Prevents circular imports
        from book.models import Item as BookItem

        _, fetched = self._fetch_item(
            filtered=BookItem.objects.filter(id__in=item_ids),
            verbose='book',
        )

        return fetched


    def __fetch_waaaves(self, user_ids=[], item_ids=[]):
        """
        Fetch the waaaves activity of a user
        """
        preprocessed = []

        filtered = ShareWaaave.objects.filter(user_id__in=user_ids) if user_ids\
                   else ShareWaaave.objects.filter(id__in=item_ids)
        filtered = filtered.filter(is_active=True)

        fetched_groups = self._fetch_item_groups(
            model=filtered,
            verbose='waaave',
            group_key='item_id',
        )

        for fetched in fetched_groups:
            preprocessed += self._preprocess(
                items=fetched,
                verbose='waaave',
                date_threshold=timedelta(weeks=4)
            )

        return preprocessed


    def __fetch_follows(self, user_ids=[], item_ids=[]):
        """
        Fetch the follows activity of a user
        """
        preprocessed = []

        filtered = ShareFollow.objects.filter(follower_id__in=user_ids) if user_ids\
                   else ShareFollow.objects.filter(id__in=item_ids)
        filtered = filtered.filter(is_active=True)

        if not self._me_user.id in user_ids:
            filtered = filtered.exclude(user_id=self._me_user.id)
        
        fetched_groups = self._fetch_item_groups(
            model=filtered,
            verbose='follow',
            group_key='follower_id',
        )

        for fetched in fetched_groups:
            preprocessed += self._preprocess(
                items=fetched,
                verbose='follow',
                date_threshold=timedelta(weeks=2)
            )

        return preprocessed


    def __fetch_spots(self, user_ids=[], item_ids=[]):
        """
        Fetch the spots activity of a user
        """
        preprocessed = []

        filtered = SpotMembership.objects.filter(user_id__in=user_ids) if user_ids\
                   else SpotMembership.objects.filter(id__in=item_ids)
        filtered = filtered.filter(is_active=True)

        if not self._me_user.id in user_ids:
            filtered = filtered.exclude(user_id=self._me_user.id)
        
        fetched_groups = self._fetch_item_groups(
            model=filtered,
            verbose='spot',
            group_key='user_id',
        )

        for fetched in fetched_groups:
            preprocessed += self._preprocess(
                items=fetched,
                verbose='spot',
                date_threshold=timedelta(weeks=1)
            )

        return preprocessed


    def __fetch_comments(self, user_ids=[], item_ids=[]):
        """
        Fetch the comments activity of a user
        """
        preprocessed = []

        filtered = CommentActive.objects.filter(author_id__in=user_ids) if user_ids\
                   else CommentActive.objects.filter(id__in=item_ids)
        filtered = filtered.filter(is_hidden=False)

        fetched_groups = self._fetch_item_groups(
            model=filtered,
            verbose='comment',
            group_key='content_item_hash',
            modificator=self.__modificator_comments,
        )

        for fetched in fetched_groups:
            preprocessed += self._preprocess(
                items=fetched,
                verbose='comment',
                date_threshold=timedelta(days=1)
            )

        return preprocessed


    def __modificator_comments(self, instance, item):
        """
        Maps content item type & item id as dict key
        """
        item['content_item_hash'] = '%s_%s' % (instance.item.item_type, instance.item.item_id)


    def __generate_item_data(self, item):
        """
        Generate the item data (can be a tutorial, a book or so)
        """
        item_data = {}
        item_type = TypesHelper.reverse(item.item_type)

        if item_type == 'tutorial':
            item_data = self.__generate_tutorial(item.item_id)
        elif item_type == 'book':
            item_data = self.__generate_book(item.item_id)

        return item_type, item_data


    def __generate_tutorial(self, tutorial_id):
        """
        Generate the tutorials data
        """
        tutorial_data = {}

        try:
            cur_tutorial_meta = TutorialMeta.objects.get(id=tutorial_id, is_online=True, status=StatusesHelper.encode('accepted'))
            cur_tutorial_author = cur_tutorial_meta.author_set.filter(is_master=True).first()
            
            tutorial_data = {
                'type': 'tutorial',
                'date': cur_tutorial_author.date,
                'data': TutorialProcessHelper.generate_data(
                    tutorial=cur_tutorial_meta,
                    author=cur_tutorial_author,
                ),
            }

            tutorial_data['data']['url_full'] = TutorialProcessHelper.url_full(tutorial_id)
        except TutorialMeta.DoesNotExist:
            pass
        finally:
            return tutorial_data


    def __generate_book(self, book_id):
        """
        Generate the book data
        """
        # Prevents circular imports
        from book.helpers import BookHelper

        book_data = {}
        cur_book = BookHelper.resolve(book_id)

        if cur_book:
            book_data = {
                'type': 'book',
                'date': cur_book.date,
                'data': BookHelper.generate_data(
                    book=cur_book,
                ),
            }

            book_data['data']['url_full'] = BookHelper.url_full(cur_book)
            book_data['data']['title'] = book_data['data']['item'].title

        return book_data


    def __generate_tutorials(self, cur_tutorial):
        """
        Generate the tutorials data
        """
        assert cur_tutorial['type'] == 'tutorial'

        gen_tutorial = self.__generate_tutorial(cur_tutorial['id'])

        return gen_tutorial


    def __generate_books(self, cur_book):
        """
        Generate the books data
        """
        assert cur_book['type'] == 'book'

        gen_book = self.__generate_book(cur_book['id'])

        return gen_book


    def __generate_waaaves(self, cur_waaave):
        """
        Generate the waaaves data
        """
        assert cur_waaave['type'] == 'waaave'

        data = []

        item_type, item_data = None, {}

        for sub_waaave in cur_waaave['items']:
            try:
                sub_waaave_instance = ShareWaaave.objects.get(id=sub_waaave['id'])
            except ShareWaaave.DoesNotExist:
                continue

            if not (item_type and item_data):
                item_type, item_data = self.__generate_item_data(sub_waaave_instance.item)

            data.append({
                'id': sub_waaave['id'],
                'date': sub_waaave['date'],

                'data': {
                    'user': sub_waaave_instance.user,
                },
            })

        if not (item_type and item_data): return

        return {
            'type': 'waaave',
            'id': cur_waaave['id'],
            'date': cur_waaave['date'],
            'data': data,

            'meta': {
                'item_type': item_type,
                'item_data': item_data,
            }
        }


    def __generate_follows(self, cur_follow):
        """
        Generate the follows data
        """
        assert cur_follow['type'] == 'follow'

        data = []

        following_user = None

        follow_ids = [i['id'] for i in cur_follow['items']]
        follow_instances = ShareFollow.objects.filter(id__in=follow_ids)

        for sub_follow in follow_instances:
            if not following_user:
                following_user = sub_follow.follower
            if following_user.id == sub_follow.user.id:
                continue

            data.append({
                'id': sub_follow.id,
                'date': sub_follow.date,

                'data': {
                    'followed_user': sub_follow.user,
                    'followed_stats': StatsUserHelper(sub_follow.user).get(),
                },
            })

        return {
            'type': 'follow',
            'id': cur_follow['id'],
            'date': cur_follow['date'],
            'data': data,

            'meta': {
                'following_user': following_user,
            }
        }


    def __generate_spots(self, cur_spot):
        """
        Generate the spots data
        """
        # Prevents circular imports
        from spot.helpers import SpotHelper

        assert cur_spot['type'] == 'spot'

        data = []

        user = None

        spot_ids = [i['id'] for i in cur_spot['items']]
        spot_instances = SpotMembership.objects.filter(id__in=spot_ids)

        for sub_spot in spot_instances:
            if not user:
                user = sub_spot.user

            data.append({
                'id': sub_spot.id,
                'date': sub_spot.date,
                'data': SpotHelper.generate_data(sub_spot.spot),
            })

        return {
            'type': 'spot',
            'id': cur_spot['id'],
            'date': cur_spot['date'],
            'data': data,

            'meta': {
                'user': user,
            }
        }


    def __generate_comments(self, cur_comment):
        """
        Generate the comments data
        """
        assert cur_comment['type'] == 'comment'

        data = []

        item_type, item_data = None, {}

        for sub_comment in cur_comment['items']:
            try:
                sub_comment_instance = CommentActive.objects.get(id=sub_comment['id'])
            except CommentActive.DoesNotExist:
                continue

            if not (item_type and item_data):
                item_type, item_data = self.__generate_item_data(sub_comment_instance.item)

            data.append({
                'id': sub_comment['id'],
                'date': sub_comment['date'],

                'data': sub_comment_instance,
            })

        if not (item_type and item_data): return

        return {
            'type': 'comment',
            'id': cur_comment['id'],
            'date': cur_comment['date'],
            'data': data,

            'meta': {
                'item_type': item_type,
                'item_data': item_data,
            }
        }


    def _fetch(self, user_ids=[], item_all_ids={}, fetch_types=()):
        """
        Fetch the whole activity of a user
        """

        fetch_data = []

        if not fetch_types or 'tutorials' in fetch_types:
            fetch_data += self.__fetch_tutorials(
                user_ids=user_ids,
                item_ids=item_all_ids.get('tutorials', []),
            )

        if not fetch_types or 'books' in fetch_types:
            fetch_data += self.__fetch_books(
                item_ids=item_all_ids.get('books', []),
            )

        if not fetch_types or 'waaaves' in fetch_types:
            fetch_data += self.__fetch_waaaves(
                user_ids=user_ids,
                item_ids=item_all_ids.get('waaaves', []),
            )

        if not fetch_types or 'follows' in fetch_types:
            fetch_data += self.__fetch_follows(
                user_ids=user_ids,
                item_ids=item_all_ids.get('follows', []),
            )

        if not fetch_types or 'spots' in fetch_types:
            fetch_data += self.__fetch_spots(
                user_ids=user_ids,
                item_ids=item_all_ids.get('spots', []),
            )

        if not fetch_types or 'comments' in fetch_types:
            fetch_data += self.__fetch_comments(
                user_ids=user_ids,
                item_ids=item_all_ids.get('comments', []),
            )

        return fetch_data


    def _generate(self, start=0, end=None):
        """
        Generate the whole timeline data
        """
        timeline = []

        for cur_timeline in self._timeline[start:end]:
            if cur_timeline['type'] == 'tutorial':
                timeline.append(
                    self.__generate_tutorials(cur_timeline)
                )
            elif cur_timeline['type'] == 'book':
                timeline.append(
                    self.__generate_books(cur_timeline)
                )
            elif cur_timeline['type'] == 'follow':
                timeline.append(
                    self.__generate_follows(cur_timeline)
                )
            elif cur_timeline['type'] == 'waaave':
                timeline.append(
                    self.__generate_waaaves(cur_timeline)
                )
            elif cur_timeline['type'] == 'spot':
                timeline.append(
                    self.__generate_spots(cur_timeline)
                )
            elif cur_timeline['type'] == 'comment':
                timeline.append(
                    self.__generate_comments(cur_timeline)
                )
            else:
                raise Exception("Unknown Model Generator")

        # Cleanup appended data
        timeline = [t for t in timeline if t]

        return timeline



class FollowTimelineFactory(TimelineFactory):
    """
    Builds follow timeline data
    """
    
    def __init__(self, me_user, fetch_filter='following'):
        assert fetch_filter in ('following', 'followers', 'everyone')

        super(FollowTimelineFactory, self).__init__(me_user)
        self.__fetch_filter = fetch_filter
        self._prepare()


    def __users_following(self):
        """
        Return the list of users I am following
        """
        return [c.user_id for c in ShareFollow.objects.filter(follower=self._me_user)]


    def __users_followers(self):
        """
        Return the list of users I am followed by
        """
        return [c.follower_id for c in ShareFollow.objects.filter(user=self._me_user)]


    def __users_everyone(self):
        """
        Return the list of all the users on the network
        """
        return [c.id for c in AuthUser.objects.all()]


    def _prepare(self):
        """
        Prepare follow timeline activity data
        """
        users_list = []

        if self.__fetch_filter == 'following':
            users_list = self.__users_following()
        elif self.__fetch_filter == 'followers':
            users_list = self.__users_followers()
        elif self.__fetch_filter == 'everyone':
            users_list = self.__users_everyone()

        # Regenerate users list ensuring myself is not in...
        users_list = [u for u in users_list if u != self._me_user.id]

        self._timeline += self._fetch(user_ids=users_list)
        self._timeline = self._order(self._timeline)


    def _fetch(self, user_ids=[]):
        """
        Fetch the whole activity of the follow timeline
        """
        namespace = CacheHelper.ns('timeline:factories:follow:_fetch', self._me_user,
            user_ids=user_ids, fetch_filter=self.__fetch_filter)
        fetch_data = CacheHelper.io.get(namespace)

        if fetch_data is None:
            fetch_types = ('tutorials', 'waaaves')

            #-- Deactivated due to #467
            #if self.__fetch_filter == 'following':
            #    fetch_types += ('follows',)

            fetch_data = super(FollowTimelineFactory, self)._fetch(
                user_ids=user_ids,
                fetch_types=fetch_types,
            )
            CacheHelper.io.set(namespace, fetch_data, 10)

        return fetch_data


    def _generate(self, start=0, end=None):
        """
        Generate the follow timeline data
        """
        namespace = CacheHelper.ns('timeline:factories:follow:_generate', self._me_user,
            start=start, end=end, fetch_filter=self.__fetch_filter)
        timeline = CacheHelper.io.get(namespace)

        if timeline is None:
            timeline = super(FollowTimelineFactory, self)._generate(start=start, end=end)
            CacheHelper.io.set(namespace, timeline, 10)

        return timeline



class UserTimelineFactory(TimelineFactory):
    """
    Builds user timeline data
    """
    
    def __init__(self, me_user, user_id=None):
        super(UserTimelineFactory, self).__init__(me_user)

        assert user_id is not None

        self.__user_id = user_id
        self._prepare()


    def _prepare(self):
        """
        Prepare user timeline activity data
        """
        self._timeline += self._fetch()
        self._timeline = self._order(self._timeline)


    def _fetch(self):
        """
        Fetch the whole activity of the user timeline
        """
        namespace = CacheHelper.ns('timeline:factories:user:_fetch', user_id=self.__user_id)
        fetch_data = CacheHelper.io.get(namespace)

        if fetch_data is None:
            fetch_data = super(UserTimelineFactory, self)._fetch(
                user_ids=[self.__user_id],
            )
            CacheHelper.io.set(namespace, fetch_data, 10)

        return fetch_data


    def _generate(self, start=0, end=None):
        """
        Generate the user timeline data
        """
        namespace = CacheHelper.ns('timeline:factories:user:_generate', user_id=self.__user_id, start=start, end=end)
        timeline = CacheHelper.io.get(namespace)

        if timeline is None:
            timeline = super(UserTimelineFactory, self)._generate(start=start, end=end)
            CacheHelper.io.set(namespace, timeline, 10)

        return timeline



class SpotTimelineFactory(TimelineFactory):
    """
    Builds spot timeline data
    """
    
    def __init__(self, me_user, spot):
        super(SpotTimelineFactory, self).__init__(me_user)

        assert spot is not None

        self.__spot = spot
        self._prepare()


    def __list_items_all_spot(self):
        """
        List the items that are in the current spot
        """
        # Prevents circular imports
        from book.helpers import BookHelper

        return {
            'books': [b.id for b in BookHelper.list_with_tag(self.__spot)],
            'tutorials': [t.id for t in TutorialReadHelper.list_with_tag(self.__spot)],
        }


    def _prepare(self):
        """
        Prepare spot timeline activity data
        """
        self._timeline += self._fetch()
        self._timeline = self._order(self._timeline)


    def _fetch(self):
        """
        Fetch the whole activity of the spot timeline
        """
        namespace = CacheHelper.ns('timeline:factories:spot:_fetch', spot_id=self.__spot.id)
        fetch_data = CacheHelper.io.get(namespace)

        if fetch_data is None:
            fetch_types = ('books', 'tutorials')

            fetch_data = super(SpotTimelineFactory, self)._fetch(
                item_all_ids=self.__list_items_all_spot(),
                fetch_types=fetch_types,
            )
            CacheHelper.io.set(namespace, fetch_data, 60)

        return fetch_data


    def _generate(self, start=0, end=None):
        """
        Generate the spot timeline data
        """
        namespace = CacheHelper.ns('timeline:factories:spot:_generate', spot_id=self.__spot.id, start=start, end=end)
        timeline = CacheHelper.io.get(namespace)

        if timeline is None:
            timeline = super(SpotTimelineFactory, self)._generate(start=start, end=end)
            CacheHelper.io.set(namespace, timeline, 60)

        return timeline
