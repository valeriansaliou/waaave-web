from urllib import quote
from urlparse import urlparse

from django.core.urlresolvers import reverse


def login_required_url(url_full):
    """
    Return the login required URL (with next URL redirect)
    """
    url_parse = urlparse(url_full)
    url_path = url_parse.path + url_parse.params
    return '%s?next=%s&required' % (reverse('account.views.login_root'),quote(url_path,''),)


def register_required_url():
    """
    Return the register required URL
    """
    return reverse('account.views.register_root')