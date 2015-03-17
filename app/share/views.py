import json

from django.http import HttpResponse
from django.contrib.humanize.templatetags import humanize
from django.contrib.auth.models import User as AuthUser

from _commons.helpers.types import TypesHelper
from _commons.helpers.redirects import login_required_url, register_required_url
from _commons.helpers.rank import RankHelper
from _index.helpers import ContentHelper
from _index.models import Ids as _IndexIds
from account.models import Profile as AuthProfile

from rank.helpers import RankProcessHelper
from notification.factories import PushWaaaveNotificationFactory, PushFollowNotificationFactory

from .models import *


def waaave(request, item_type, item_id):
    """
    Share > Waaave
    """
    # Validate item data
    item_exists, item_author_id = ContentHelper.validate(item_id, item_type)
    item_type = TypesHelper.encode(item_type)

    result = {
        'status': 'error',
        'message': '',
        'contents': {}
    }

    if item_exists is True:
        if request.method == 'POST':
            waaave_state = request.POST.get('waaave_state', 0)

            if waaave_state.isdigit():
                waaave_state = int(waaave_state)

            if waaave_state is 0 or waaave_state is 1:
                if request.user.is_authenticated():
                    user = request.user

                    db_index_ids = _IndexIds.objects.get_or_create(
                        item_id=item_id,
                        item_type=item_type,
                    )[0]
                    db_waaave = Waaave.objects.get_or_create(
                        user=user,
                        item=db_index_ids,
                    )[0]

                    notification_factory = PushWaaaveNotificationFactory(request=request, item_type=item_type, item_id=item_id)

                    if waaave_state is 0:
                        notification_factory.unset(db_waaave)
                        
                        if db_waaave.is_active is not False:
                            db_waaave.is_active = False
                            db_waaave.save()

                        # Cancel the record and downgrade experience
                        try:
                            RankProcessHelper.cancel(
                                AuthProfile.objects.get(user_id=item_author_id),
                                user.profile,
                                [item_id, 'tutorial'],
                                RankHelper.get_action_by_name('share_waaave'),
                            )
                        except AuthProfile.DoesNotExist:
                            pass
                    
                    elif waaave_state is 1:
                        notification_factory.set(db_waaave)

                        if db_waaave.is_active is not True:
                            db_waaave.is_active = True
                            db_waaave.save()

                        # Create the record and upgrade experience
                        try:
                            RankProcessHelper.create(
                                AuthProfile.objects.get(user_id=item_author_id),
                                user.profile,
                                [item_id, 'tutorial'],
                                RankHelper.get_action_by_name('share_waaave'),
                            )
                        except AuthProfile.DoesNotExist:
                            pass

                    db_waaave_all_count = Waaave.objects.filter(item=db_index_ids, is_active=True).count()

                    result['status'] = 'success'
                    result['contents']['status'] = waaave_state
                    result['contents']['count'] = humanize.intcomma(db_waaave_all_count)
                
                else:
                    result['message'] = 'Not authenticated'
                    result['contents']['redirect'] = {
                        'login': login_required_url(request.META.get('HTTP_REFERER', '/')),
                        'register': register_required_url(),
                    }
            else:
                result['message'] = 'Data missing'
        else:
            result['message'] = 'Bad request'
    else:
        result['message'] = 'Not found'
    
    return HttpResponse(json.dumps(result), content_type='application/json')


def follow(request, user_id):
    """
    Share > Follow
    """
    result = {
        'status': 'error',
        'message': '',
        'contents': {}
    }

    # Not me?
    if str(user_id) != str(request.user.id):
        # Validate user data
        try:
            followed_user = AuthUser.objects.get(id=user_id)
            follower_user = request.user

            if request.method == 'POST':
                follow_state = request.POST.get('follow_state', 0)

                if follow_state.isdigit():
                    follow_state = int(follow_state)

                if follow_state is 0 or follow_state is 1:
                    if request.user.is_authenticated():
                        db_follow = Follow.objects.get_or_create(
                            user=followed_user,
                            follower=follower_user,
                        )[0]

                        notification_factory = PushFollowNotificationFactory(request=request, target_user=followed_user)

                        if follow_state is 0:
                            notification_factory.unset(db_follow)

                            if db_follow.is_active is not False:
                                db_follow.is_active = False
                                db_follow.save()

                            # Cancel the record and downgrade experience
                            RankProcessHelper.cancel(
                                followed_user.profile,
                                follower_user.profile,
                                [user_id, 'user'],
                                RankHelper.get_action_by_name('follower'),
                            )

                        if follow_state is 1:
                            notification_factory.set(db_follow)

                            if db_follow.is_active is not True:
                                db_follow.is_active = True
                                db_follow.save()

                            # Create the record and upgrade experience
                            RankProcessHelper.create(
                                followed_user.profile,
                                follower_user.profile,
                                [user_id, 'user'],
                                RankHelper.get_action_by_name('follower'),
                            )

                        # Get the new, freshly updated, results
                        db_follow_all_count = Follow.objects.filter(user=followed_user, is_active=True).count()

                        result['status'] = 'success'
                        result['contents']['status'] = follow_state
                        result['contents']['count'] = humanize.intcomma(db_follow_all_count)
                    else:
                        result['message'] = 'Not authenticated'
                        result['contents']['redirect'] = {
                            'login': login_required_url(request.META.get('HTTP_REFERER', '/')),
                            'register': register_required_url(),
                        }
                else:
                    result['message'] = 'Data missing'
            else:
                result['message'] = 'Bad request'
        except AuthUser.DoesNotExist:
            result['message'] = 'Not found'
    else:
        result['message'] = 'Self user'
    
    return HttpResponse(json.dumps(result), content_type='application/json')
