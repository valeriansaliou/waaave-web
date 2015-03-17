from datetime import datetime

from hitcount.utils import count_hits as hitcount_count_hits
from django.contrib.auth.models import User as AuthUser

from tag.models import List as TagList

from _commons.helpers.fields import FieldsHelper
from _commons.helpers.cache import CacheHelper
from _index.helpers import ContentHelper as _IndexContentHelper

from notification.factories import PushSpotNotificationFactory
from timeline.helpers import SpotTimelineHelper
from tutorial.helpers.read import ReadHelper as TutorialReadHelper
from tutorial.helpers.process import ProcessHelper as TutorialProcessHelper
from tag.helpers import TagHelper

from .models import *
from .exceptions import *


class SpotHelper(object):
    """
    An helper on spot operations
    """

    @staticmethod
    def _generate_namespace(fn_name, tag, items_per_page, page):
        """
        Generate call namespace
        """
        return CacheHelper.ns(
            ('spot:views:%s' % fn_name),

            tag=tag,
            items_per_page=items_per_page,
            page=page,
        )


    @staticmethod
    def _generate_view(fn_name):
        """
        Generate call view
        """
        return 'spot.views.%s' % fn_name


    @staticmethod
    def _read_timeline(spot):
        """
        Read spot timeline
        """
        return SpotTimelineFactory


    @staticmethod
    def _list_tutorials(spot):
        """
        List spot tutorials
        """
        return TutorialReadHelper.list_with_tag(spot)


    @staticmethod
    def _list_books(spot):
        """
        List spot books
        """
        # Prevents circular imports
        from book.helpers import BookHelper

        return BookHelper.list_with_tag(spot)


    @classmethod
    def _list_waaavers(_class, spot):
        """
        List spot waaavers
        """
        user_ids = [m.user_id for m in _class.list_memberships_in_spot(spot)]

        return AuthUser.objects.filter(id__in=user_ids)


    @classmethod
    def _read_tutorials(_class, spot):
        """
        Read spot tutorials
        """
        return [TutorialProcessHelper.generate_data(t) for t in _class._list_tutorials(spot)]


    @classmethod
    def _read_books(_class, spot):
        """
        Read spot books
        """
        # Prevents circular imports
        from book.helpers import BookHelper
        
        return [BookHelper.generate_data(b) for b in _class._list_books(spot)]


    @classmethod
    def _read_waaavers(_class, spot):
        """
        Read spot waaavers
        """
        waaavers = []

        for waaaver in _class._list_waaavers(spot):
            waaavers.append({
                'user': waaaver,
                'tutorial': (TutorialReadHelper.random_for_author(waaaver) + [None])[0],
            })

        return waaavers


    @classmethod
    def _read_items(_class, fn_name, spot):
        """
        Read items contained in this spot
        """
        if fn_name == 'view_tutorials':
            return _class._read_tutorials(spot)
        elif fn_name == 'view_books':
            return _class._read_books(spot)
        elif fn_name == 'view_waaavers':
            return _class._read_waaavers(spot)
        else:
            raise SpotNotFound("Spot Handler Not Found")


    @staticmethod
    def resolve(tag):
        """
        Resolve a spot by ID
        """
        try:
            return TagList.objects.get(slug=tag)
        except TagList.DoesNotExist:
            return None


    @staticmethod
    def resolve_list(tags):
        """
        Resolve spots by ID
        """
        return TagList.objects.filter(slug__in=tags)


    @staticmethod
    def list():
        """
        List available spots
        """
        return TagList.objects.all()


    @staticmethod
    def list_memberships_in_spot(spot):
        """
        Return the memberships in provided spot
        """
        return spot.membership_set.filter(is_active=True)


    @staticmethod
    def list_spots_for_user(user):
        """
        Return the spots provided user is in
        """
        tag_ids = [m.spot_id for m in user.membership_set.filter(is_active=True)]

        return TagList.objects.filter(id__in=tag_ids)


    @classmethod
    def views(_class, spot):
        """
        Return a spot number of views
        """
        return hitcount_count_hits(spot)


    @classmethod
    def count_items(_class, spot):
        """
        Count items contained in this spot
        """
        return {
            'tutorials': len(_class._list_tutorials(spot)),
            'books': len(_class._list_books(spot)),
            'waaavers': _class.list_memberships_in_spot(spot).count(),
        }


    @staticmethod
    def join(user, spot, join=True):
        """
        Join provided spot
        """
        membership = Membership.objects.get_or_create(
            spot=spot,
            user=user,
        )[0]

        membership.is_active = True if join else False
        membership.save()

        return membership


    @classmethod
    def autojoin(_class, user, name):
        """
        Autojoin a list of spots if they exists
        """
        slug_list = [slug[0] for slug in TagHelper.string_to_list(name)]
        tag_list = _class.resolve_list(slug_list)

        for tag in tag_list:
            _class.join(user, tag)


    @classmethod
    def notify_followers(_class, spots, item_type, item_id, ignore_user_ids=[], date_threshold=None):
        """
        Notifies spot followers for new content
        """
        index = _IndexContentHelper.get(
            item_id=item_id,
            item_type=item_type,
        )

        for spot in spots:
            # Exclude ignored users from spot members list (if any)
            members = [m for m in _class.list_memberships_in_spot(spot) if not m.user.id in ignore_user_ids]

            for member in members:
                # Do not notify old members (if any date threshold set)
                if date_threshold is None or member.date < date_threshold:
                    PushSpotNotificationFactory(
                        target_user=member.user,
                        spot=spot,
                    ).set(index)


    @classmethod
    def generate_data(_class, spot):
        """
        Generates spot data
        """
        return {
            'item': spot,
            'views': _class.views(spot),
            'count_items': _class.count_items(spot),
        }


    @classmethod
    def build_response(_class, request, fn_name, tag, items_per_page=10, page=1):
        """
        Builds the spot response data
        """
        namespace = _class._generate_namespace(fn_name, tag, items_per_page, page)
        response = CacheHelper.io.get(namespace)

        if response is None:
            spot = SpotHelper.resolve(tag)

            try:
                page = page or 1
                page = int(page) or 1

                if not spot:
                    raise SpotNotFound("No Spot Data Resolved")

                if fn_name in ('view_root', 'view_root_fetch'):
                    response_data = SpotTimelineHelper.build_response(
                        request=request,
                        spot=spot,
                        page=page,
                        items_per_page=items_per_page,
                    )
                else:
                    start = (page - 1) * items_per_page
                    end = start + items_per_page

                    items = []
                    items_all = _class._read_items(fn_name, spot)

                    items_count = len(items_all) if items_all else 0
                    page_total = items_count // items_per_page\
                               + (1 if items_count % items_per_page else 0)\
                               or 1

                    # Page overflow?
                    if page > page_total:
                        raise SpotDataOverflow("Exceeded Page Threshold")

                    if items_all:
                        items = items_all[start:end]

                    response_data = {
                        'items': items,

                        'spot_view': _class._generate_view(fn_name),
                        'spot_page': page,
                        'spot_page_total': page_total,
                    }

                response_data.update({
                    'spot': _class.generate_data(spot),
                    'count_items': _class.count_items(spot),
                })

                response = True, response_data
            except (SpotNotFound, SpotDataOverflow):
                response = False, {}

            CacheHelper.io.set(namespace, response, 300)

        return response


    @classmethod
    def suggestions(_class, user, maximum=1):
        """
        Suggests a set of spots
        """
        namespace = CacheHelper.ns('spot:helpers:suggestions', user, maximum=maximum)
        results = CacheHelper.io.get(namespace)

        if results is None:
            results = []

            for spot in FieldsHelper.random(_class.list(), maximum):
                results.append(
                    _class.generate_data(spot)
                )

            CacheHelper.io.set(namespace, results, 60)

        return results
