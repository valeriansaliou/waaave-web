from django.conf.urls import patterns
from robots.utils import url

urlpatterns = patterns('user.views',
    (r'^(?P<username>[\w\.-]+)/$', 'main'),
    url(r'^(?P<username>[\w\.-]+)/fetch/(?P<page>\d+)/$', 'main_fetch', robots_allow=False),

    (r'^(?P<username>[\w\.-]+)/following/$', 'main_following'),
    url(r'^(?P<username>[\w\.-]+)/following/fetch/(?P<page>\d+)/$', 'main_following_fetch', robots_allow=False),

    (r'^(?P<username>[\w\.-]+)/followers/$', 'main_followers'),
    url(r'^(?P<username>[\w\.-]+)/followers/fetch/(?P<page>\d+)/$', 'main_followers_fetch', robots_allow=False),

    (r'^(?P<username>[\w\.-]+)/interests/$', 'main_interests'),
    url(r'^(?P<username>[\w\.-]+)/interests/fetch/(?P<page>\d+)/$', 'main_interests_fetch', robots_allow=False),
)