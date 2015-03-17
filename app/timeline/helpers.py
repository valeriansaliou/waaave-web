from share.models import Follow as ShareFollow

from .factories import *



class FollowTimelineHelper(object):
    """
    An helper on follow timeline operations
    """

    @staticmethod
    def __has_following(request):
        """
        Returns whether the current user follows anyone or not
        """
        return True if ShareFollow.objects.filter(follower=request.user).count() else False


    @staticmethod
    def __has_followers(request):
        """
        Returns whether the current user is followed by anyone or not
        """
        return True if ShareFollow.objects.filter(user=request.user).count() else False


    @classmethod
    def build_response(_class, request, fetch_filter='following', page=1):
        """
        Builds the follow timeline response
        """
        # Generate the timeline itself
        items_per_page = 10

        timeline_feed, has_show_more = FollowTimelineFactory(request.user, fetch_filter).get(
            page=page,
            items_per_page=items_per_page,
        )

        response_data = {
            'timeline': timeline_feed,
            'has_show_more': has_show_more,
            'fetch_filter': fetch_filter,
            'next_page': page + 1,
        }

        response_data.update({
            'has_following': _class.__has_following(request),
            'has_followers': _class.__has_followers(request),
        })

        return response_data



class UserTimelineHelper(object):
    """
    An helper on user timeline operations
    """

    @staticmethod
    def build_response(request, user, page=1):
        """
        Builds the user timeline response
        """
        items_per_page = 10

        timeline_feed, has_show_more = UserTimelineFactory(request.user, user.id).get(
            page=page,
            items_per_page=items_per_page,
        )

        return {
            'aut_user': user,
            'timeline': timeline_feed,
            'has_show_more': has_show_more,
            'next_page': page + 1,
        }



class SpotTimelineHelper(object):
    """
    An helper on spot timeline operations
    """

    @staticmethod
    def build_response(request, spot, page=1, items_per_page=10):
        """
        Builds the spot timeline response
        """
        timeline_feed, has_show_more = SpotTimelineFactory(request.user, spot).get(
            page=page,
            items_per_page=items_per_page,
        )

        return {
            'timeline': timeline_feed,
            'has_show_more': has_show_more,
            'next_page': page + 1,
        }
