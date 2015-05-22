# -*- coding: utf-8 -*-

# Testing environment settings

from .common import LOGGING, AVATAR_DEFAULT_PATH


DEBUG = True
TEMPLATE_DEBUG = DEBUG

USE_X_FORWARDED_HOST = True

ALLOWED_HOSTS = ['waaave.com.test', 'avatar.waaave.com.test', 'api.waaave.com.test']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'waaave_testing',
        'USER': 'travis',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
    }
}

REDIS = {
    'host': 'localhost',
    'port': 6379,
    'db': 5,
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'waaave_testing',
        'TIMEOUT': 600,
    }
}

BROKER_URL = 'redis://%s:%s/%s' % (REDIS['host'], REDIS['port'], REDIS['db'],)
CELERY_RESULT_BACKEND = BROKER_URL
CELERY_REDIRECT_STDOUTS_LEVEL = 'CRITICAL'

EVENTS_HOST = 'events.waaave.com.test'
API_HOST = 'api.waaave.com.test'
AVATAR_HOST = 'avatar.waaave.com.test'

SITE_URL = 'http://waaave.com.test/'
API_URL = 'http://%s/' % API_HOST
AVATAR_URL = 'http://%s/' % AVATAR_HOST
MEDIA_URL = 'http://media.waaave.com.test/'
STATIC_URL = 'http://static.waaave.com.test/'
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
        'handlers': ['all_console'],
        'level': 'CRITICAL',
        'propagate': True,
    },
    'django.security.DisallowedHost': {
        'handlers': ['null'],
        'propagate': False,
    },
    'celery.task': {
        'handlers': ['all_console'],
        'level': 'CRITICAL',
        'propagate': True,
    },
    'celery.redirected': {
        'handlers': ['all_console'],
        'level': 'CRITICAL',
        'propagate': True,
    }
}

DEPLOY = {
    'django': {
        'clean': 'find ./app/ -name "*.pyc" -exec rm -rf {} \;',
        'env': 'if [ ! -f "./env/bin/python" ]; then virtualenv -p /usr/bin/python2 env --no-site-packages; fi',
        'install': ['export PATH=$PATH:/Applications/MAMP/Library/bin/; ./tools/setup.py install', ['retry_error']],
        'syncdb': './tools/manage.py syncdb --noinput',
        'migrate': './tools/manage.py migrate --noinput',
        'index': './tools/manage.py update_index --remove',
        'collectstatic': './tools/manage.py collectstatic --noinput',
    },

    'static': {
        'install': 'cd ./static/; npm install',
        'clean': None, #'cd ./static/; npm run-script clean',
        'build': 'cd ./static/; npm run-script build-testing',
    },

    'events': {
        'install': 'cd ./events/; npm install',
    },

    'run': {
        'start': '',
        'wait': False,
        'stop': '',
    }
}

RUN = [
    ['celery', [
        ['daemon', (
                    './tools/manage.py celeryd'
                    ' -l CRITICAL'
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
                    ' --env=testing'
                    ' --port=8205'
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
]

# Note: we fallback onto production there since Gravatar needs to open this URL from an Internet-open machine
GRAVATAR_DEFAULT_IMAGE = 'https://static.waaave.com/%s' % AVATAR_DEFAULT_PATH['default']['original']
