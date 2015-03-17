from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


def root(request):
    return render(request, 'services/services_root.jade')

def advertise(request):
    return render(request, 'services/services_advertise.jade')

def bootstrap(request):
    return render(request, 'services/services_bootstrap.jade')

def api(request):
    return render(request, 'services/services_api.jade')