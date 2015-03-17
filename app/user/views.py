import json

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User as AuthUser

from share.models import Follow as ShareFollow

from _commons.helpers.cache import CacheHelper
from timeline.helpers import UserTimelineHelper

from .helpers import *


def main(request, username):
    """
    User > Main
    """
    namespace = CacheHelper.ns('user:views:main', username=username)
    response_data = CacheHelper.io.get(namespace)

    if response_data is None:
        response_data, user = MainUserHelper.build_response(request, username)

        if response_data['status'] == 'not_found':
            raise Http404

        response_data.update(
            UserTimelineHelper.build_response(
                request=request,
                user=user,
            )
        )

        CacheHelper.io.set(namespace, response_data, 30)

    return render(request, 'user/user_main.jade', response_data)


def main_fetch(request, username, page=1):
    """
    User > Main Fetch
    """
    namespace = CacheHelper.ns('user:views:main_fetch', username=username, page=page)
    response_data = CacheHelper.io.get(namespace)

    if response_data is None:
        try:
            aut_user = AuthUser.objects.get(username=username)
        except AuthUser.DoesNotExist:
            raise Http404

        response_data = UserTimelineHelper.build_response(
            request=request,
            user=aut_user,
            page=int(page),
        )

        CacheHelper.io.set(namespace, response_data, 30)

    if len(response_data['timeline']):
        return render(request, 'user/user_main_fetch.jade', response_data)

    return HttpResponse(
        json.dumps({
            'status': 'error',
            'message': 'Page overflow',
            'contents': {}
        }),
        content_type='application/json'
    )


def me(request):
    """
    User > Me
    """
    if not request.user.is_authenticated():
        raise Http404
    
    return HttpResponseRedirect(reverse('user.views.main', kwargs={
        'username': request.user.username
    }))


def main_following(request, username):
    """
    User > Main Following
    """
    namespace = CacheHelper.ns('user:views:main_following', username=username)
    response_data = CacheHelper.io.get(namespace)

    if response_data is None:
        response_data, user = MainUserHelper.build_following_response(request, username)

        if response_data['status'] == 'not_found':
            raise Http404

        CacheHelper.io.set(namespace, response_data, 60)

    return render(request, 'user/user_main_following.jade', response_data)


def main_following_fetch(request, username, page):
    """
    User > Main Following Fetch
    """
    namespace = CacheHelper.ns('user:views:main_following_fetch', username=username, page=page)
    response_data = CacheHelper.io.get(namespace)

    if response_data is None:
        response_data, _ = MainUserHelper.build_following_response(
            request=request,
            username=username,
            page=int(page),
        )

        CacheHelper.io.set(namespace, response_data, 60)

    if len(response_data['user_following']):
        return render(request, 'user/user_main_following_fetch.jade', response_data)

    return HttpResponse(
        json.dumps({
            'status': 'error',
            'message': 'Page overflow',
            'contents': {}
        }),
        content_type='application/json'
    )


def main_followers(request, username):
    """
    User > Main Followers
    """
    namespace = CacheHelper.ns('user:views:main_followers', username=username)
    response_data = CacheHelper.io.get(namespace)

    if response_data is None:
        response_data, user = MainUserHelper.build_followers_response(request, username)

        if response_data['status'] == 'not_found':
            raise Http404

        CacheHelper.io.set(namespace, response_data, 60)

    return render(request, 'user/user_main_followers.jade', response_data)


def main_followers_fetch(request, username, page):
    """
    User > Main Followers Fetch
    """
    namespace = CacheHelper.ns('user:views:main_followers_fetch', username=username, page=page)
    response_data = CacheHelper.io.get(namespace)

    if response_data is None:
        response_data, _ = MainUserHelper.build_followers_response(
            request=request,
            username=username,
            page=int(page),
        )
        
        CacheHelper.io.set(namespace, response_data, 60)

    if len(response_data['user_followers']):
        return render(request, 'user/user_main_followers_fetch.jade', response_data)

    return HttpResponse(
        json.dumps({
            'status': 'error',
            'message': 'Page overflow',
            'contents': {}
        }),
        content_type='application/json'
    )


def main_interests(request, username):
    """
    User > Main Interests
    """
    namespace = CacheHelper.ns('user:views:main_interests', username=username)
    response_data = CacheHelper.io.get(namespace)

    if response_data is None:
        response_data, user = MainUserHelper.build_interests_response(request, username)

        if response_data['status'] == 'not_found':
            raise Http404

        CacheHelper.io.set(namespace, response_data, 120)

    return render(request, 'user/user_main_interests.jade', response_data)


def main_interests_fetch(request, username, page):
    """
    User > Main Interests Fetch
    """
    namespace = CacheHelper.ns('user:views:main_interests_fetch', username=username, page=page)
    response_data = CacheHelper.io.get(namespace)

    if response_data is None:
        response_data, _ = MainUserHelper.build_interests_response(
            request=request,
            username=username,
            page=int(page),
        )
        
        CacheHelper.io.set(namespace, response_data, 120)

    if len(response_data['user_interests']):
        return render(request, 'user/user_main_interests_fetch.jade', response_data)

    return HttpResponse(
        json.dumps({
            'status': 'error',
            'message': 'Page overflow',
            'contents': {}
        }),
        content_type='application/json'
    )
