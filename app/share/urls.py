from django.conf.urls import patterns
from robots.utils import url

urlpatterns = patterns('share.views',
    url(r'^ajax/waaave/(?P<item_type>tutorial|book|shot|blog)/(?P<item_id>\d+)/', 'waaave', robots_allow=False),
    url(r'^ajax/follow/(?P<user_id>\d+)/', 'follow', robots_allow=False),
)