import json

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from _commons.decorators.security import auth_required

from .factories import *
from .helpers import *


@auth_required
def root(request):
    """
    Notification > Root
    """
    return HttpResponseRedirect(reverse('account.views.settings_notifications'))


@auth_required
def fetch_page(request, page=1):
    """
    Notification > Fetch Page
    """
    page = int(page)
    items_per_page = 8

    response_data = NotificationHelper.build_response_page(
        request=request,
        page=page,
        items_per_page=items_per_page,
    )

    if len(response_data['notification_feed']) or page is 1:
        return render(request, 'notification/notification_fetch.jade', response_data)
    
    return HttpResponse(
        json.dumps({
            'status': 'error',
            'message': 'Page overflow',
            'contents': {}
        }),
        content_type='application/json'
    )


@auth_required
def fetch_single(request, notif_type=None, notif_id=None):
    """
    Notification > Fetch Single
    """
    response_data = NotificationHelper.build_response_single(
        request=request,
        notif_type=notif_type,
        notif_id=notif_id,
    )

    if len(response_data['notification_feed']):
        return render(request, 'notification/notification_fetch.jade', response_data)

    return HttpResponse(
        json.dumps({
            'status': 'error',
            'message': 'Not found',
            'contents': {}
        }),
        content_type='application/json'
    )


@auth_required
def read(request, read_type='all', notif_type=None, notif_id=None):
    """
    Notification > Read
    """
    result = {
        'status': 'error',
        'message': '',
        'contents': {}
    }

    if request.method == 'POST':
        if read_type == 'all':
            mark = NotificationHelper.mark_read_all(
                user=request.user,
            )

            if mark > 0:
                result['status'] = 'success'
                result['contents']['count'] = mark
            else:
                result['message'] = 'No unread notification found'

        elif read_type == 'single' and notif_id is not None:
            notif_id = int(notif_id)

            mark = NotificationHelper.mark_read_single(
                user=request.user,
                notif_type=notif_type,
                notif_id=notif_id,
            )

            if mark:
                result['status'] = 'success'
            else:
                result['message'] = 'Already read or does not exist'
    else:
        result['message'] = 'Bad request'

    return HttpResponse(json.dumps(result), content_type='application/json')
