from django.http import HttpResponseRedirect

from _commons.security.defaults import auth_manager, reg_manager


def auth_required(f):
    """
    Protects auth-required pages
    """
    def wrap(request, *args, **kwargs):
        return auth_manager(request) or f(request, *args, **kwargs)

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap


def anon_required(f):
    """
    Assert anonymous-required pages
    """
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated():
            return HttpResponseRedirect('/')
        return f(request, *args, **kwargs)
    
    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap


def reg_required(f):
    """
    Protects registration pages (semi-auth)
    """
    def wrap(request, *args, **kwargs):
        return reg_manager(request) or f(request, *args, **kwargs)

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap


def new_required(f):
    """
    Protects new registration page (semi-auth)
    """
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated():
            return reg_manager(request) or f(request, *args, **kwargs)
        else:
            return f(request, *args, **kwargs)

    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap