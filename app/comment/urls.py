from django.conf.urls import patterns, include
from robots.utils import url

comment_patterns = patterns('comment.views',
    url(r'^read/$', 'read', robots_allow=False),
    url(r'^add/$', 'add', robots_allow=False),
    url(r'^action/$', 'action', robots_allow=False),
)

urlpatterns = patterns('',
    (r'^(?P<item_type>tutorial|shot|book|spot|blog)/(?P<item_id>\d+)/', include(comment_patterns))
)