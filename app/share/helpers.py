from django.contrib.auth.models import User as AuthUser

from .models import *



class FollowShareHelper(object):
    """
    An helper on follow share operations
    """

    @staticmethod
    def follow_users(user):
        """
        Returns the list of users that follow given user
        """
        for cur_follow in Follow.objects.filter(user_id=user.id, is_active=True):
            yield cur_follow.follower
