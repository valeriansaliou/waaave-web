from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

from api.helpers import *
from avatar.helpers import *


def __error_response(request, message, status):
    """
    Commons > Error Response Helper
    """
    host = request.get_host()

    if host == settings.API_HOST:
        return APIHelper.response(
            message=message,
            http_code=status,
        )
    elif host == settings.AVATAR_HOST:
        return HttpResponse(
            message,
            content_type='text/plain',
            status=status,
        )

    return render(
        request,
        ('%s.jade' % status),
        status=status
    )


def bad_request_400(request):
    """
    Commons > 400 Bad Request
    """
    return __error_response(request, 'Bad Request', 400)


def forbidden_403(request):
    """
    Commons > 403 Forbidden
    """
    return __error_response(request, 'Forbidden', 403)


def not_found_404(request):
    """
    Commons > 404 Not Found
    """
    return __error_response(request, 'Not Found', 404)


def server_error_500(request):
    """
    Commons > 500 Server Error
    """
    return __error_response(request, 'Server Error', 500)
