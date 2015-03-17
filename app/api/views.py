from django.http import HttpResponse
from django.contrib.sessions.models import Session
from django.views.decorators.csrf import csrf_exempt

from .helpers import APIHelper
from .decorators import api_key_required
from .exceptions import APINotFound


def root(request):
    """
    API > Root
    """
    return APIHelper.response(
        status='success',
        message='Waaave API',
        http_code=200,
    )


@csrf_exempt
@api_key_required
def user_session(request):
    """
    API > User Session
    Reverses a provided user session key to its associated user ID
    """
    session_key = request.POST.get('session_key')

    if session_key:
        try:
            session = Session.objects.get(session_key=session_key)
            user_id = session.get_decoded().get('_auth_user_id')

            if not user_id:
                raise APINotFound()

            return APIHelper.response(
                status='success',
                message='Found an user for session key',
                contents={
                    'user_id': user_id,
                },
                http_code=200,
            )
        except (Session.DoesNotExist, APINotFound):
            return APIHelper.response(
                message='Could not find an user with this session ID',
                http_code=404,
            )

    return APIHelper.response(
        message='Missing POST data',
        http_code=400,
    )
