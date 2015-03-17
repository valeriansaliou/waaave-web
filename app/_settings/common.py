# -*- coding: utf-8 -*-

# Common settings

import os.path

try:
    import djcelery
    djcelery.setup_loader()
except ImportError:
    pass


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Project owners
ADMINS = (
    (u'Valérian Saliou', 'valerian@waaave.com'),
    (u'Julien Le Coupanec', 'julien@waaave.com'),
    (u'Anthony Peron', 'anthony@waaave.com'),
)

MANAGERS = ADMINS

# Site ID for Site framework
SITE_ID = 1

INTERNAL_IPS = ('127.0.0.1', '::1',)

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Pacific/Honolulu'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = False

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = os.path.abspath(os.path.join(BASE_DIR, '../../media'))

# .zip, .doc, .ppt, .pdf, .odt, .odp, .jpeg, .png
CONTENT_TYPES = [
    # Documents
    'application/msword',
    'application/vnd.ms-powerpoint',
    'application/pdf',
    'application/vnd.oasis.opendocument.text',
    'application/vnd.oasis.opendocument.presentation',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.template',
    'application/vnd.openxmlformats-officedocument.presentationml.template',
    'application/vnd.openxmlformats-officedocument.presentationml.slideshow',
    'application/vnd.openxmlformats-officedocument.presentationml.presentation',
    'application/vnd.openxmlformats-officedocument.presentationml.slide',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.template',

    # Images
    'image/jpeg',
    'image/png',

    # Archives
    'application/x-compress',
    'application/x-compressed',
    'application/tar',
    'application/x-tar',
    'applicaton/x-gtar',
    'multipart/x-tar',
    'application/zip',
    'application/x-zip',
    'application/x-zip-compressed',
    'application/octet-stream',
    'multipart/x-zip',
]

MAX_UPLOAD_SIZE = 20971520 # 20MB

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_SRC_ROOT = os.path.abspath(os.path.join(BASE_DIR, '../../static/src'))
STATIC_ROOT = os.path.abspath(os.path.join(BASE_DIR, '../../static/dist'))

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

TEMPLATE_LOADERS = (
    ('pyjade.ext.django.Loader',(
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    )),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
    '_commons.context_processors.sidebar_left',
    '_commons.context_processors.sidebar_right',
    '_commons.context_processors.notification',
    '_commons.context_processors.alert',
    '_commons.context_processors.conf',
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, '../../template'),
)

# List of middlewares in use
MIDDLEWARE_CLASSES = (
    # GZip output at least
    'django.middleware.gzip.GZipMiddleware',

    # Django middlewares
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',

    # Waaave middlewares
    '_middleware.request.XForwardedForMiddleware',

    # Debug middlewares
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
)

# Configure test runner
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# Core URLs
ROOT_URLCONF = '_core.urls'

# Redirect user to an URL with an ending slash if none is present
APPEND_SLASH = True

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = '_core.wsgi.application'

INSTALLED_APPS_DJANGO = (
    # Django apps
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.sitemaps',
)

INSTALLED_APPS_THIRD_PARTY = (
    # Third-party apps
    'social.apps.django_app.default',
    'email_html',
    'honeypot',
    'pygments',
    'south',
    'django_cron',
    'djcelery',
    'haystack',
    'mathfilters',
    'django_js_utils',
    'robots',
    'humans',
    'gitlab_logging',
    #'debug_toolbar',
)

INSTALLED_APPS_WAAAVE_EXTERNAL = (
    # Waaave external apps
    'gravatar',
    'hitcount',
    'bbcode',
)

INSTALLED_APPS_WAAAVE_INTERNAL = (
    # Waaave internal apps
    '_commons',
    '_index',
    'account',
    'activity',
    'applications',
    'api',
    'avatar',
    'blog',
    'book',
    'comment',
    'company',
    'dashboard',
    'explore',
    'feedback',
    'home',
    'moderation',
    'newsletter',
    'notification',
    'pro',
    'rank',
    'relevance',
    'search',
    'services',
    'share',
    'shot',
    'spot',
    'tag',
    'timeline',
    'tutorial',
    'upload',
    'user',
)

# Installed apps
INSTALLED_APPS = INSTALLED_APPS_DJANGO\
               + INSTALLED_APPS_THIRD_PARTY\
               + INSTALLED_APPS_WAAAVE_EXTERNAL\
               + INSTALLED_APPS_WAAAVE_INTERNAL

# Authentication backends
AUTHENTICATION_BACKENDS = (
    'social.backends.facebook.FacebookOAuth2',
    'social.backends.twitter.TwitterOAuth',
    'social.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

CRON_CLASSES_THIRD_PARTY = [
    # Third-party cron jobs
    'django_cron.cron.FailedRunsNotificationCronJob',
]

CRON_CLASSES_INTERNAL = [
    # Waaave internal cron jobs
    '_index.cron.UpdateIndexCronJob',
    'avatar.cron.UpdateAvatarCronJob',
    'feedback.cron.InviteFeedbackCronJob',
]

# Cron job classes
CRON_CLASSES = CRON_CLASSES_THIRD_PARTY\
             + CRON_CLASSES_INTERNAL

FAILED_RUNS_CRONJOB_EMAIL_PREFIX = "[WARNING] "

# Celery
BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}
CELERY_TASK_RESULT_EXPIRES = 3600
CELERYD_HIJACK_ROOT_LOGGER = False

CELERY_IMPORTS = (
    '_commons.tasks',
    '_index.tasks',
)

# Django Social Auth (Facebook)
# FB App is defined per-environment
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email', 'user_location', 'user_work_history', 'user_website']

# Django Social Auth (Twitter)
SOCIAL_AUTH_TWITTER_KEY = 'yNMsfXZycBvDk6gt8L3AQ'
SOCIAL_AUTH_TWITTER_SECRET = 'uXoavdz41E0LrHjXtV0m3Lo7r5Zq3AO53BWPdnW5gF0'

# Django Social Auth (Google)
SOCIAL_AUTH_GOOGLE_OAUTH2_EXTRA_DATA = [('id', 'id')]

# Django Social Auth (Common)
SOCIAL_AUTH_BACKENDS = {
    'twitter': 'Twitter',
    'facebook': 'Facebook',
    'google-oauth2': 'Google+',
}

SOCIAL_AUTH_LOGIN_URL = '/account/login/'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'
SOCIAL_AUTH_LOGIN_ERROR_URL = '%s?social_auth_failed' % SOCIAL_AUTH_LOGIN_URL
SOCIAL_AUTH_LOGIN_REVOKED_URL = '%s?social_auth_revoked' % SOCIAL_AUTH_LOGIN_URL
SOCIAL_AUTH_NEW_USER_REDIRECT_URL = '/account/register/go/'
SOCIAL_AUTH_NEW_ASSOCIATION_REDIRECT_URL = '/account/settings/'
SOCIAL_AUTH_CONNECT_ERROR_URL = '%s?social_cannot_connect' % SOCIAL_AUTH_NEW_ASSOCIATION_REDIRECT_URL
SOCIAL_AUTH_DISCONNECT_REDIRECT_URL = SOCIAL_AUTH_NEW_ASSOCIATION_REDIRECT_URL
SOCIAL_AUTH_DISCONNECT_ERROR_URL = '%s?social_cannot_disconnect' % SOCIAL_AUTH_DISCONNECT_REDIRECT_URL

# Social auth tweakings
SOCIAL_AUTH_UID_LENGTH = 223
SOCIAL_AUTH_UUID_LENGTH = 16
SOCIAL_AUTH_SANITIZE_REDIRECTS = False
SOCIAL_AUTH_URLOPEN_TIMEOUT = 10
SOCIAL_AUTH_FORCE_POST_DISCONNECT = True
SOCIAL_AUTH_SESSION_EXPIRATION = False
SOCIAL_AUTH_REVOKE_TOKENS_ON_DISCONNECT = True

# Social auth pipeline
SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.social_auth.associate_by_email',
    'account.pipeline.get_username',
    'social.pipeline.user.create_user',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'account.pipeline.update_user_avatar',
    'account.pipeline.fill_profile_user',
    'account.pipeline.move_comment_pool',
)

SOCIAL_AUTH_DISCONNECT_PIPELINE = (
    'social.pipeline.disconnect.allowed_to_disconnect',
    'social.pipeline.disconnect.get_entries',
    'social.pipeline.disconnect.disconnect',
    'account.pipeline.remove_avatar_binding',
)

# Common e-mail send settings
EMAIL_HOST_USER = 'server@waaave.com'
EMAIL_HOST_PASSWORD = 'UWe3i8yD98Fv3WnmP1k5'
EMAIL_HOST = 'mail.gandi.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_SUBJECT_PREFIX = ''
SERVER_EMAIL = 'server@waaave.com'

# Custom email settings
EMAIL_NAME = 'Waaave'
EMAIL_NOREPLY = 'noreply@waaave.com'
EMAIL_CONTACT = 'hello@waaave.com'

# Honeypot settings
HONEYPOT_FIELD_NAME = 'cake'

# Session values
SESSION_COOKIE_HTTPONLY = False
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_REMEMBER_EXPIRITY = 365*12*30*60*60

# Avatar configuration
AVATAR_SIZE_SMALL = 40
AVATAR_SIZE_NORMAL = 55
AVATAR_SIZE_LARGE = 70
AVATAR_SIZE_ORIGINAL = 512
AVATAR_CACHE_EXPIRITY = 24*60*60
AVATAR_ROOT = os.path.abspath(os.path.join(BASE_DIR, '../../avatar'))
AVATAR_ALLOWED_EXTENSIONS = ('jpg', 'jpeg', 'png', 'gif',)
AVATAR_IMG_CLASS = 'picture'
AVATAR_DEFAULT_MIME = 'image/png'
AVATAR_DEFAULT_EXTENSION = 'png'
AVATAR_DEFAULT_SIZE = 'normal'
AVATAR_SOURCES_DIR = 'controllers/layout/images/layout_both'
AVATAR_DEFAULT_PATH = {
    'default': {
        'small': '%s/default_avatar_small.png' % AVATAR_SOURCES_DIR,
        'normal': '%s/default_avatar.png' % AVATAR_SOURCES_DIR,
        'large': '%s/default_avatar_large.png' % AVATAR_SOURCES_DIR,
        'original': '%s/default_avatar_original.png' % AVATAR_SOURCES_DIR,
    },

    'circle': {
        'small': '%s/default_avatar_small_circle.png' % AVATAR_SOURCES_DIR,
        'normal': '%s/default_avatar_circle.png' % AVATAR_SOURCES_DIR,
        'large': '%s/default_avatar_large_circle.png' % AVATAR_SOURCES_DIR,
        'original': '%s/default_avatar_original_circle.png' % AVATAR_SOURCES_DIR,
    },
}

# Gravatar configuration
GRAVATAR_URL_PREFIX = 'http://www.gravatar.com/'
GRAVATAR_DEFAULT_RATING = 'rg'
GRAVATAR_DEFAULT_SIZE = 55
GRAVATAR_IMG_CLASS = 'picture'

# Haystack configuration
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(BASE_DIR, '../../tmp/indexes/'),
    },
}

# Hitcount configuration
HITCOUNT_KEEP_HIT_ACTIVE = { 'days': 1 }
HITCOUNT_HITS_PER_IP_LIMIT = 0

# Django-js-utils configuration
URLS_JS_GENERATED_FILE='static/src/controllers/dutils.conf.urls.js'

# Social accounts
FACEBOOK_PAGE = 'https://www.facebook.com/waaavehq'
TWITTER_PAGE = 'https://twitter.com/waaavehq'

# GitLab options
#GITLAB_HOST = 'https://gitlab.com/'
#GITLAB_PROJECT_ID = 114
#GITLAB_ASSIGNEE_ID = 2

# Amazon options
AMAZON_URL = 'http://www.amazon.com'
AMAZON_AFFILIATE_ID = 'frenc09-20'

# Debug toolbar
DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]

DEBUG_TOOLBAR_CONFIG = {
    'INSERT_BEFORE': '<div class="end_body"></div>',
    'ENABLE_STACKTRACES': False,
    'SHOW_COLLAPSED': True,
}

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(asctime)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'all_console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'django_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, '../../log/django.log'),
            'formatter': 'verbose',
            'maxBytes': 1024 * 1024 * 2, # 2 MB
        },
        'celery_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, '../../log/celery.log'),
            'formatter': 'verbose',
            'maxBytes': 1024 * 1024 * 2, # 2 MB
        },
        'mail_admins': {
            'level': 'DEBUG',
            'class': 'django.utils.log.AdminEmailHandler',
        },
        'gitlab_issues': {
            'level': 'ERROR',
            'class': 'gitlab_logging.handlers.GitlabIssuesHandler',
        },
    },
}
