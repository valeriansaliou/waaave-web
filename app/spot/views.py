import json

from django.shortcuts import render
from django.http import HttpResponse, HttpResponsePermanentRedirect, Http404
from django.contrib.humanize.templatetags import humanize
from django.core.urlresolvers import reverse

from _commons.helpers.redirects import login_required_url, register_required_url

from .helpers import *
from .models import *


def root(request):
    """
    Spot > Root
    """
    return HttpResponsePermanentRedirect(reverse('explore.views.spots'))


def view_root(request, tag, page=1):
    """
    Spot > View Root
    """
    success, response_data = SpotHelper.build_response(
        request=request,
        fn_name='view_root',
        tag=tag,
        items_per_page=10,
        page=page,
    )

    if not success:
        raise Http404

    return render(request, 'spot/spot_view_root.jade', response_data)


def view_root_fetch(request, tag, page):
    """
    Spot > View Root Fetch
    """
    success, response_data = SpotHelper.build_response(
        request=request,
        fn_name='view_root_fetch',
        tag=tag,
        items_per_page=10,
        page=page,
    )

    if not success:
        raise Http404

    if len(response_data['timeline']):
        return render(request, 'spot/spot_view_root_fetch.jade', response_data)

    return HttpResponse(
        json.dumps({
            'status': 'error',
            'message': 'Page overflow',
            'contents': {}
        }),
        content_type='application/json'
    )


def view_tutorials(request, tag, page=1):
    """
    Spot > Tutorials
    """
    success, response_data = SpotHelper.build_response(
        request=request,
        fn_name='view_tutorials',
        tag=tag,
        items_per_page=12,
        page=page,
    )

    if not success:
        raise Http404

    return render(request, 'spot/spot_view_tutorials.jade', response_data)


def view_books(request, tag, page=1):
    """
    Spot > Books
    """
    success, response_data = SpotHelper.build_response(
        request=request,
        fn_name='view_books',
        tag=tag,
        items_per_page=12,
        page=page,
    )

    if not success:
        raise Http404

    return render(request, 'spot/spot_view_books.jade', response_data)


def view_waaavers(request, tag, page=1):
    """
    Spot > Waaavers
    """
    success, response_data = SpotHelper.build_response(
        request=request,
        fn_name='view_waaavers',
        tag=tag,
        items_per_page=20,
        page=page,
    )

    if not success:
        raise Http404

    return render(request, 'spot/spot_view_waaavers.jade', response_data)


def join(request, tag):
    """
    Spot > Join
    """
    result = {
        'status': 'error',
        'message': '',
        'contents': {}
    }

    spot = SpotHelper.resolve(tag)
    user = request.user

    if spot:
        if request.method == 'POST':
            join_state = request.POST.get('join_state', 0)

            if join_state.isdigit():
                join_state = int(join_state)

            if join_state in (0, 1):
                join = True if join_state else False

                if user.is_authenticated():
                    SpotHelper.join(user, spot, join)

                    result['status'] = 'success'
                    result['contents']['status'] = join_state
                    result['contents']['count'] = humanize.intcomma(
                        Membership.objects.filter(spot=spot, is_active=True).count()
                    )
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
