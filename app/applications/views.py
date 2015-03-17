from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


def root(request):
    """
    Applications > Root
    """
    return render(request, 'applications/applications_root.jade')

def ios(request):
    """
    Applications > iOS
    """
    return render(request, 'applications/applications_ios.jade')

def android(request):
    """
    Applications > Android
    """
    return render(request, 'applications/applications_android.jade')