from django.conf import settings

from .helpers import APIHelper


def api_key_required(f):
    """
    Protects non-public API sections
    """
    def wrap(request, *args, **kwargs):
        """
        Wraps the decorated function
        """
        api_key = request.POST.get('api_key', None)

        if api_key is None:
            return APIHelper.response(
                message='Unauthorized',
                http_code=401,
            )

        elif request.POST.get('api_key') == settings.API_KEY:
            return f(request, *args, **kwargs)
        
        else:
            return APIHelper.response(
                message='Forbidden',
                http_code=403,
            )

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__

    return wrap
