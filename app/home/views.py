from account.views import login_root
from timeline.views import root as timeline_root


def root(request):
    """
    Home > Root
    """
    if request.user.is_authenticated():
        return timeline_root(request)

    return login_root(request)