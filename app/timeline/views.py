import json

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from _commons.decorators.security import auth_required

from .helpers import *


@auth_required
def root(request):
    """
    Timeline > Root
    """
    response_data = FollowTimelineHelper.build_response(
        request=request,
        fetch_filter='following',
    )

    if not len(response_data['timeline']):
        return HttpResponseRedirect(reverse('timeline.views.everyone'))

    return render(request, 'timeline/timeline_root.jade', response_data)


@auth_required
def fetch(request, fetch_filter, page=1):
    """
    Timeline > Fetch
    """
    response_data = FollowTimelineHelper.build_response(
        request=request,
        fetch_filter=fetch_filter,
        page=int(page),
    )

    if len(response_data['timeline']):
        return render(request, 'timeline/timeline_fetch.jade', response_data)
    
    return HttpResponse(
        json.dumps({
            'status': 'error',
            'message': 'Page overflow',
            'contents': {}
        }),
        content_type='application/json'
    )


@auth_required
def followers(request):
    """
    Timeline > Followers
    """
    response_data = FollowTimelineHelper.build_response(
        request=request,
        fetch_filter='followers',
    )
    
    if not len(response_data['timeline']):
        return HttpResponseRedirect(reverse('home.views.root'))

    return render(request, 'timeline/timeline_followers.jade', response_data)


@auth_required
def everyone(request):
    """
    Timeline > Everyone
    """
    response_data = FollowTimelineHelper.build_response(
        request=request,
        fetch_filter='everyone',
    )
    
    return render(request, 'timeline/timeline_everyone.jade', response_data)