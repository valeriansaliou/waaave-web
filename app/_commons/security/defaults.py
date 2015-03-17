from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from _commons.helpers.redirects import login_required_url
from account.helpers import RegisterHelper

from account.models import Register as AccountRegister
from account.models import Confirm as AccountConfirm


AUTH_CODES = {
    'allowed': 0,
    'protected': 1,
    'register': 2,
    'anonymous': 3
}


def is_register_complete(request):
    """
    Return whether the user registration is complete or not
    """
    try:
        return AccountRegister.objects.get(user=request.user).complete
    except AccountRegister.DoesNotExist:
        return False


def reg_manager(request):
    """
    Return the redirect URL for register process (if any)
    """
    if request.user.is_authenticated():
        if not is_register_complete(request):
            resume_url = reverse('account.views.register_%s' % RegisterHelper.step(request))
            if request.path != resume_url:
                return HttpResponseRedirect(resume_url)
        return None
    return HttpResponseRedirect(reverse('account.views.register_root'))


def auth_processor(request, protected=True, anonymous_only=False):
    """
    Manage the user authentication level
    """
    # User authenticated?
    if request.user.is_authenticated() and request.user.is_active:
        if not is_register_complete(request):
            return AUTH_CODES['register']
        if anonymous_only:
            return AUTH_CODES['anonymous']
    elif protected:
        return AUTH_CODES['protected']

    return AUTH_CODES['allowed']


def auth_manager(request, protected=True, anonymous_only=False):
    """
    Return the redirect URL for authentication status
    """
    auth_p = auth_processor(request, protected, anonymous_only)

    if auth_p == AUTH_CODES['protected']:
        return HttpResponseRedirect(login_required_url(request.path))
    if auth_p == AUTH_CODES['register']:
        return HttpResponseRedirect(reverse('account.views.register_%s' % RegisterHelper.step(request)))
    if auth_p == AUTH_CODES['anonymous']:
        return HttpResponseRedirect('/')

    return None


def user_confirmed(request):
    """
    Return whether the user is confirmed or not
    """
    try:
        return AccountConfirm.objects.get(user=request.user).confirmed
    except AccountConfirm.DoesNotExist:
        return True