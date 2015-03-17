from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from _commons.decorators.security import auth_required


@auth_required
def root(request):
    """
    Activity > Root
    """
    return render(request, 'activity/activity_root.jade')


@auth_required
def statistics(request):
    """
    Activity > Statistics
    """
    return render(request, 'activity/activity_statistics.jade')


@auth_required
def comments(request):
    """
    Activity > Comments
    """
    return render(request, 'activity/activity_comments.jade')