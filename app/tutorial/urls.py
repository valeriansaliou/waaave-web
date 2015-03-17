from django.conf.urls import patterns
from robots.utils import url

urlpatterns = patterns('tutorial.views',
    (r'^$', 'root'),
    (r'^(?P<tag>[\w-]+)/(?P<slug>[\w-]+)/$', 'view'),
    (r'^(?P<tag>[\w-]+)/(?P<slug>[\w-]+)/related/tutorials/$', 'view_related_tutorials'),
    url(r'^(?P<tag>[\w-]+)/(?P<slug>[\w-]+)/related/tutorials/fetch/(?P<page>\d+)/$', 'view_related_tutorials_fetch', robots_allow=False),
    (r'^(?P<tag>[\w-]+)/(?P<slug>[\w-]+)/related/developers/$', 'view_related_developers'),
    url(r'^(?P<tag>[\w-]+)/(?P<slug>[\w-]+)/related/developers/fetch/(?P<page>\d+)/$', 'view_related_developers_fetch', robots_allow=False),
)