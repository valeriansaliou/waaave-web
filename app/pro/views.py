from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


def root(request):
    """
    Pro > Root
    """
    return render(request, 'pro/pro_root.jade')