from django.conf.urls import patterns
from robots.utils import url

urlpatterns = patterns('notification.views',
    (r'^$', 'root'),
    url(r'^fetch/page/(?P<page>\d+)/$', 'fetch_page', robots_allow=False),
    url(r'^fetch/single/(?P<notif_type>comment|response|spot|waaave|follow|follow-add)/(?P<notif_id>\d+)/$', 'fetch_single', robots_allow=False),
    url(r'^read/(?P<read_type>all)/$', 'read', robots_allow=False),
    url(r'^read/(?P<read_type>single)/(?P<notif_type>comment|response|spot|waaave|follow|follow-add|rank-up)/(?P<notif_id>\d+)/$', 'read', robots_allow=False),
)