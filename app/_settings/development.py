# -*- coding: utf-8 -*-

# Development environment settings

from .common import LOGGING, AVATAR_DEFAULT_PATH


DEBUG = True
TEMPLATE_DEBUG = DEBUG

USE_X_FORWARDED_HOST = True

ALLOWED_HOSTS = ['waaave.com.dev', 'avatar.waaave.com.dev', 'api.waaave.com.dev']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'waaave_development',
        'USER': 'waaave',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
    }
}

REDIS = {
    'host': 'localhost',
    'port': 6379,
    'db': 4,
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'waaave_development',
        'TIMEOUT': 600,
    }
}

BROKER_URL = 'redis://%s:%s/%s' % (REDIS['host'], REDIS['port'], REDIS['db'],)
CELERY_RESULT_BACKEND = BROKER_URL
CELERY_REDIRECT_STDOUTS_LEVEL = 'DEBUG'

EVENTS_HOST = 'events.waaave.com.dev'
API_HOST = 'api.waaave.com.dev'
AVATAR_HOST = 'avatar.waaave.com.dev'

SITE_URL = 'http://waaave.com.dev/'
API_URL = 'http://%s/' % API_HOST
AVATAR_URL = 'http://%s/' % AVATAR_HOST
MEDIA_URL = 'http://media.waaave.com.dev/'
STATIC_URL = 'http://static.waaave.com.dev/'
EVENTS_URL = 'http://%s/' % EVENTS_HOST

SECRET_KEY = 'OBFUSCATED'
API_KEY = 'OBFUSCATED'

STATICFILES_DIRS = ()

SOCIAL_AUTH_FACEBOOK_KEY = 'OBFUSCATED'
SOCIAL_AUTH_FACEBOOK_SECRET = 'OBFUSCATED'
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = 'OBFUSCATED'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'OBFUSCATED'

LOGGING['loggers'] = {
    'django.request': {
        'handlers': ['all_console', 'django_file'],
        'level': 'DEBUG',
        'propagate': True,
    },
    'django.security.DisallowedHost': {
        'handlers': ['null'],
        'propagate': False,
    },
    'celery.task': {
        'handlers': ['all_console', 'celery_file'],
        'level': 'DEBUG',
        'propagate': True,
    },
    'celery.redirected': {
        'handlers': ['all_console', 'celery_file'],
        'level': 'DEBUG',
        'propagate': True,
    }
}

DEPLOY = {
    'django': {
        'clean': 'find ./app/ -name "*.pyc" -exec rm -rf {} \;',
        'env': 'if [ ! -f "./env/bin/python" ]; then virtualenv -p /usr/bin/python env --no-site-packages; fi',
        'install': ['export PATH=$PATH:/Applications/MAMP/Library/bin/; ./tools/setup.py install', ['retry_error']],
        'syncdb': './tools/manage.py syncdb --noinput',
        'migrate': './tools/manage.py migrate --noinput',
        'index': './tools/manage.py update_index --remove',
        'collectstatic': './tools/manage.py collectstatic --noinput',
    },

    'static': {
        'install': 'cd ./static/; npm install',
        'clean': None,
        'build': 'cd ./static/; npm run-script build-development',
    },

    'events': {
        'install': 'cd ./events/; npm install',
    },

    'run': {
        'start': './tools/run.py',
        'wait': True,
        'stop': './tools/run.py kill',
    }
}

RUN = [
    ['celery', [
        ['daemon', (
                    './tools/manage.py celeryd'
                    ' -l DEBUG'
                    ' --pidfile {pid_file}'
                    ' -f {log_file}'
                   )],
    ]],

    ['events', [
        ['server', (
                    '%s'
                    ' --logfile={log_file}'
                   ) % (
                    ' ./tools/events.py'
                    ' --env=development'
                    ' --port=8001'
                    ' --redis_host={redis_host}'
                    ' --redis_port={redis_port}'
                    ' --redis_db={redis_db}'
                    ' --api_url={api_url}'
                    ' --api_key={api_key}'
                   ).format(
                    redis_host=REDIS['host'],
                    redis_port=REDIS['port'],
                    redis_db=REDIS['db'],
                    api_url=API_URL,
                    api_key=API_KEY
                   )],
    ]],

    ['django', [
        ['server', (
                    './tools/manage.py'
                    ' runserver 8000'
                   )],
    ]],
]

# Note: we fallback onto production there since Gravatar needs to open this URL from an Internet-open machine
GRAVATAR_DEFAULT_IMAGE = 'https://static.waaave.com/%s' % AVATAR_DEFAULT_PATH['default']['original']
