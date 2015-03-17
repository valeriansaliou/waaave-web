"""
WSGI config for waaave-web.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

"""

import os


# We defer to a DJANGO_SETTINGS_MODULE already in the environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "_settings")


# This application object is used by any WSGI server configured
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()