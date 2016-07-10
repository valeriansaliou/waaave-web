#!/bin/sh
# -*- coding: utf-8 -*-
''''exec python2 -- "$0" ${1+"$@"} # '''

"""
Waaave setup script
Automatically pull app dependencies and install/update them
"""

from setuptools import setup
import os

os.chdir(os.path.join(os.path.dirname(__file__), '../tmp/eggs/'))

# Fixes an issue with Xcode compiler on MacOS
os.environ['ARCHFLAGS'] = '-Wno-error=unused-command-line-argument-hard-error-in-future'

setup(
    name='waaave-web',
    version='1.0.0',
    description='Waaave app',
    url='https://github.com/valeriansaliou/waaave-web',

    author=u'Valérian Saliou',
    author_email='valerian@valeriansaliou.name',

    install_requires=[
        'six==1.8.0',
        'psutil==2.1.3',
        'requests==2.5.0',
        'redis==2.10.3',
        'Pillow==2.6.1',
        'Markdown==2.5.2',
        'uWSGI==2.0.9',
        'MySQL-python==1.2.5',
        'South==1.0.1',
        'BeautifulSoup==3.2.1',
        'pyjade==3.0.0',
        'python-memcached==1.53',
        'requests-oauthlib==0.4.2',
        'python-social-auth==0.1.26',
        'facebook-sdk==0.4.0',
        'python-twitter==2.0',
        'Whoosh==2.5.7',
        'django==1.6.10',
        'django-countries==3.0.1',
        'django-email-html==0.1.8',
        'django-pygments==0.1',
        'django-cron==0.3.5',
        'django-celery-with-redis==3.0',
        'django-haystack==2.3.1',
        'django-mathfilters==0.3.0',
        'django-js-utils==0.0.5dev',
        'django-robots==1.6.2alt',
        'django-humans==0.3alt',
        'django-debug-toolbar==1.2.2',
        'django-honeypot==0.4.0',
        'django-gitlab-logging==0.2.2',
        'django-request-mock==0.1.4',
        'waaave-gravatar==0.5.1',
        'waaave-bbcode==0.5.10',
        'waaave-hitcount==0.6.4',
    ],

    dependency_links=[
        'git://github.com/valeriansaliou/django-robots@1.6.2alt#egg=django-robots-1.6.2alt',
        'git://github.com/valeriansaliou/django-humans@0.3alt#egg=django-humans-0.3alt',

        'git://github.com/valeriansaliou/waaave-gravatar@0.5.1#egg=waaave-gravatar-0.5.1',
        'git://github.com/valeriansaliou/waaave-bbcode@0.5.10#egg=waaave-bbcode-0.5.10',
        'git://github.com/valeriansaliou/waaave-hitcount.git@0.6.4#egg=waaave-hitcount-0.6.4',
    ],
)
