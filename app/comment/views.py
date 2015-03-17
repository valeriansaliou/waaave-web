from datetime import datetime
import json

from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User as AuthUser

from _commons.helpers.cache import CacheHelper
from _commons.helpers.redirects import login_required_url, register_required_url
from _commons.helpers.types import TypesHelper
from _index.helpers import ContentHelper as _IndexContentHelper
from _index.models import Ids as _IndexIds

from tutorial.helpers.process import ProcessHelper as TutorialProcessHelper
from relevance.helpers import RelevanceHelper
from rank.helpers import RankProcessHelper
from notification.factories import PushCommentNotificationFactory

from .helpers import ReadHelper
from .models import *


def read(request, item_type, item_id):
    """
    Comment > Read
    """
    # Validate item data
    item_exists, item_author_id = _IndexContentHelper.validate(item_id, item_type)
    
    if item_exists is False:
        raise Http404

    # Read from cache
    namespace = CacheHelper.ns('comment:views:read', request.user, item_type=item_type, item_id=item_id)
    results = CacheHelper.io.get(namespace)

    if results is None:
        results = ReadHelper.read(
            user=request.user,
            item=_IndexContentHelper.get(item_id, item_type),
            item_author_id=item_author_id,
        )

        CacheHelper.io.set(namespace, results, 300)

    # Pass data to template
    comment_args = {
        # Commons
        'item_id': item_id,
        'item_type': item_type,

        # Comments
        'comments': results,
    }

    return render(request, 'comment/comment_read.jade', comment_args)


def add(request, item_type, item_id):
    """
    Comment > Add
    """
    # Validate item data
    item_exists, item_author_id = _IndexContentHelper.validate(item_id, item_type)

    result = {
        'status': 'error',
        'message': '',
        'contents': {}
    }

    if item_exists is True:
        namespace = CacheHelper.ns('comment:views:read', request.user, item_type=item_type, item_id=item_id)

        if request.method == 'POST':
            comment_body = request.POST.get('comment_body', '') or ''
            comment_in_reply_to = request.POST.get('comment_in_reply_to', None) or None

            db_comment_in_reply_to = None
            if comment_in_reply_to:
                try:
                    db_comment_in_reply_to = Active.objects.get(id=comment_in_reply_to)
                except Active.DoesNotExist:
                    pass

            if comment_body and item_type and item_id:
                try:
                    db_item = _IndexIds.objects.get(
                        item_id=item_id,
                        item_type=TypesHelper.encode(item_type),
                    )

                    if request.user.is_authenticated():
                        # Store comment
                        comment = Active.objects.create(
                            author=request.user,
                            item=db_item,
                            body=comment_body,
                            in_reply_to=db_comment_in_reply_to,
                        )

                        _IndexIds.objects.get_or_create(
                            item_type=TypesHelper.encode('comment'),
                            item_id=comment.id,
                        )

                        # Remove comment cache
                        CacheHelper.io.delete(namespace)

                        # Notify target users (in case it's a tutorial)
                        if item_type == 'tutorial':
                            target_users = []

                            if db_comment_in_reply_to:
                                try:
                                    target_users.append(
                                        AuthUser.objects.get(id=db_comment_in_reply_to.author_id)
                                    )
                                except AuthUser.DoesNotExist:
                                    pass
                            else:
                                for cur_author in TutorialProcessHelper.authors_all(item_id):
                                    target_users.append(cur_author.user)

                            for cur_user in target_users:
                                PushCommentNotificationFactory(
                                    request=request,
                                    target_user=cur_user,
                                    item_type=item_type,
                                    item_id=item_id,
                                ).set(comment)

                    else:
                        # Store comment (in pool)
                        comment = Pool.objects.create(
                            item=db_item,
                            body=comment_body,
                            in_reply_to=db_comment_in_reply_to,
                        )

                        # Next operations
                        result['contents']['please_login'] = True
                        result['contents']['next'] = {
                            'email': reverse('account.views.register_go'),
                            'facebook': reverse('social:begin', args=['facebook']),
                            'twitter': reverse('social:begin', args=['twitter']),
                        }

                        try:
                            if request.session.get('comment_pool', None) is None:
                                request.session['comment_pool'] = {}

                            request.session['comment_pool'][comment.id] = _IndexContentHelper.read(db_item)['content']['url']
                            request.session.modified = True
                        except KeyError:
                            pass

                    result['contents']['id'] = comment.id
                    result['status'] = 'success'
                except _IndexIds.DoesNotExist:
                    result['message'] = 'Item not found'
            else:
                result['message'] = 'Not enough data'
        else:
            result['message'] = 'Bad request'
    else:
        result['message'] = 'Not found'
    
    return HttpResponse(json.dumps(result), content_type='application/json')


def action(request, item_type, item_id):
    """
    Comment > Action
    """
    # Validate item data
    item_exists, item_author_id = _IndexContentHelper.validate(item_id, item_type)

    result = {
        'status': 'error',
        'message': '',
        'contents': {}
    }

    if item_exists is True:
        namespace = CacheHelper.ns('comment:views:read', request.user, item_type=item_type, item_id=item_id)

        if request.method == 'POST':
            comment_id = request.POST.get('comment_id', None)
            comment_action = request.POST.get('comment_action', None)

            if comment_id and comment_action in (
                'relevant',
                'irrelevant',
                'flag',
                'delete',
                'edit',
                'hide',
                'unhide'
            ):
                if request.user.is_authenticated():
                    user = request.user
                    uid = user.id
                    is_moderator = request.user.is_staff or request.user.is_superuser

                    try:
                        db_item = _IndexIds.objects.get(
                            item_id=item_id,
                            item_type=TypesHelper.encode(item_type),
                        )
                        db_comments = Active.objects.get(item=db_item, id=comment_id)

                        if comment_action in ('edit', 'delete'):
                            if uid == db_comments.author_id or is_moderator:
                                is_success = False

                                if comment_action == 'edit':
                                    comment_body = request.POST.get('comment_body', '')

                                    if comment_body:
                                        db_comments.body = comment_body
                                        db_comments.save()
                                        
                                        is_success = True
                                    else:
                                        result['message'] = 'Empty comment body'

                                elif comment_action == 'delete':
                                    if item_type in ('tutorial'):
                                        PushCommentNotificationFactory(request=request, item_type=item_type, item_id=item_id).unset(db_comments)
                                    
                                    db_comments.delete()
                                    is_success = True

                                if is_success:
                                    # Remove comment cache
                                    CacheHelper.io.delete(namespace)
                                    
                                    result['status'] = 'success'
                            else:
                                result['message'] = 'Not allowed'

                        elif comment_action in ('hide', 'unhide'):
                            if uid == db_comments.author_id or is_moderator:
                                if db_comments is not None:
                                    db_comments.is_hidden = (comment_action == 'hide' and True)
                                    db_comments.hidden_date = datetime.now()
                                    db_comments.save()

                                    # Remove comment cache
                                    CacheHelper.io.delete(namespace)

                                result['status'] = 'success'
                            else:
                                result['message'] = 'Not allowed'

                        elif comment_action in ('relevant', 'irrelevant'):
                            index_item = _IndexContentHelper.get(db_comments.id, 'comment')

                            if not index_item:
                                index_item = _IndexIds.objects.get_or_create(
                                    item_type=TypesHelper.encode('comment'),
                                    item_id=db_comments.id,
                                )[0]

                            RelevanceHelper.update(
                                request.user,
                                index_item,
                                comment_action,
                            )

                            # Remove comment cache
                            CacheHelper.io.delete(namespace)

                            result['status'] = 'success'

                        elif comment_action in ('flag'):
                            if not Flag.objects.filter(comment=db_comments, author=user).exists():
                                Flag(
                                    comment=db_comments,
                                    author=user,
                                ).save()

                                # Remove comment cache
                                CacheHelper.io.delete(namespace)

                            result['status'] = 'success'

                        else:
                            result['message'] = 'Unexpected error'
                    
                    except (_IndexIds.DoesNotExist, Active.DoesNotExist):
                        result['message'] = 'Not found'
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
