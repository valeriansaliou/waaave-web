from django.conf.urls import patterns
from robots.utils import url

urlpatterns = patterns('book.views',
    (r'^$', 'root'),
    (r'^(?P<author>[\w-]+)/(?P<slug>[\w-]+)/$', 'view'),
    url(r'^(?P<author>[\w-]+)/(?P<slug>[\w-]+)/relevance/$', 'view_relevance', robots_allow=False),
)
