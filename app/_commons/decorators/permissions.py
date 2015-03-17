from django.http import Http404


def user_staff_required(f):
    """
    Protects staff-only pages
    """
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated() and (request.user.is_staff or request.user.is_superuser):
            return f(request, *args, **kwargs)
        return Http404

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap