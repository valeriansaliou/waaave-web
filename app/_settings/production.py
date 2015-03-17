# -*- coding: utf-8 -*-

# Production environment settings

import os
from .common import BASE_DIR, LOGGING, AVATAR_DEFAULT_PATH, GITLAB_HOST, GITLAB_PROJECT_ID, GITLAB_ASSIGNEE_ID


ALLOWED_HOSTS = ['waaave.com', 'avatar.waaave.com', 'api.waaave.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'waaave_production',
        'USER': 'waaave',
        'PASSWORD': 'OBFUSCATED',
        'HOST': 'localhost',
        'PORT': '',
        'CONN_MAX_AGE': 25,
    }
}

REDIS = {
    'host': 'localhost',
    'port': 6379,
    'db': 2,
}

MEMCACHED = {
    'host': 'localhost',
    'port': 11211,
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '%s:%s' % (MEMCACHED['host'], MEMCACHED['port'],),
        'KEY_PREFIX': 'waaave_production',
        'TIMEOUT': 600,
    },

    'staticfiles': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'staticfiles',
        'TIMEOUT': 3600 * 24 * 8,
        'MAX_ENTRIES': 10000,
    },
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

BROKER_URL = 'redis://%s:%s/%s' % (REDIS['host'], REDIS['port'], REDIS['db'],)
CELERY_RESULT_BACKEND = BROKER_URL
CELERY_REDIRECT_STDOUTS_LEVEL = 'DEBUG'
CELERY_SEND_TASK_ERROR_EMAILS = False

EVENTS_HOST = 'events.waaave.com'
API_HOST = 'api.waaave.com'
AVATAR_HOST = 'avatar.waaave.com'

SITE_URL = 'https://waaave.com/'
API_URL = 'https://%s/' % API_HOST
AVATAR_URL = 'https://%s/' % AVATAR_HOST
MEDIA_URL = 'https://media.waaave.com/'
STATIC_URL = 'https://static.waaave.com/'
EVENTS_URL = 'https://%s/' % EVENTS_HOST

SECRET_KEY = 'OBFUSCATED'
API_KEY = 'OBFUSCATED'

STATICFILES_DIRS = (
    os.path.abspath(os.path.join(BASE_DIR, '../../static/build')),
)

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.CachedStaticFilesStorage'

SOCIAL_AUTH_FACEBOOK_KEY = 'OBFUSCATED'
SOCIAL_AUTH_FACEBOOK_SECRET = 'OBFUSCATED'
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = 'OBFUSCATED'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'OBFUSCATED'

#GITLAB_USER = 'hakuma.server'
#GITLAB_TOKEN = 'OBFUSCATED'

LOGGING['loggers'] = {
    'django.request': {
        'handlers': ['django_file', 'gitlab_issues'],
        'level': 'ERROR',
        'propagate': True,
    },
    'django.security.DisallowedHost': {
        'handlers': ['null'],
        'propagate': False,
    },
    'celery.task': {
        'handlers': ['celery_file'],
        'level': 'ERROR',
        'propagate': True,
    },
    'celery.redirected': {
        'handlers': ['celery_file'],
        'level': 'ERROR',
        'propagate': True,
    }
}

DEPLOY = {
    'django': {
        'clean': 'find ./app/ -name "*.pyc" -exec rm -rf {} \;',
        'env': 'if [ ! -f "./env/bin/python" ]; then virtualenv -p /usr/bin/python2 env --no-site-packages; fi',
        'install': ['./tools/setup.py install', ['retry_error']],
        'syncdb': './tools/manage.py syncdb --noinput',
        'migrate': './tools/manage.py migrate --noinput',
        'index': './tools/manage.py update_index --remove',
        'collectstatic': './tools/manage.py collectstatic --noinput',
    },

    'static': {
        'install': 'cd ./static/; npm install',
        'clean': None, #'cd ./static/; npm run-script clean',
        'build': 'cd ./static/; npm run-script build-production',
    },

    'events': {
        'install': 'cd ./events/; npm install',
    },

    'run': {
        'start': 'run web waaave.com start',
        'wait': True,
        'stop': 'run web waaave.com stop',
    }
}

RUN = [
    ['celery', [
        ['daemon', (
                    './tools/manage.py celeryd'
                    ' -l ERROR'
                    ' --pidfile {pid_file}'
                    ' -f {log_file}'
                   )],
    ]],

    ['events', [
        ['server', (
                    '%s'
                    ' --socket={socket_file}'
                    ' --logfile={log_file}'
                   ) % (
                    ' ./tools/events.py'
                    ' --env=production'
                    ' --redis_host={redis_host}'
                    ' --redis_port={redis_port}'
                    ' --redis_db={redis_db}'
                    ' --api_url={api_url}'
                    ' --api_key={api_key}'
                    ' --gitlab_host={gitlab_host}'
                    ' --gitlab_project_id={gitlab_project_id}'
                    ' --gitlab_assignee_id={gitlab_assignee_id}'
                    ' --gitlab_user={gitlab_user}'
                    ' --gitlab_token={gitlab_token}'
                   ).format(
                    redis_host=REDIS['host'],
                    redis_port=REDIS['port'],
                    redis_db=REDIS['db'],
                    api_url=API_URL,
                    api_key=API_KEY,
                    gitlab_host=GITLAB_HOST,
                    gitlab_project_id=GITLAB_PROJECT_ID,
                    gitlab_assignee_id=GITLAB_ASSIGNEE_ID,
                    gitlab_user=GITLAB_USER,
                    gitlab_token=GITLAB_TOKEN
                   )],
    ]],

    ['django', [
        ['server', (
                    './tools/uwsgi.py'
                    ' --master'
                    ' --processes 1'
                    ' --threads 1'
                    ' --workers 2'
                    ' --harakiri 20'
                    ' --log-x-forwarded-for'
                    ' --uwsgi-socket {socket_file}'
                    ' --pidfile {pid_file}'
                   )],
    ]],
]

GRAVATAR_DEFAULT_IMAGE = 'https://static.waaave.com/%s' % AVATAR_DEFAULT_PATH['default']['original']
