from django.conf.urls import patterns, include
from robots.utils import url

relevance_pattern = patterns('relevance.views',
    url(r'^action/$', 'action', robots_allow=False),
)

urlpatterns = patterns('',
    (r'^(?P<item_type>tutorial|book)/(?P<item_id>\d+)/', include(relevance_pattern))
)