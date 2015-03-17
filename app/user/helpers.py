from hitcount.utils import count_hits as hitcount_count_hits
from django.contrib.auth.models import User as AuthUser

from share.models import Follow as ShareFollow
from share.models import Waaave as ShareWaaave

from tutorial.models import Author as TutorialAuthor
from tutorial.models import Meta as TutorialMeta

from _commons.helpers.statuses import StatusesHelper
from tutorial.helpers.read import ReadHelper


class MainUserHelper(object):
    """
    An helper on user main operations
    """

    @classmethod
    def __init__build_following_followers_interests_response(_class, request, username, page):
        """
        Initializes the build of following/followers response
        """
        page = page if page > 0 else 1
        items_per_page = 10

        response_data, user = _class.build_response(request, username)

        start = items_per_page * (page - 1)
        end = start + items_per_page

        return response_data, user, start, end


    @staticmethod
    def build_response(request, username):
        """
        Builds the user main response
        """
        # Response data object
        response_data = {
            'status': 'none',
        }

        try:
            user = AuthUser.objects.get(username=username)
        except AuthUser.DoesNotExist:
            response_data['status'] = 'not_found'
            return response_data, None

        response_data.update({
            'status': 'success',
            'aut_user': user,
            'aut_profile': user.profile,
            'aut_stats': AdvancedStatsUserHelper(user).get(),
        })

        return response_data, user


    @classmethod
    def build_following_response(_class, request, username, page=1):
        """
        Builds the user main (following) response
        """
        response_data, user, start, end = _class.__init__build_following_followers_interests_response(request, username, page)

        if response_data['status'] != 'not_found':
            filtered = ShareFollow.objects.filter(follower=user, is_active=True).exclude(user=user).order_by('-date')
            user_following = []

            for follow in filtered[start:end]:
                user_following.append({
                    'user': follow.user,
                    'tutorial': (ReadHelper.random_for_author(follow.user) + [None])[0],
                })

            response_data.update({
                'user_following': user_following,
                'has_show_more': filtered.count() > end,
                'next_page': page + 1,
            })

        return response_data, user


    @classmethod
    def build_followers_response(_class, request, username, page=1):
        """
        Builds the user main (followers) response
        """
        response_data, user, start, end = _class.__init__build_following_followers_interests_response(request, username, page)

        if response_data['status'] != 'not_found':
            filtered = ShareFollow.objects.filter(user=user, is_active=True).exclude(follower=user).order_by('-date')
            user_followers = []

            for follow in filtered[start:end]:
                user_followers.append({
                    'user': follow.follower,
                    'tutorial': (ReadHelper.random_for_author(follow.follower) + [None])[0],
                })

            response_data.update({
                'user_followers': user_followers,
                'has_show_more': filtered.count() > end,
                'next_page': page + 1,
            })

        return response_data, user


    @classmethod
    def build_interests_response(_class, request, username, page=1):
        """
        Builds the user main (interests) response
        """
        # Prevents circular imports
        from spot.helpers import SpotHelper

        response_data, user, start, end = _class.__init__build_following_followers_interests_response(request, username, page)

        if response_data['status'] != 'not_found':
            filtered = SpotHelper.list_spots_for_user(user)
            user_interests = []

            for spot in filtered[start:end]:
                user_interests.append(
                    SpotHelper.generate_data(spot)
                )

            response_data.update({
                'user_interests': user_interests,
                'has_show_more': filtered.count() > end,
                'next_page': page + 1,
            })

        return response_data, user



class StatsUserHelper(object):
    """
    An helper on user statistics operations
    """

    def __init__(self, user):
        """
        Initializes the user statistics
        """
        self._user = user
        self._stats = {}
        self.__prepare()


    def __prepare(self):
        """
        Prepares the user statistics
        """
        self._stats.update({
            'followers': self.__count_followers(),
            'tutorials': self.__count_tutorials(),
            'shots': self.__count_shots(),
        })


    def __count_followers(self):
        """
        Counts the number of followers for current user
        """
        return ShareFollow.objects.filter(user=self._user).count()


    def __count_tutorials(self):
        """
        Counts the number of tutorials for current user
        """
        return TutorialAuthor.objects.filter(user=self._user).filter(tutorial__is_online=True).filter(tutorial__status=2).count()


    def __count_shots(self):
        """
        Counts the number of shots for current user
        """
        #return ShotAuthor.objects.filter(author_id=self._user_id).count()
        return 0


    def get(self):
        """
        Gets the user statistics
        """
        return self._stats



class AdvancedStatsUserHelper(StatsUserHelper):
    """
    An helper on user advanced statistics operations
    """

    def __init__(self, user):
        """
        Initializes the user advanced statistics
        """
        super(AdvancedStatsUserHelper, self).__init__(user)
        self.__prepare_advanced()


    def __prepare_advanced(self):
        """
        Prepares the user advanced statistics
        """
        self._stats.update({
            'views': self.__count_views(),
            'shares': self.__count_shares(),
            'followings': self.__count_followings(),
        })


    def __count_views(self):
        """
        Counts the total number of tutorials' views for current user
        """
        views = 0
        tutorials = TutorialMeta.objects.filter(author__user=self._user, is_online=True, status=StatusesHelper.encode('accepted'))
        for tutorial in tutorials:
            views += hitcount_count_hits(tutorial)
        return views


    def __count_shares(self):
        """
        Counts the number of shares for current user
        """
        return ShareWaaave.objects.filter(user=self._user).count()


    def __count_followings(self):
        """
        Counts the number of followings for current user
        """
        return ShareFollow.objects.filter(follower=self._user).count()
