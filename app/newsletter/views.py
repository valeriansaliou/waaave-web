from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


def root(request):
    """
    Newsletter > Root
    """
    return render(request, 'newsletter/newsletter_root.jade')