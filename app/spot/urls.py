from django.conf.urls import patterns
from robots.utils import url

urlpatterns = patterns('spot.views',
    (r'^$', 'root'),
    
    (r'^(?P<tag>[\w-]+)/(?:(?P<page>\d+)/)?$', 'view_root'),
    url(r'^(?P<tag>[\w-]+)/fetch/(?P<page>\d+)/$', 'view_root_fetch', robots_allow=False),

    (r'^(?P<tag>[\w-]+)/tutorials/(?:(?P<page>\d+)/)?$', 'view_tutorials'),
    (r'^(?P<tag>[\w-]+)/books/(?:(?P<page>\d+)/)?$', 'view_books'),
    (r'^(?P<tag>[\w-]+)/waaavers/(?:(?P<page>\d+)/)?$', 'view_waaavers'),

    url(r'^ajax/join/(?P<tag>[\w-]+)/', 'join', robots_allow=False),
)
